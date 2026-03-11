import math
from dataclasses import dataclass
from pathlib import Path

import pygame

from game.core.snapshot import WorldSnapshot
from game.render.camera import Camera
from game.render.characters import (
    ANIM_DEATH,
    ANIM_IDLE,
    ANIM_THROW,
    ANIM_WALK,
    AnimationClip,
    CharacterSpriteLibrary,
)
from game.render.fonts import UIFonts
from game.render.spritesheet import load_image
from game.settings import GameSettings

ROCK_SPRITE_PATH = Path(__file__).resolve().parents[3] / "assets" / "effects" / "Rock1.png"


@dataclass(slots=True)
class PlayerAnimationState:
    current_animation: str = ANIM_IDLE
    frame_index: int = 0
    frame_progress_seconds: float = 0.0
    throw_time_remaining_seconds: float = 0.0
    last_attack_tick_seen: int = -1
    facing_left: bool = False


class Renderer:
    def __init__(
        self,
        screen: pygame.Surface,
        camera: Camera,
        settings: GameSettings,
        local_player_id: str,
        fonts: UIFonts,
    ) -> None:
        self.screen = screen
        self.camera = camera
        self.settings = settings
        self.local_player_id = local_player_id
        self.hud_font = fonts.hud
        self.character_library = CharacterSpriteLibrary()
        self.player_animation_states: dict[str, PlayerAnimationState] = {}
        self._last_render_time_seconds: float | None = None
        self.rock_sprite_base = load_image(ROCK_SPRITE_PATH)

    def set_screen(self, screen: pygame.Surface) -> None:
        self.screen = screen

    def render(self, snapshot: WorldSnapshot) -> None:
        render_now_seconds = pygame.time.get_ticks() / 1000.0
        if self._last_render_time_seconds is None:
            render_dt = 0.0
        else:
            render_dt = max(0.0, min(0.1, render_now_seconds - self._last_render_time_seconds))
        self._last_render_time_seconds = render_now_seconds

        focus_player = next(
            (
                player
                for player in snapshot.players
                if isinstance(player, dict) and bool(player.get("alive", True))
            ),
            None,
        )
        self.camera.update(
            self._read_position(focus_player) if isinstance(focus_player, dict) else None
        )

        # TODO: Add resolution-aware world scaling during the planned camera/map rendering rework.
        self.screen.fill(self.settings.background_color)
        self._draw_grid()
        self._draw_coins(snapshot)
        self._draw_projectiles(snapshot)
        self._draw_enemies(snapshot)
        self._draw_players(snapshot, render_dt)
        self._draw_hud(snapshot)

    def _draw_grid(self) -> None:
        screen_width, screen_height = self.screen.get_size()
        left = int(self.camera.offset_x) - (int(self.camera.offset_x) % self.settings.grid_step)
        top = int(self.camera.offset_y) - (int(self.camera.offset_y) % self.settings.grid_step)

        for x in range(
            left,
            int(self.camera.offset_x) + screen_width + 1,
            self.settings.grid_step,
        ):
            screen_x = x - int(self.camera.offset_x)
            pygame.draw.line(
                self.screen,
                self.settings.grid_color,
                (screen_x, 0),
                (screen_x, screen_height),
                1,
            )

        for y in range(
            top,
            int(self.camera.offset_y) + screen_height + 1,
            self.settings.grid_step,
        ):
            screen_y = y - int(self.camera.offset_y)
            pygame.draw.line(
                self.screen,
                self.settings.grid_color,
                (0, screen_y),
                (screen_width, screen_y),
                1,
            )

    def _draw_players(self, snapshot: WorldSnapshot, render_dt: float) -> None:
        active_player_ids: set[str] = set()
        for player in snapshot.players:
            if not isinstance(player, dict):
                continue

            player_id = str(player.get("player_id", ""))
            if not player_id:
                continue
            active_player_ids.add(player_id)

            position = self._read_position(player)
            center = self.camera.world_to_screen(position)
            aim_position = self._read_position_dict(player.get("aim_position"))
            direction_x = aim_position[0] - position[0]
            direction_y = aim_position[1] - position[1]

            animation_state = self.player_animation_states.setdefault(
                player_id,
                PlayerAnimationState(),
            )
            if direction_x != 0.0:
                animation_state.facing_left = direction_x < 0.0

            self._update_throw_state(player, animation_state, render_dt)
            target_animation = self._choose_player_animation(player, animation_state)

            character_id = str(
                player.get("character_id", self.settings.default_player_character_id)
            )
            clip = self.character_library.get_animation_clip(character_id, target_animation)

            if clip is None or not clip.frames:
                self._draw_player_fallback_circle(player, center, direction_x, direction_y)
                continue

            self._advance_animation(animation_state, clip, target_animation, render_dt)
            current_frame = clip.frames[animation_state.frame_index]
            if animation_state.facing_left:
                current_frame = pygame.transform.flip(current_frame, True, False)

            sprite_rect = current_frame.get_rect(center=center)
            self.screen.blit(current_frame, sprite_rect)

            self._draw_player_aim_line(player, center, direction_x, direction_y)

        self._drop_stale_animation_states(active_player_ids)

    def _choose_player_animation(
        self,
        player: dict[str, object],
        state: PlayerAnimationState,
    ) -> str:
        if not bool(player.get("alive", True)):
            return ANIM_DEATH

        if state.throw_time_remaining_seconds > 0.0:
            return ANIM_THROW

        velocity = self._read_position_dict(player.get("velocity"))
        moving = abs(velocity[0]) > 0.1 or abs(velocity[1]) > 0.1
        if moving:
            return ANIM_WALK

        return ANIM_IDLE

    @staticmethod
    def _advance_animation(
        state: PlayerAnimationState,
        animation_clip: AnimationClip,
        target_animation: str,
        render_dt: float,
    ) -> None:
        frame_count = len(animation_clip.frames)
        if frame_count == 0:
            return

        if target_animation != state.current_animation:
            state.current_animation = target_animation
            state.frame_index = 0
            state.frame_progress_seconds = 0.0
            return

        fps = max(0.01, float(animation_clip.fps))
        frame_duration = 1.0 / fps
        state.frame_progress_seconds += render_dt

        while state.frame_progress_seconds >= frame_duration:
            state.frame_progress_seconds -= frame_duration
            if state.frame_index < frame_count - 1:
                state.frame_index += 1
            elif bool(animation_clip.loop):
                state.frame_index = 0
            else:
                state.frame_index = frame_count - 1
                state.frame_progress_seconds = 0.0
                break

    def _update_throw_state(
        self,
        player: dict[str, object],
        state: PlayerAnimationState,
        render_dt: float,
    ) -> None:
        last_attack_tick = int(player.get("last_attack_tick", -1))
        if last_attack_tick > state.last_attack_tick_seen:
            state.last_attack_tick_seen = last_attack_tick
            character_id = str(
                player.get("character_id", self.settings.default_player_character_id)
            )
            throw_clip = self.character_library.get_animation_clip(character_id, ANIM_THROW)
            if throw_clip is not None:
                state.throw_time_remaining_seconds = max(
                    state.throw_time_remaining_seconds,
                    throw_clip.duration_seconds,
                )

        state.throw_time_remaining_seconds = max(
            0.0,
            state.throw_time_remaining_seconds - render_dt,
        )

    def _draw_player_fallback_circle(
        self,
        player: dict[str, object],
        center: tuple[int, int],
        direction_x: float,
        direction_y: float,
    ) -> None:
        radius = round(float(player.get("radius", self.settings.player_radius)))
        pygame.draw.circle(self.screen, self.settings.player_color, center, radius)
        self._draw_player_aim_line(player, center, direction_x, direction_y)

    def _draw_player_aim_line(
        self,
        player: dict[str, object],
        center: tuple[int, int],
        direction_x: float,
        direction_y: float,
    ) -> None:
        if direction_x == 0.0 and direction_y == 0.0:
            return

        magnitude = (direction_x**2 + direction_y**2) ** 0.5
        aim_distance = float(player.get("radius", self.settings.player_radius)) + 18.0
        end = (
            round(center[0] + (direction_x / magnitude) * aim_distance),
            round(center[1] + (direction_y / magnitude) * aim_distance),
        )
        pygame.draw.line(self.screen, self.settings.player_aim_color, center, end, 3)

    def _drop_stale_animation_states(self, active_player_ids: set[str]) -> None:
        self.player_animation_states = {
            player_id: state
            for player_id, state in self.player_animation_states.items()
            if player_id in active_player_ids
        }

    def _draw_enemies(self, snapshot: WorldSnapshot) -> None:
        for enemy in snapshot.enemies:
            if not isinstance(enemy, dict):
                continue
            center = self.camera.world_to_screen(self._read_position(enemy))
            radius = round(float(enemy.get("radius", self.settings.enemy_radius)))
            pygame.draw.circle(self.screen, self.settings.enemy_color, center, radius)

    def _draw_projectiles(self, snapshot: WorldSnapshot) -> None:
        for projectile in snapshot.projectiles:
            if not isinstance(projectile, dict):
                continue
            center = self.camera.world_to_screen(self._read_position(projectile))
            if self._draw_rock_projectile(projectile, center):
                continue
            radius = round(float(projectile.get("radius", self.settings.projectile_radius)))
            pygame.draw.circle(self.screen, self.settings.projectile_color, center, radius)

    def _draw_coins(self, snapshot: WorldSnapshot) -> None:
        for coin in snapshot.coins:
            if not isinstance(coin, dict):
                continue
            center = self.camera.world_to_screen(self._read_position(coin))
            radius = round(float(coin.get("radius", self.settings.coin_radius)))
            pygame.draw.circle(self.screen, self.settings.coin_color, center, radius)

    def _draw_hud(self, snapshot: WorldSnapshot) -> None:
        local_player = next(
            (
                player
                for player in snapshot.players
                if isinstance(player, dict) and player.get("player_id") == self.local_player_id
            ),
            None,
        )
        if local_player is None:
            local_player = next(
                (player for player in snapshot.players if isinstance(player, dict)),
                None,
            )

        player_health = int(local_player.get("health", 0)) if local_player else 0
        player_coins = int(local_player.get("coins", 0)) if local_player else 0

        difficulty = snapshot.difficulty
        text = (
            f"State: {snapshot.run_state}   "
            f"Tick: {snapshot.tick}   "
            f"HP: {player_health}   "
            f"Run Coins: {player_coins}   "
            f"Enemies: {len(snapshot.enemies)}   "
            f"Spawn Interval: {float(difficulty.get('spawn_interval_seconds', 0.0)):.2f}s   "
            f"Difficulty: {float(difficulty.get('factor', 1.0)):.2f}x"
        )
        hud = self.hud_font.render(text, True, self.settings.hud_color)
        self.screen.blit(hud, (12, 12))

    def _draw_rock_projectile(
        self,
        projectile: dict[str, object],
        center: tuple[int, int],
    ) -> bool:
        if self.rock_sprite_base is None:
            return False

        radius = float(projectile.get("radius", self.settings.projectile_radius))
        target_size = max(6, int(round(radius * 2.2)))

        sprite = self.rock_sprite_base
        if sprite.get_width() != target_size or sprite.get_height() != target_size:
            sprite = pygame.transform.smoothscale(sprite, (target_size, target_size))

        velocity = self._read_position_dict(projectile.get("velocity"))
        speed_sq = velocity[0] ** 2 + velocity[1] ** 2
        if speed_sq > 0.0001:
            angle_degrees = -math.degrees(math.atan2(velocity[1], velocity[0]))
            sprite = pygame.transform.rotozoom(sprite, angle_degrees, 1.0)

        sprite_rect = sprite.get_rect(center=center)
        self.screen.blit(sprite, sprite_rect)
        return True

    @staticmethod
    def _read_position(payload: dict[str, object]) -> tuple[float, float]:
        return Renderer._read_position_dict(payload.get("position"))

    @staticmethod
    def _read_position_dict(payload: object) -> tuple[float, float]:
        if isinstance(payload, dict):
            return (float(payload.get("x", 0.0)), float(payload.get("y", 0.0)))
        return (0.0, 0.0)

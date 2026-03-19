import math
from dataclasses import dataclass
from pathlib import Path

import pygame

from game.active_abilities import ABILITY_GUARDIAN_SPIRIT
from game.core.blessings import BLESSING_DAMAGE_AURA, BLESSING_VFX_DAMAGE_AURA
from game.core.enemy_catalog import get_fallback_enemy_radius
from game.core.snapshot import WorldSnapshot
from game.render.blessings import BlessingSpriteLibrary
from game.render.camera import Camera
from game.render.characters import (
    ANIM_DEATH,
    ANIM_IDLE,
    ANIM_THROW,
    ANIM_WALK,
    AnimationClip,
    CharacterSpriteLibrary,
)
from game.render.effects import WorldEffectPlayer
from game.render.enemies import EnemySpriteLibrary
from game.render.fonts import UIFonts
from game.render.spritesheet import load_image
from game.render.tiles import AshlandGroundLayer
from game.settings import GameSettings
from game.ui.hud import BottomPlayerHUD, TopRunStatsHUD

ROCK_SPRITE_PATH = Path(__file__).resolve().parents[3] / "assets" / "effects" / "Rock.png"
COIN_SPRITE_PATH = Path(__file__).resolve().parents[3] / "assets" / "effects" / "coin.png"
FALLBACK_ENEMY_RADIUS = get_fallback_enemy_radius()
GUARDIAN_SPIRIT_LOOP_VFX = "active_ability.guardian_spirit.loop"


@dataclass(slots=True)
class PlayerAnimationState:
    current_animation: str = ANIM_IDLE
    frame_index: int = 0
    frame_progress_seconds: float = 0.0
    throw_time_remaining_seconds: float = 0.0
    last_attack_tick_seen: int = -1
    facing_left: bool = False


@dataclass(slots=True)
class EnemyAnimationState:
    current_animation: str = ANIM_IDLE
    frame_index: int = 0
    frame_progress_seconds: float = 0.0


@dataclass(slots=True)
class TimedBlessingAnimationState:
    frame_index: int = 0
    frame_progress_seconds: float = 0.0


@dataclass(slots=True)
class ScreenShakeState:
    remaining_seconds: float = 0.0
    duration_seconds: float = 0.0
    amplitude: float = 0.0


@dataclass(slots=True)
class FloatingDamageNumber:
    surface: pygame.Surface
    world_x: float
    world_y: float
    velocity_y: float
    remaining_seconds: float
    total_seconds: float


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
        self.character_library = CharacterSpriteLibrary()
        self.enemy_library = EnemySpriteLibrary()
        self.blessing_library = BlessingSpriteLibrary()
        self.world_effect_player = WorldEffectPlayer()
        self.ground_layer = AshlandGroundLayer()
        self.player_animation_states: dict[str, PlayerAnimationState] = {}
        self.enemy_animation_states: dict[int, EnemyAnimationState] = {}
        self.damage_aura_animation_states: dict[str, TimedBlessingAnimationState] = {}
        self.enemy_effect_animation_states: dict[tuple[int, str], TimedBlessingAnimationState] = {}
        self.projectile_effect_animation_states: dict[
            tuple[int, str], TimedBlessingAnimationState
        ] = {}
        self.guardian_spirit_animation_states: dict[str, TimedBlessingAnimationState] = {}
        self._last_render_time_seconds: float | None = None
        self.rock_sprite_base = load_image(ROCK_SPRITE_PATH)
        self.coin_sprite_base = load_image(COIN_SPRITE_PATH)
        self.damage_number_font = fonts.small
        self.damage_number_surface_cache: dict[
            tuple[str, tuple[int, int, int]], pygame.Surface
        ] = {}
        self.damage_aura_frame_cache: dict[tuple[int, int], pygame.Surface] = {}
        self.floating_damage_numbers: list[FloatingDamageNumber] = []
        self.enemy_hit_flash_timers: dict[int, float] = {}
        self.screen_shake = ScreenShakeState()
        self.bottom_hud = BottomPlayerHUD(
            fonts=fonts,
            local_player_id=local_player_id,
            character_library=self.character_library,
        )
        self.top_hud = TopRunStatsHUD(fonts=fonts)
        self._last_snapshot_tick = -1
        self._last_combat_feedback_event_id_seen = 0

    def set_screen(self, screen: pygame.Surface) -> None:
        self.screen = screen

    def set_fonts(self, fonts: UIFonts) -> None:
        self.damage_number_font = fonts.small
        self.damage_number_surface_cache.clear()
        self.damage_aura_frame_cache.clear()
        self.bottom_hud.set_fonts(fonts)
        self.top_hud.set_fonts(fonts)

    def set_active_map(self, map_id: str) -> None:
        self.ground_layer = AshlandGroundLayer(map_id=map_id)
        self.world_effect_player.clear()
        self.damage_aura_animation_states.clear()
        self.enemy_effect_animation_states.clear()
        self.projectile_effect_animation_states.clear()
        self.guardian_spirit_animation_states.clear()
        self.damage_aura_frame_cache.clear()
        self.floating_damage_numbers.clear()
        self.enemy_hit_flash_timers.clear()
        self.screen_shake = ScreenShakeState()
        self._last_combat_feedback_event_id_seen = 0

    def render(self, snapshot: WorldSnapshot) -> None:
        render_now_seconds = pygame.time.get_ticks() / 1000.0
        if self._last_render_time_seconds is None:
            render_dt = 0.0
        else:
            render_dt = max(0.0, min(0.1, render_now_seconds - self._last_render_time_seconds))
        self._last_render_time_seconds = render_now_seconds
        if snapshot.tick < self._last_snapshot_tick:
            self.world_effect_player.clear()
            self.enemy_effect_animation_states.clear()
            self.projectile_effect_animation_states.clear()
            self.guardian_spirit_animation_states.clear()
            self.damage_aura_frame_cache.clear()
            self.floating_damage_numbers.clear()
            self.enemy_hit_flash_timers.clear()
            self.screen_shake = ScreenShakeState()
            self._last_combat_feedback_event_id_seen = 0
        self._last_snapshot_tick = snapshot.tick
        self.world_effect_player.consume_events(snapshot.vfx_events)
        self._consume_combat_feedback_events(snapshot.combat_feedback_events)
        self._update_feedback_state(render_dt)
        player_positions = self._snapshot_player_positions(snapshot)

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
        base_offset_x = self.camera.offset_x
        base_offset_y = self.camera.offset_y
        shake_x, shake_y = self._current_screen_shake_offset()
        self.camera.offset_x = base_offset_x - shake_x
        self.camera.offset_y = base_offset_y - shake_y

        # TODO: Add resolution-aware world scaling during the planned camera/map rendering rework.
        self.screen.fill(self.settings.background_color)
        if not self._draw_ground_layer(snapshot):
            self._draw_grid()
        self._draw_coins(snapshot)
        self._draw_blessings(snapshot)
        self._draw_enemies(snapshot, render_dt)
        self._draw_projectiles(snapshot, render_dt)
        self._draw_damage_auras(snapshot, render_dt)
        self._draw_players(snapshot, render_dt)
        self._draw_guardian_spirit_effects(snapshot, render_dt)
        self._draw_world_effects(render_dt, player_positions)
        self._draw_damage_numbers()
        self.camera.offset_x = base_offset_x
        self.camera.offset_y = base_offset_y
        self.top_hud.render(self.screen, snapshot)
        self.bottom_hud.render(self.screen, snapshot)

    def _draw_ground_layer(self, snapshot: WorldSnapshot) -> bool:
        world_width = float(snapshot.world.get("width", self.settings.world_width))
        world_height = float(snapshot.world.get("height", self.settings.world_height))
        return self.ground_layer.draw(
            self.screen,
            self.camera,
            world_width=world_width,
            world_height=world_height,
        )

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
                self._draw_player_fallback_circle(player, center)
                continue

            self._advance_animation(animation_state, clip, target_animation, render_dt)
            current_frame = clip.frames[animation_state.frame_index]
            if animation_state.facing_left:
                current_frame = pygame.transform.flip(current_frame, True, False)

            sprite_rect = current_frame.get_rect(center=center)
            self.screen.blit(current_frame, sprite_rect)

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
        state: PlayerAnimationState | EnemyAnimationState,
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
                # Force replay from frame 0 on each real throw event.
                state.current_animation = ""
                state.frame_index = 0
                state.frame_progress_seconds = 0.0
                state.throw_time_remaining_seconds = max(0.0, throw_clip.duration_seconds)

        state.throw_time_remaining_seconds = max(
            0.0,
            state.throw_time_remaining_seconds - render_dt,
        )

    def _draw_player_fallback_circle(
        self,
        player: dict[str, object],
        center: tuple[int, int],
    ) -> None:
        radius = round(float(player.get("radius", self.settings.player_radius)))
        pygame.draw.circle(self.screen, self.settings.player_color, center, radius)

    def _drop_stale_animation_states(self, active_player_ids: set[str]) -> None:
        self.player_animation_states = {
            player_id: state
            for player_id, state in self.player_animation_states.items()
            if player_id in active_player_ids
        }

    def _draw_enemies(self, snapshot: WorldSnapshot, render_dt: float) -> None:
        active_enemy_ids: set[int] = set()
        active_enemy_effect_keys: set[tuple[int, str]] = set()
        tier_order = {
            "normal": 0,
            "elite": 1,
            "boss": 2,
        }
        sorted_enemies = sorted(
            snapshot.enemies,
            key=lambda enemy: (
                tier_order.get(str(enemy.get("tier", "normal")), 0)
                if isinstance(enemy, dict)
                else 0,
                int(enemy.get("entity_id", -1)) if isinstance(enemy, dict) else -1,
            ),
        )
        for enemy in sorted_enemies:
            if not isinstance(enemy, dict):
                continue

            enemy_id = int(enemy.get("entity_id", -1))
            if enemy_id >= 0:
                active_enemy_ids.add(enemy_id)

            center = self.camera.world_to_screen(self._read_position(enemy))
            clip = self.enemy_library.get_idle_clip(
                profile_id=(
                    str(enemy.get("profile_id"))
                    if enemy.get("profile_id") not in (None, "")
                    else None
                ),
                entity_id=enemy_id,
            )
            if clip is None or not clip.frames:
                radius = round(float(enemy.get("radius", FALLBACK_ENEMY_RADIUS)))
                pygame.draw.circle(self.screen, self.settings.enemy_color, center, radius)
                continue

            state = self.enemy_animation_states.setdefault(enemy_id, EnemyAnimationState())
            self._advance_animation(state, clip, ANIM_IDLE, render_dt)
            current_frame = clip.frames[state.frame_index]
            current_frame = self._apply_enemy_hit_flash(enemy_id, current_frame)
            sprite_rect = current_frame.get_rect(center=center)
            self.screen.blit(current_frame, sprite_rect)

            active_effect_id = (
                str(enemy.get("active_ability_vfx_id"))
                if enemy.get("active_ability_vfx_id") not in (None, "")
                else None
            )
            if active_effect_id is None:
                continue

            effect_clip = self.world_effect_player.library.get_clip(active_effect_id)
            if effect_clip is None or not effect_clip.frames:
                continue

            effect_key = (enemy_id, active_effect_id)
            active_enemy_effect_keys.add(effect_key)
            effect_state = self.enemy_effect_animation_states.setdefault(
                effect_key,
                TimedBlessingAnimationState(),
            )
            self._advance_looping_animation(
                effect_state,
                fps=float(effect_clip.fps),
                frame_count=len(effect_clip.frames),
                render_dt=render_dt,
            )

            effect_frame = effect_clip.frames[effect_state.frame_index]
            effect_rect = effect_frame.get_rect(center=center)
            self.screen.blit(effect_frame, effect_rect)

        self.enemy_animation_states = {
            enemy_id: state
            for enemy_id, state in self.enemy_animation_states.items()
            if enemy_id in active_enemy_ids
        }
        self.enemy_effect_animation_states = {
            effect_key: state
            for effect_key, state in self.enemy_effect_animation_states.items()
            if effect_key in active_enemy_effect_keys
        }

    def _draw_projectiles(self, snapshot: WorldSnapshot, render_dt: float) -> None:
        active_projectile_effect_keys: set[tuple[int, str]] = set()
        for projectile in snapshot.projectiles:
            if not isinstance(projectile, dict):
                continue
            projectile_id = int(projectile.get("entity_id", -1))
            center = self.camera.world_to_screen(self._read_position(projectile))

            effect_id = (
                str(projectile.get("projectile_effect_id"))
                if projectile.get("projectile_effect_id") not in (None, "")
                else None
            )
            if effect_id:
                effect_clip = self.world_effect_player.library.get_clip(effect_id)
                if effect_clip is not None and effect_clip.frames and projectile_id >= 0:
                    effect_key = (projectile_id, effect_id)
                    active_projectile_effect_keys.add(effect_key)
                    effect_state = self.projectile_effect_animation_states.setdefault(
                        effect_key,
                        TimedBlessingAnimationState(),
                    )
                    self._advance_looping_animation(
                        effect_state,
                        fps=float(effect_clip.fps),
                        frame_count=len(effect_clip.frames),
                        render_dt=render_dt,
                    )
                    effect_frame = effect_clip.frames[effect_state.frame_index]
                    effect_rect = effect_frame.get_rect(center=center)
                    self.screen.blit(effect_frame, effect_rect)

            if self._draw_rock_projectile(projectile, center):
                continue
            radius = round(float(projectile.get("radius", self.settings.projectile_radius)))
            pygame.draw.circle(self.screen, self.settings.projectile_color, center, radius)

        self.projectile_effect_animation_states = {
            effect_key: state
            for effect_key, state in self.projectile_effect_animation_states.items()
            if effect_key in active_projectile_effect_keys
        }

    def _draw_coins(self, snapshot: WorldSnapshot) -> None:
        for coin in snapshot.coins:
            if not isinstance(coin, dict):
                continue
            center = self.camera.world_to_screen(self._read_position(coin))
            if self._draw_coin_sprite(coin, center):
                continue
            radius = round(float(coin.get("radius", self.settings.coin_radius)))
            pygame.draw.circle(self.screen, self.settings.coin_color, center, radius)

    def _draw_blessings(self, snapshot: WorldSnapshot) -> None:
        for blessing in snapshot.blessings:
            if not isinstance(blessing, dict):
                continue
            center = self.camera.world_to_screen(self._read_position(blessing))
            if self._draw_blessing_sprite(blessing, center):
                continue
            radius = round(float(blessing.get("radius", 9.0)))
            self._draw_blessing_fallback(center, radius)

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

    def _draw_coin_sprite(self, coin: dict[str, object], center: tuple[int, int]) -> bool:
        if self.coin_sprite_base is None:
            return False

        radius = float(coin.get("radius", self.settings.coin_radius))
        target_size = max(8, int(round(radius * 2.6)))
        sprite = self.coin_sprite_base
        if sprite.get_width() != target_size or sprite.get_height() != target_size:
            sprite = pygame.transform.scale(sprite, (target_size, target_size))

        sprite_rect = sprite.get_rect(center=center)
        self.screen.blit(sprite, sprite_rect)
        return True

    def _draw_blessing_sprite(
        self,
        blessing: dict[str, object],
        center: tuple[int, int],
    ) -> bool:
        blessing_id = str(blessing.get("blessing_id", ""))
        if not blessing_id:
            return False

        sprite = self.blessing_library.get_icon(blessing_id)
        if sprite is None:
            return False

        sprite_rect = sprite.get_rect(center=center)
        self.screen.blit(sprite, sprite_rect)
        return True

    def _draw_damage_auras(self, snapshot: WorldSnapshot, render_dt: float) -> None:
        aura_clip = self.world_effect_player.library.get_clip(BLESSING_VFX_DAMAGE_AURA)
        if aura_clip is None or not aura_clip.frames:
            self.damage_aura_animation_states.clear()
            return

        player_positions: dict[str, tuple[float, float]] = {}
        for player in snapshot.players:
            if not isinstance(player, dict):
                continue

            player_id = str(player.get("player_id", ""))
            if not player_id or not bool(player.get("alive", True)):
                continue
            player_positions[player_id] = self._read_position(player)

        active_player_ids: set[str] = set()
        for blessing in snapshot.active_blessings:
            if not isinstance(blessing, dict):
                continue
            if str(blessing.get("blessing_id", "")) != BLESSING_DAMAGE_AURA:
                continue

            player_id = str(blessing.get("player_id", ""))
            if not player_id:
                continue
            position = player_positions.get(player_id)
            if position is None:
                continue

            active_player_ids.add(player_id)
            state = self.damage_aura_animation_states.setdefault(
                player_id,
                TimedBlessingAnimationState(),
            )
            self._advance_looping_animation(
                state,
                fps=float(aura_clip.fps),
                frame_count=len(aura_clip.frames),
                render_dt=render_dt,
            )

            frame = aura_clip.frames[state.frame_index]
            aura_radius = float(blessing.get("radius", self.settings.damage_aura_radius))
            frame = self._scaled_damage_aura_frame(frame, aura_radius)
            frame_rect = frame.get_rect(center=self.camera.world_to_screen(position))
            self.screen.blit(frame, frame_rect)

        self.damage_aura_animation_states = {
            player_id: state
            for player_id, state in self.damage_aura_animation_states.items()
            if player_id in active_player_ids
        }

    def _draw_world_effects(
        self,
        render_dt: float,
        player_positions: dict[str, tuple[float, float]],
    ) -> None:
        self.world_effect_player.update_and_draw(
            self.screen,
            self.camera,
            render_dt,
            player_positions=player_positions,
        )

    def _draw_guardian_spirit_effects(self, snapshot: WorldSnapshot, render_dt: float) -> None:
        clip = self.world_effect_player.library.get_clip(GUARDIAN_SPIRIT_LOOP_VFX)
        if clip is None or not clip.frames:
            self.guardian_spirit_animation_states.clear()
            return

        active_player_ids: set[str] = set()
        for player in snapshot.players:
            if not isinstance(player, dict) or not bool(player.get("alive", True)):
                continue
            player_id = str(player.get("player_id", ""))
            if not player_id:
                continue

            active_ability = player.get("active_ability")
            if not isinstance(active_ability, dict):
                continue
            if str(active_ability.get("ability_id", "")) != ABILITY_GUARDIAN_SPIRIT:
                continue

            active_remaining = float(active_ability.get("active_remaining_seconds", 0.0))
            if active_remaining <= 0.0:
                continue

            active_player_ids.add(player_id)
            state = self.guardian_spirit_animation_states.setdefault(
                player_id,
                TimedBlessingAnimationState(),
            )
            self._advance_looping_animation(
                state,
                fps=float(clip.fps),
                frame_count=len(clip.frames),
                render_dt=render_dt,
            )

            frame = clip.frames[state.frame_index]
            center = self.camera.world_to_screen(self._read_position(player))
            frame_rect = frame.get_rect(center=center)
            self.screen.blit(frame, frame_rect)

        self.guardian_spirit_animation_states = {
            player_id: state
            for player_id, state in self.guardian_spirit_animation_states.items()
            if player_id in active_player_ids
        }

    def _consume_combat_feedback_events(self, events: list[dict[str, object]]) -> None:
        for event in events:
            if not isinstance(event, dict):
                continue
            event_id = int(event.get("event_id", 0))
            if event_id <= self._last_combat_feedback_event_id_seen:
                continue
            self._last_combat_feedback_event_id_seen = event_id
            event_type = str(event.get("type", ""))
            if event_type == "enemy_hit":
                enemy_id = int(event.get("enemy_id", -1))
                if enemy_id >= 0:
                    self.enemy_hit_flash_timers[enemy_id] = max(
                        self.enemy_hit_flash_timers.get(enemy_id, 0.0),
                        0.08,
                    )
                position = self._read_position_dict(event.get("position"))
                damage = max(0, int(event.get("damage", 0)))
                if damage > 0:
                    self._spawn_damage_number(position, damage)
            elif event_type == "player_hit":
                damage = max(0.0, float(event.get("damage", 0.0)))
                max_health = max(1.0, float(event.get("max_health", 1.0)))
                damage_fraction = max(0.0, min(1.0, damage / max_health))
                amplitude = 4.0 + (damage_fraction * 16.0)
                duration_seconds = 0.10 + (damage_fraction * 0.14)
                self._trigger_screen_shake(
                    duration_seconds=duration_seconds,
                    amplitude=amplitude,
                )

    def _update_feedback_state(self, render_dt: float) -> None:
        self.enemy_hit_flash_timers = {
            enemy_id: max(0.0, timer - render_dt)
            for enemy_id, timer in self.enemy_hit_flash_timers.items()
            if timer - render_dt > 0.0
        }
        if self.screen_shake.remaining_seconds > 0.0:
            self.screen_shake.remaining_seconds = max(
                0.0,
                self.screen_shake.remaining_seconds - render_dt,
            )

        kept_numbers: list[FloatingDamageNumber] = []
        for number in self.floating_damage_numbers:
            number.remaining_seconds = max(0.0, number.remaining_seconds - render_dt)
            if number.remaining_seconds <= 0.0:
                continue
            number.world_y += number.velocity_y * render_dt
            kept_numbers.append(number)
        self.floating_damage_numbers = kept_numbers

    def _trigger_screen_shake(self, *, duration_seconds: float, amplitude: float) -> None:
        if self.screen_shake.remaining_seconds > 0.0:
            self.screen_shake.remaining_seconds = max(
                self.screen_shake.remaining_seconds,
                float(duration_seconds),
            )
            self.screen_shake.duration_seconds = max(
                self.screen_shake.duration_seconds,
                float(duration_seconds),
            )
            self.screen_shake.amplitude = max(self.screen_shake.amplitude, float(amplitude))
            return

        self.screen_shake = ScreenShakeState(
            remaining_seconds=float(duration_seconds),
            duration_seconds=float(duration_seconds),
            amplitude=float(amplitude),
        )

    def _current_screen_shake_offset(self) -> tuple[float, float]:
        if self.screen_shake.remaining_seconds <= 0.0 or self.screen_shake.duration_seconds <= 0.0:
            return (0.0, 0.0)

        progress = self.screen_shake.remaining_seconds / self.screen_shake.duration_seconds
        amplitude = self.screen_shake.amplitude * max(0.0, min(1.0, progress))
        phase = pygame.time.get_ticks() / 1000.0
        shake_x = math.sin(phase * 92.0) * amplitude
        shake_y = math.cos(phase * 71.0) * amplitude * 0.7
        return (shake_x, shake_y)

    def _spawn_damage_number(self, position: tuple[float, float], damage: int) -> None:
        if len(self.floating_damage_numbers) >= 48:
            self.floating_damage_numbers.pop(0)

        surface = self._damage_number_surface(str(damage), (245, 245, 245)).copy()
        self.floating_damage_numbers.append(
            FloatingDamageNumber(
                surface=surface,
                world_x=float(position[0]),
                world_y=float(position[1]) - 18.0,
                velocity_y=-28.0,
                remaining_seconds=0.7,
                total_seconds=0.7,
            )
        )

    def _draw_damage_numbers(self) -> None:
        for number in self.floating_damage_numbers:
            alpha = int(
                round(
                    255.0
                    * max(0.0, min(1.0, number.remaining_seconds / max(0.01, number.total_seconds)))
                )
            )
            number.surface.set_alpha(alpha)
            center = self.camera.world_to_screen((number.world_x, number.world_y))
            rect = number.surface.get_rect(center=center)
            self.screen.blit(number.surface, rect)

    def _scaled_damage_aura_frame(
        self,
        frame: pygame.Surface,
        aura_radius: float,
    ) -> pygame.Surface:
        target_diameter = max(24, int(round(max(1.0, aura_radius) * 2.4)))
        cache_key = (id(frame), target_diameter)
        cached = self.damage_aura_frame_cache.get(cache_key)
        if cached is not None:
            return cached

        if frame.get_width() == target_diameter and frame.get_height() == target_diameter:
            self.damage_aura_frame_cache[cache_key] = frame
            return frame

        scaled = pygame.transform.scale(frame, (target_diameter, target_diameter))
        self.damage_aura_frame_cache[cache_key] = scaled
        return scaled

    def _damage_number_surface(
        self,
        text: str,
        color: tuple[int, int, int],
    ) -> pygame.Surface:
        cache_key = (text, color)
        cached = self.damage_number_surface_cache.get(cache_key)
        if cached is not None:
            return cached

        rendered = self.damage_number_font.render(text, True, color)
        self.damage_number_surface_cache[cache_key] = rendered
        return rendered

    def _apply_enemy_hit_flash(
        self,
        enemy_id: int,
        frame: pygame.Surface,
    ) -> pygame.Surface:
        remaining = self.enemy_hit_flash_timers.get(enemy_id, 0.0)
        if remaining <= 0.0:
            return frame

        flashed = frame.copy()
        intensity = max(90, min(180, int(round((remaining / 0.08) * 180.0))))
        flashed.fill((intensity, intensity, intensity), special_flags=pygame.BLEND_RGB_ADD)
        return flashed

    def _draw_blessing_fallback(self, center: tuple[int, int], radius: int) -> None:
        pygame.draw.circle(self.screen, (136, 214, 255), center, radius)
        pygame.draw.circle(self.screen, (44, 100, 138), center, radius, width=2)

    @staticmethod
    def _snapshot_player_positions(snapshot: WorldSnapshot) -> dict[str, tuple[float, float]]:
        positions: dict[str, tuple[float, float]] = {}
        for player in snapshot.players:
            if not isinstance(player, dict):
                continue
            player_id = str(player.get("player_id", ""))
            if not player_id or not bool(player.get("alive", True)):
                continue
            positions[player_id] = Renderer._read_position(player)
        return positions

    @staticmethod
    def _read_position(payload: dict[str, object]) -> tuple[float, float]:
        return Renderer._read_position_dict(payload.get("position"))

    @staticmethod
    def _read_position_dict(payload: object) -> tuple[float, float]:
        if isinstance(payload, dict):
            return (float(payload.get("x", 0.0)), float(payload.get("y", 0.0)))
        return (0.0, 0.0)

    @staticmethod
    def _advance_looping_animation(
        state: TimedBlessingAnimationState,
        *,
        fps: float,
        frame_count: int,
        render_dt: float,
    ) -> None:
        if frame_count <= 0:
            return

        frame_duration = 1.0 / max(0.01, fps)
        state.frame_progress_seconds += max(0.0, render_dt)
        while state.frame_progress_seconds >= frame_duration:
            state.frame_progress_seconds -= frame_duration
            state.frame_index = (state.frame_index + 1) % frame_count

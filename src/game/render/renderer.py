import pygame

from game.core.snapshot import WorldSnapshot
from game.render.camera import Camera
from game.settings import GameSettings


class Renderer:
    def __init__(
        self,
        screen: pygame.Surface,
        camera: Camera,
        settings: GameSettings,
        local_player_id: str,
    ) -> None:
        self.screen = screen
        self.camera = camera
        self.settings = settings
        self.local_player_id = local_player_id
        self.font = pygame.font.Font(None, 24)

    def set_screen(self, screen: pygame.Surface) -> None:
        self.screen = screen

    def render(self, snapshot: WorldSnapshot) -> None:
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
        self._draw_players(snapshot)
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

    def _draw_players(self, snapshot: WorldSnapshot) -> None:
        for player in snapshot.players:
            if not isinstance(player, dict) or not bool(player.get("alive", True)):
                continue

            center = self.camera.world_to_screen(self._read_position(player))
            radius = round(float(player.get("radius", self.settings.player_radius)))
            pygame.draw.circle(self.screen, self.settings.player_color, center, radius)

            aim_position = self._read_position_dict(player.get("aim_position"))
            direction_x = aim_position[0] - self._read_position(player)[0]
            direction_y = aim_position[1] - self._read_position(player)[1]
            if direction_x == 0.0 and direction_y == 0.0:
                continue

            magnitude = (direction_x**2 + direction_y**2) ** 0.5
            aim_distance = float(player.get("radius", self.settings.player_radius)) + 18.0
            end = (
                round(center[0] + (direction_x / magnitude) * aim_distance),
                round(center[1] + (direction_y / magnitude) * aim_distance),
            )
            pygame.draw.line(self.screen, self.settings.player_aim_color, center, end, 3)

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
        hud = self.font.render(text, True, self.settings.hud_color)
        self.screen.blit(hud, (12, 12))

    @staticmethod
    def _read_position(payload: dict[str, object]) -> tuple[float, float]:
        return Renderer._read_position_dict(payload.get("position"))

    @staticmethod
    def _read_position_dict(payload: object) -> tuple[float, float]:
        if isinstance(payload, dict):
            return (float(payload.get("x", 0.0)), float(payload.get("y", 0.0)))
        return (0.0, 0.0)

from __future__ import annotations

from pathlib import Path

import pygame

from game.core.snapshot import WorldSnapshot
from game.render.characters import CharacterSpriteLibrary
from game.render.fonts import UIFonts
from game.render.spritesheet import load_image, load_pixelart_image

ROCK_ICON_PATH = Path(__file__).resolve().parents[3] / "assets" / "effects" / "Rock1.png"
COIN_ICON_PATH = Path(__file__).resolve().parents[3] / "assets" / "effects" / "coin.png"
HUD_ROCK_ICON_PIXEL_SCALE = 4


class BottomPlayerHUD:
    def __init__(
        self,
        fonts: UIFonts,
        local_player_id: str,
        character_library: CharacterSpriteLibrary,
    ) -> None:
        self.local_player_id = local_player_id
        self.character_library = character_library
        self.label_font = fonts.hud
        self.value_font = fonts.small
        self._coin_icon_size = 32
        self._portrait_size = 62
        self._portrait_cache: dict[str, pygame.Surface] = {}

        self.rock_icon_hud = load_pixelart_image(
            ROCK_ICON_PATH,
            scale_multiple=HUD_ROCK_ICON_PIXEL_SCALE,
        )
        coin_icon = load_image(COIN_ICON_PATH)
        self.coin_icon = (
            pygame.transform.smoothscale(coin_icon, (self._coin_icon_size, self._coin_icon_size))
            if coin_icon is not None
            else None
        )

    def render(self, surface: pygame.Surface, snapshot: WorldSnapshot) -> None:
        player = self._resolve_player(snapshot)
        if player is None:
            return

        panel_rect = self._panel_rect(surface)
        pygame.draw.rect(surface, (16, 18, 22), panel_rect, border_radius=12)
        pygame.draw.rect(surface, (86, 96, 110), panel_rect, width=2, border_radius=10)

        padding = 14
        gap = 12
        content_rect = panel_rect.inflate(-padding * 2, -padding * 2)
        block_height = content_rect.height

        portrait_width = 82
        cooldown_width = 96
        coin_width = 138
        hp_width = max(
            160,
            min(
                260,
                content_rect.width - portrait_width - cooldown_width - coin_width - gap * 3,
            ),
        )

        x = content_rect.left
        x = self._draw_portrait(
            surface, player, pygame.Rect(x, content_rect.top, portrait_width, block_height)
        )
        x += gap
        x = self._draw_health_bar(
            surface, pygame.Rect(x, content_rect.top, hp_width, block_height), player
        )
        x += gap
        x = self._draw_throw_cooldown(
            surface,
            pygame.Rect(x, content_rect.top, cooldown_width, block_height),
            player,
        )
        x += gap
        self._draw_coin_counter(
            surface, pygame.Rect(x, content_rect.top, coin_width, block_height), player, snapshot
        )

    def _resolve_player(self, snapshot: WorldSnapshot) -> dict[str, object] | None:
        local_player = next(
            (
                player
                for player in snapshot.players
                if isinstance(player, dict) and player.get("player_id") == self.local_player_id
            ),
            None,
        )
        if local_player is not None:
            return local_player

        return next((player for player in snapshot.players if isinstance(player, dict)), None)

    @staticmethod
    def _panel_rect(surface: pygame.Surface) -> pygame.Rect:
        screen_width, screen_height = surface.get_size()
        margin = 14
        height = 100
        width = min(860, screen_width - margin * 2)
        return pygame.Rect(
            (screen_width - width) // 2,
            screen_height - height - margin,
            width,
            height,
        )

    def _draw_portrait(
        self,
        surface: pygame.Surface,
        player: dict[str, object],
        block_rect: pygame.Rect,
    ) -> int:
        pygame.draw.rect(surface, (30, 34, 40), block_rect, border_radius=8)
        pygame.draw.rect(surface, (95, 102, 118), block_rect, width=2, border_radius=8)

        character_id = str(player.get("character_id", self.character_library.default_character_id))
        portrait = self._get_portrait(character_id)
        portrait_rect = pygame.Rect(0, 0, self._portrait_size, self._portrait_size)
        portrait_rect.center = block_rect.center
        if portrait is not None:
            surface.blit(portrait, portrait_rect)
        else:
            pygame.draw.circle(
                surface, (98, 118, 150), portrait_rect.center, self._portrait_size // 2 - 2
            )
            pygame.draw.circle(
                surface,
                (48, 58, 76),
                portrait_rect.center,
                self._portrait_size // 2 - 2,
                width=2,
            )

        return block_rect.right

    def _draw_health_bar(
        self,
        surface: pygame.Surface,
        block_rect: pygame.Rect,
        player: dict[str, object],
    ) -> int:
        pygame.draw.rect(surface, (26, 30, 36), block_rect, border_radius=8)
        pygame.draw.rect(surface, (95, 102, 118), block_rect, width=2, border_radius=8)

        label = self.label_font.render("HP", True, (228, 230, 235))
        label_rect = label.get_rect(topleft=(block_rect.left + 10, block_rect.top + 9))
        surface.blit(label, label_rect)

        health = max(0.0, float(player.get("health", 0.0)))
        max_health = max(1.0, float(player.get("max_health", 1.0)))
        ratio = max(0.0, min(1.0, health / max_health))

        bar_rect = pygame.Rect(
            block_rect.left + 10,
            block_rect.top + 38,
            max(128, block_rect.width - 20),
            20,
        )
        pygame.draw.rect(surface, (46, 50, 60), bar_rect, border_radius=6)
        pygame.draw.rect(surface, (95, 102, 118), bar_rect, width=2, border_radius=6)

        if ratio > 0.0:
            fill_width = max(1, int(round((bar_rect.width - 4) * ratio)))
            fill_rect = pygame.Rect(
                bar_rect.left + 2,
                bar_rect.top + 2,
                fill_width,
                bar_rect.height - 4,
            )
            fill_color = self._health_color(ratio)
            pygame.draw.rect(surface, fill_color, fill_rect, border_radius=5)

        value_text = self.value_font.render(
            f"{int(round(health))} / {int(round(max_health))}",
            True,
            (246, 246, 246),
        )
        value_rect = value_text.get_rect(
            midleft=(block_rect.left + 10, block_rect.bottom - 10),
        )
        surface.blit(value_text, value_rect)
        return block_rect.right

    def _draw_throw_cooldown(
        self,
        surface: pygame.Surface,
        block_rect: pygame.Rect,
        player: dict[str, object],
    ) -> int:
        pygame.draw.rect(surface, (26, 30, 36), block_rect, border_radius=8)
        pygame.draw.rect(surface, (95, 102, 118), block_rect, width=2, border_radius=8)

        icon_size = self.rock_icon_hud.get_height() if self.rock_icon_hud is not None else 32
        icon_rect = pygame.Rect(0, 0, icon_size, icon_size)
        icon_rect.center = block_rect.center

        if self.rock_icon_hud is not None:
            surface.blit(self.rock_icon_hud, icon_rect)
        else:
            pygame.draw.circle(surface, (188, 156, 114), icon_rect.center, icon_size // 2)
            pygame.draw.circle(
                surface,
                (74, 66, 58),
                icon_rect.center,
                icon_size // 2,
                width=2,
            )

        cooldown_total = max(0.0001, float(player.get("throw_cooldown_seconds", 0.0)))
        cooldown_remaining = max(0.0, float(player.get("throw_cooldown_remaining", 0.0)))
        cooldown_ratio = max(0.0, min(1.0, cooldown_remaining / cooldown_total))

        if cooldown_ratio > 0.0:
            overlay_height = max(1, int(round(icon_rect.height * cooldown_ratio)))
            cooldown_overlay = pygame.Surface((icon_rect.width, overlay_height), pygame.SRCALPHA)
            cooldown_overlay.fill((12, 16, 22, 160))
            surface.blit(cooldown_overlay, (icon_rect.left, icon_rect.top))

        pygame.draw.rect(surface, (95, 102, 118), icon_rect, width=2, border_radius=6)
        return block_rect.right

    def _draw_coin_counter(
        self,
        surface: pygame.Surface,
        block_rect: pygame.Rect,
        player: dict[str, object],
        snapshot: WorldSnapshot,
    ) -> None:
        pygame.draw.rect(surface, (26, 30, 36), block_rect, border_radius=8)
        pygame.draw.rect(surface, (95, 102, 118), block_rect, width=2, border_radius=8)

        title = self.label_font.render("Coins", True, (228, 230, 235))
        surface.blit(title, title.get_rect(topleft=(block_rect.left + 10, block_rect.top + 10)))

        icon_rect = pygame.Rect(0, 0, self._coin_icon_size, self._coin_icon_size)
        icon_rect.bottomleft = (block_rect.left + 10, block_rect.bottom - 10)
        if self.coin_icon is not None:
            surface.blit(self.coin_icon, icon_rect)
        else:
            pygame.draw.circle(surface, (230, 190, 60), icon_rect.center, self._coin_icon_size // 2)
            pygame.draw.circle(
                surface,
                (120, 95, 34),
                icon_rect.center,
                self._coin_icon_size // 2,
                width=2,
            )

        run_coins = self._read_player_run_coins(player, snapshot)
        value = self.value_font.render(str(run_coins), True, (245, 245, 245))
        value_rect = value.get_rect(midleft=(icon_rect.right + 8, icon_rect.centery))
        surface.blit(value, value_rect)

    def _get_portrait(self, character_id: str) -> pygame.Surface | None:
        if character_id in self._portrait_cache:
            return self._portrait_cache[character_id]

        character_assets = self.character_library.get_character(character_id)
        portrait = character_assets.portrait if character_assets is not None else None
        if portrait is None:
            return None

        scaled = pygame.transform.smoothscale(
            portrait,
            (self._portrait_size, self._portrait_size),
        )
        self._portrait_cache[character_id] = scaled
        return scaled

    def _read_player_run_coins(
        self,
        player: dict[str, object],
        snapshot: WorldSnapshot,
    ) -> int:
        player_coins = player.get("coins")
        if isinstance(player_coins, int):
            return max(0, player_coins)

        score_coins = snapshot.score.get("run_coins_by_player")
        if isinstance(score_coins, dict):
            value = score_coins.get(self.local_player_id, 0)
            try:
                return max(0, int(value))
            except (TypeError, ValueError):
                return 0
        return 0

    @staticmethod
    def _health_color(ratio: float) -> tuple[int, int, int]:
        if ratio >= 0.65:
            return (86, 212, 126)
        if ratio >= 0.35:
            return (236, 190, 78)
        return (230, 90, 90)

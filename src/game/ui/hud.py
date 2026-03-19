from __future__ import annotations

from dataclasses import fields as dataclass_fields
from pathlib import Path

import pygame

from game.core.blessings import (
    BlessingCategory,
    BlessingDefinition,
    RunBoonModifier,
    list_blessings,
)
from game.core.snapshot import WorldSnapshot
from game.render.blessings import BlessingSpriteLibrary
from game.render.characters import CharacterSpriteLibrary
from game.render.fonts import UIFonts
from game.render.spritesheet import load_image, load_pixelart_image

ROCK_ICON_PATH = Path(__file__).resolve().parents[3] / "assets" / "effects" / "Rock.png"
COIN_ICON_PATH = Path(__file__).resolve().parents[3] / "assets" / "effects" / "coin.png"
HUD_ROCK_ICON_PIXEL_SCALE = 4
HUD_PANEL_FILL_ALPHA = 208
HUD_BOON_PANEL_FILL_ALPHA = 224


def _draw_panel(
    surface: pygame.Surface,
    rect: pygame.Rect,
    *,
    fill_color: tuple[int, int, int],
    border_color: tuple[int, int, int],
    border_radius: int,
    fill_alpha: int = 255,
    border_width: int = 2,
) -> None:
    if fill_alpha >= 255:
        pygame.draw.rect(surface, fill_color, rect, border_radius=border_radius)
    else:
        panel_surface = pygame.Surface(rect.size, pygame.SRCALPHA)
        pygame.draw.rect(
            panel_surface,
            (*fill_color, max(0, min(255, fill_alpha))),
            panel_surface.get_rect(),
            border_radius=border_radius,
        )
        surface.blit(panel_surface, rect.topleft)
    pygame.draw.rect(
        surface,
        border_color,
        rect,
        width=border_width,
        border_radius=border_radius,
    )


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
        self.blessing_library = BlessingSpriteLibrary(world_icon_scale=1)
        self._coin_icon_size = 32
        self._portrait_size = 62
        self._portrait_cache: dict[str, pygame.Surface] = {}
        self._run_boon_bindings = self._build_run_boon_bindings()

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

    def set_fonts(self, fonts: UIFonts) -> None:
        self.label_font = fonts.hud
        self.value_font = fonts.small

    def render(self, surface: pygame.Surface, snapshot: WorldSnapshot) -> None:
        player = self._resolve_player(snapshot)
        if player is None:
            return

        panel_rect = self._panel_rect(surface)
        self._draw_active_run_boons(surface, player, panel_rect)
        _draw_panel(
            surface,
            panel_rect,
            fill_color=(16, 18, 22),
            border_color=(86, 96, 110),
            border_radius=12,
            fill_alpha=HUD_PANEL_FILL_ALPHA,
        )

        padding = 14
        gap = 12
        content_rect = panel_rect.inflate(-padding * 2, -padding * 2)
        block_height = content_rect.height

        (
            show_portrait,
            portrait_width,
            hp_width,
            cooldown_width,
            ability_width,
            coin_width,
        ) = self._block_widths(
            content_rect.width,
            gap,
        )
        x = content_rect.left
        if show_portrait:
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
        x = self._draw_ability_cooldown(
            surface,
            pygame.Rect(x, content_rect.top, ability_width, block_height),
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
        height = max(82, min(104, screen_height // 6))
        width = min(860, screen_width - margin * 2)
        return pygame.Rect(
            (screen_width - width) // 2,
            screen_height - height - margin,
            width,
            height,
        )

    @staticmethod
    def _block_widths(content_width: int, gap: int) -> tuple[bool, int, int, int, int, int]:
        full_min = 78 + 120 + 72 + 118 + 96 + (gap * 4)
        compact_min = 110 + 60 + 92 + 84 + (gap * 3)

        if content_width >= full_min:
            usable = content_width - (gap * 4)
            portrait = max(72, min(92, int(usable * 0.16)))
            cooldown = max(72, min(108, int(usable * 0.17)))
            ability = max(100, min(156, int(usable * 0.24)))
            coin = max(88, min(160, int(usable * 0.18)))
            hp = usable - portrait - cooldown - ability - coin
            if hp < 120:
                deficit = 120 - hp
                shift_from_ability = min(deficit, max(0, ability - 90))
                ability -= shift_from_ability
                hp += shift_from_ability
                deficit -= shift_from_ability
                shift_from_coin = min(deficit, max(0, coin - 84))
                coin -= shift_from_coin
                hp += shift_from_coin
            return True, portrait, hp, cooldown, ability, coin

        if content_width >= compact_min:
            usable = content_width - (gap * 3)
            cooldown = max(58, min(94, int(usable * 0.18)))
            ability = max(82, min(130, int(usable * 0.28)))
            coin = max(76, min(140, int(usable * 0.26)))
            hp = usable - cooldown - ability - coin
            if hp < 110:
                deficit = 110 - hp
                shift_from_coin = min(deficit, max(0, coin - 72))
                coin -= shift_from_coin
                hp += shift_from_coin
                deficit -= shift_from_coin
                if deficit > 0:
                    shift_from_ability = min(deficit, max(0, ability - 74))
                    ability -= shift_from_ability
                    hp += shift_from_ability
                    deficit -= shift_from_ability
                if deficit > 0:
                    shift_from_cooldown = min(deficit, max(0, cooldown - 54))
                    cooldown -= shift_from_cooldown
                    hp += shift_from_cooldown
            return False, 0, hp, cooldown, ability, coin

        # Extremely narrow fallback: keep all blocks visible with reduced widths.
        usable = max(160, content_width - (gap * 3))
        cooldown = max(54, int(usable * 0.18))
        ability = max(78, int(usable * 0.30))
        coin = max(68, int(usable * 0.22))
        hp = max(72, usable - cooldown - ability - coin)
        return False, 0, hp, cooldown, ability, coin

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

    def _draw_active_run_boons(
        self,
        surface: pygame.Surface,
        player: dict[str, object],
        hud_panel_rect: pygame.Rect,
    ) -> None:
        active_boons = self._active_run_boons(player)
        if not active_boons:
            return

        icon_size, icon_gap = self._boon_icon_layout(hud_panel_rect.width, len(active_boons))
        padding = max(8, icon_gap)
        panel_width = (len(active_boons) * icon_size) + (max(0, len(active_boons) - 1) * icon_gap)
        panel_rect = pygame.Rect(0, 0, panel_width + padding * 2, icon_size + padding * 2)
        panel_rect.centerx = hud_panel_rect.centerx
        panel_rect.bottom = hud_panel_rect.top - 10

        _draw_panel(
            surface,
            panel_rect,
            fill_color=(20, 24, 30),
            border_color=(86, 96, 110),
            border_radius=10,
            fill_alpha=HUD_BOON_PANEL_FILL_ALPHA,
        )

        mouse_pos = pygame.mouse.get_pos()
        hovered_name: str | None = None
        x = panel_rect.left + padding
        icon_y = panel_rect.top + padding
        for definition, stack_count in active_boons:
            icon_rect = pygame.Rect(x, icon_y, icon_size, icon_size)
            self._draw_boon_icon(surface, icon_rect, definition, stack_count)
            if icon_rect.collidepoint(mouse_pos):
                hovered_name = definition.display_name
            x += icon_size + icon_gap

        if hovered_name is not None:
            self._draw_boon_tooltip(surface, hovered_name, mouse_pos, panel_rect)

    def _draw_boon_icon(
        self,
        surface: pygame.Surface,
        icon_rect: pygame.Rect,
        definition: BlessingDefinition,
        stack_count: int,
    ) -> None:
        pygame.draw.rect(surface, (32, 36, 42), icon_rect, border_radius=8)
        pygame.draw.rect(surface, (96, 104, 120), icon_rect, width=2, border_radius=8)

        icon_padding = max(3, icon_rect.width // 10)
        icon_target_rect = icon_rect.inflate(-icon_padding * 2, -icon_padding * 2)
        icon = self._get_boon_icon(definition.blessing_id, icon_target_rect.size)
        if icon is not None:
            icon_draw_rect = icon.get_rect(center=icon_target_rect.center)
            surface.blit(icon, icon_draw_rect)
        else:
            pygame.draw.circle(surface, (98, 112, 138), icon_rect.center, icon_rect.width // 3)

        badge_text = self.value_font.render(str(stack_count), True, (250, 250, 252))
        badge_padding_x = 6
        badge_rect = pygame.Rect(
            0,
            0,
            max(18, badge_text.get_width() + badge_padding_x * 2),
            max(18, badge_text.get_height() + 4),
        )
        badge_rect.topright = (icon_rect.right - 2, icon_rect.top + 2)
        pygame.draw.rect(surface, (18, 22, 28), badge_rect, border_radius=8)
        pygame.draw.rect(surface, (222, 226, 235), badge_rect, width=1, border_radius=8)
        surface.blit(badge_text, badge_text.get_rect(center=badge_rect.center))

    def _draw_boon_tooltip(
        self,
        surface: pygame.Surface,
        boon_name: str,
        mouse_pos: tuple[int, int],
        anchor_rect: pygame.Rect,
    ) -> None:
        tooltip_text = self.value_font.render(boon_name, True, (244, 246, 250))
        padding_x = 10
        padding_y = 7
        tooltip_rect = pygame.Rect(
            0,
            0,
            tooltip_text.get_width() + padding_x * 2,
            tooltip_text.get_height() + padding_y * 2,
        )
        tooltip_rect.midbottom = (mouse_pos[0], anchor_rect.top - 6)
        tooltip_rect.clamp_ip(surface.get_rect().inflate(-8, -8))

        _draw_panel(
            surface,
            tooltip_rect,
            fill_color=(18, 20, 26),
            border_color=(106, 114, 130),
            border_radius=8,
            fill_alpha=236,
            border_width=1,
        )
        surface.blit(tooltip_text, tooltip_text.get_rect(center=tooltip_rect.center))

    def _active_run_boons(
        self,
        player: dict[str, object],
    ) -> list[tuple[BlessingDefinition, int]]:
        active: list[tuple[BlessingDefinition, int]] = []
        for definition, stack_field in self._run_boon_bindings:
            stack_count = self._read_int(player.get(stack_field), default=0)
            if stack_count > 0:
                active.append((definition, stack_count))
        return active

    def _get_boon_icon(
        self,
        blessing_id: str,
        target_size: tuple[int, int],
    ) -> pygame.Surface | None:
        base_icon = self.blessing_library.get_icon(blessing_id, scale_multiple=1)
        if base_icon is None:
            return None
        if base_icon.get_size() == target_size:
            return base_icon
        return pygame.transform.scale(base_icon, target_size)

    def _boon_icon_layout(self, hud_panel_width: int, boon_count: int) -> tuple[int, int]:
        available_width = max(160, hud_panel_width - 28)
        default_icon_size = 36 if hud_panel_width >= 620 else 32
        gap = 8
        usable_width = available_width - (max(0, boon_count - 1) * gap) - 16
        icon_size = max(26, min(default_icon_size, usable_width // max(1, boon_count)))
        return icon_size, gap

    @staticmethod
    def _build_run_boon_bindings() -> list[tuple[BlessingDefinition, str]]:
        bindings: list[tuple[BlessingDefinition, str]] = []
        for definition in list_blessings():
            if definition.category is not BlessingCategory.RUN_BOON:
                continue
            stack_field = BottomPlayerHUD._run_boon_stack_field(definition.run_boon_modifier)
            if stack_field is not None:
                bindings.append((definition, stack_field))
        return bindings

    @staticmethod
    def _run_boon_stack_field(modifier: RunBoonModifier) -> str | None:
        for field in dataclass_fields(RunBoonModifier):
            value = getattr(modifier, field.name)
            if int(value) > 0:
                return field.name
        return None

    def _draw_ability_cooldown(
        self,
        surface: pygame.Surface,
        block_rect: pygame.Rect,
        player: dict[str, object],
    ) -> int:
        pygame.draw.rect(surface, (26, 30, 36), block_rect, border_radius=8)
        pygame.draw.rect(surface, (95, 102, 118), block_rect, width=2, border_radius=8)

        ability_payload = player.get("active_ability")
        if not isinstance(ability_payload, dict):
            label = self.label_font.render("Ability", True, (210, 212, 218))
            value = self.value_font.render("None", True, (190, 194, 204))
            surface.blit(label, label.get_rect(topleft=(block_rect.left + 8, block_rect.top + 8)))
            surface.blit(value, value.get_rect(topleft=(block_rect.left + 8, block_rect.top + 34)))
            return block_rect.right

        ability_name = str(ability_payload.get("ability_hud_label", "Ability"))
        cooldown_total = max(0.001, float(ability_payload.get("cooldown_total_seconds", 0.0)))
        cooldown_remaining = max(
            0.0,
            float(ability_payload.get("cooldown_remaining_seconds", 0.0)),
        )
        ratio = max(0.0, min(1.0, cooldown_remaining / cooldown_total))
        ready = cooldown_remaining <= 0.0
        active_remaining = max(0.0, float(ability_payload.get("active_remaining_seconds", 0.0)))

        label = self.label_font.render(ability_name, True, (228, 230, 235))
        surface.blit(label, label.get_rect(topleft=(block_rect.left + 8, block_rect.top + 8)))

        bar_rect = pygame.Rect(
            block_rect.left + 8,
            block_rect.top + 36,
            max(62, block_rect.width - 16),
            16,
        )
        pygame.draw.rect(surface, (46, 50, 60), bar_rect, border_radius=5)
        pygame.draw.rect(surface, (95, 102, 118), bar_rect, width=1, border_radius=5)
        if ratio > 0.0:
            fill_width = max(1, int(round((bar_rect.width - 2) * (1.0 - ratio))))
            fill_rect = pygame.Rect(
                bar_rect.left + 1,
                bar_rect.top + 1,
                fill_width,
                max(1, bar_rect.height - 2),
            )
            pygame.draw.rect(surface, (112, 124, 146), fill_rect, border_radius=4)
        elif ready:
            fill_rect = pygame.Rect(
                bar_rect.left + 1,
                bar_rect.top + 1,
                max(1, bar_rect.width - 2),
                max(1, bar_rect.height - 2),
            )
            pygame.draw.rect(surface, (104, 196, 132), fill_rect, border_radius=4)

        status_text = "Ready" if ready else f"{cooldown_remaining:.1f}s"
        if active_remaining > 0.0:
            status_text = f"Active {active_remaining:.1f}s"
        status = self.value_font.render(status_text, True, (242, 242, 242))
        surface.blit(
            status,
            status.get_rect(midleft=(block_rect.left + 8, block_rect.bottom - 12)),
        )
        return block_rect.right

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

    @staticmethod
    def _read_int(value: object, default: int) -> int:
        try:
            return int(value)
        except (TypeError, ValueError):
            return default


class TopRunStatsHUD:
    def __init__(self, fonts: UIFonts) -> None:
        self.value_font = fonts.hud

    def set_fonts(self, fonts: UIFonts) -> None:
        self.value_font = fonts.hud

    def render(self, surface: pygame.Surface, snapshot: WorldSnapshot) -> None:
        panel_rect = self._panel_rect(surface)
        pygame.draw.rect(surface, (16, 18, 22), panel_rect, border_radius=10)
        pygame.draw.rect(surface, (86, 96, 110), panel_rect, width=2, border_radius=10)

        stats_line = self._build_stats_line(snapshot, panel_rect.width, self.value_font)
        rendered = self.value_font.render(stats_line, True, (230, 232, 238))
        surface.blit(
            rendered,
            rendered.get_rect(center=panel_rect.center),
        )

    @staticmethod
    def _panel_rect(surface: pygame.Surface) -> pygame.Rect:
        margin = 14
        width = min(980, surface.get_width() - margin * 2)
        height = 44
        return pygame.Rect((surface.get_width() - width) // 2, margin, width, height)

    def _build_stats_line(
        self,
        snapshot: WorldSnapshot,
        panel_width: int,
        font: pygame.font.Font,
    ) -> str:
        difficulty_factor = self._read_float(snapshot.difficulty.get("factor"), default=1.0)
        spawn_interval = self._read_float(
            snapshot.difficulty.get("spawn_interval_seconds"),
            default=0.0,
        )
        elapsed = max(0.0, float(snapshot.simulation_time))
        enemies_alive = len(snapshot.enemies)
        kills = self._read_int(snapshot.score.get("enemies_killed_total"), default=0)

        full = (
            f"Difficulty x{difficulty_factor:.2f} | "
            f"Time {self._format_time(elapsed)} | "
            f"Enemies Alive {enemies_alive} | "
            f"Kills {kills} | "
            f"Spawn {spawn_interval:.2f}s"
        )
        if font.size(full)[0] <= panel_width - 20:
            return full

        compact = (
            f"Diff x{difficulty_factor:.2f} | "
            f"Time {self._format_time(elapsed)} | "
            f"Alive {enemies_alive} | "
            f"Kills {kills}"
        )
        if font.size(compact)[0] <= panel_width - 20:
            return compact

        return f"x{difficulty_factor:.2f}  {self._format_time(elapsed)}  A{enemies_alive}  K{kills}"

    @staticmethod
    def _format_time(total_seconds: float) -> str:
        whole_seconds = int(total_seconds)
        minutes = whole_seconds // 60
        seconds = whole_seconds % 60
        return f"{minutes:02d}:{seconds:02d}"

    @staticmethod
    def _read_float(value: object, default: float) -> float:
        try:
            return float(value)
        except (TypeError, ValueError):
            return default

    @staticmethod
    def _read_int(value: object, default: int) -> int:
        try:
            return int(value)
        except (TypeError, ValueError):
            return default

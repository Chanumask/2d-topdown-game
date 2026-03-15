from __future__ import annotations

import math

import pygame

from game.core.profile import PlayerProfile
from game.core.upgrades import (
    UpgradeDefinition,
    compute_upgrade_cost,
    compute_upgrade_runtime_value,
    get_upgrade_runtime_label,
    list_upgrades,
)
from game.input.menu_actions import MenuActions
from game.render.upgrades import UpgradeSpriteLibrary
from game.ui.widgets import draw_centered_text, hovered_index, wrap_text


class ShopScreen:
    def __init__(self) -> None:
        self.upgrades: list[UpgradeDefinition] = list_upgrades()
        self.icon_library = UpgradeSpriteLibrary(self.upgrades)
        self.selected_index = 0
        self.focus_area = "grid"
        self.hover_index: int | None = None
        self.hover_back = False
        self.last_message = ""

    def handle_input(
        self,
        actions: MenuActions,
        profile: PlayerProfile,
        surface: pygame.Surface,
    ) -> tuple[str | None, bool]:
        changed_profile = False

        tile_rects = self._tile_rects(surface)
        self.hover_index = hovered_index(actions.mouse_position, tile_rects)
        back_rect = self._back_rect(surface)
        self.hover_back = back_rect.collidepoint(actions.mouse_position or (-1, -1))

        if actions.mouse_moved:
            if self.hover_index is not None:
                self.selected_index = self.hover_index
                self.focus_area = "grid"
            elif self.hover_back:
                self.focus_area = "back"

        if actions.back:
            return "back", changed_profile

        if actions.mouse_left_click:
            if self.hover_index is not None:
                self.selected_index = self.hover_index
                self.focus_area = "grid"
                return self._activate_selected(profile)
            if self.hover_back:
                self.focus_area = "back"
                return "back", changed_profile

        if self.focus_area == "grid":
            self._handle_grid_navigation(actions, surface)
            if actions.select:
                return self._activate_selected(profile)
        elif self.focus_area == "back":
            if actions.navigate_down and self.upgrades:
                self.focus_area = "grid"
            if actions.select:
                return "back", changed_profile

        return None, changed_profile

    def render(
        self,
        surface: pygame.Surface,
        profile: PlayerProfile,
        title_font: pygame.font.Font,
        body_font: pygame.font.Font,
        small_font: pygame.font.Font,
    ) -> None:
        width, _ = surface.get_size()
        margin_x, title_y, currency_y, helper_y, panel_top, panel_height = self._header_layout(
            surface
        )

        draw_centered_text(surface, title_font, "Shop", title_y, (245, 245, 245))
        draw_centered_text(
            surface,
            body_font,
            f"Persistent Meta Currency: {profile.meta_currency}",
            currency_y,
            (230, 230, 230),
        )
        draw_centered_text(
            surface,
            small_font,
            "Upgrade tiles buy persistent power-ups for future runs.",
            helper_y,
            (180, 180, 180),
        )

        self._draw_button(
            surface,
            body_font,
            self._back_rect(surface),
            "Back",
            selected=self.focus_area == "back",
            hovered=self.hover_back,
        )

        tile_rects = self._tile_rects(surface)
        for index, upgrade in enumerate(self.upgrades):
            self._draw_upgrade_tile(
                surface=surface,
                body_font=body_font,
                small_font=small_font,
                rect=tile_rects[index],
                upgrade=upgrade,
                profile=profile,
                selected=self.focus_area == "grid" and index == self.selected_index,
                hovered=index == self.hover_index,
            )

        if self.last_message:
            message_y = panel_top - 16
            draw_centered_text(surface, small_font, self.last_message, message_y, (235, 215, 120))

        self._draw_details_panel(
            surface=surface,
            body_font=body_font,
            small_font=small_font,
            profile=profile,
            margin_x=margin_x,
            panel_top=panel_top,
            panel_height=panel_height,
            panel_width=width - (margin_x * 2),
        )

    def _activate_selected(self, profile: PlayerProfile) -> tuple[str | None, bool]:
        changed_profile = False
        selected_upgrade = self.upgrades[self.selected_index]
        result = profile.purchase_upgrade(selected_upgrade.upgrade_id)
        if result.success:
            changed_profile = True
            self.last_message = (
                f"Purchased {selected_upgrade.display_name} "
                f"Lv {result.new_level}/{result.max_level} for {result.cost}"
            )
        elif result.reason == "insufficient_funds":
            self.last_message = (
                f"Not enough meta currency for {selected_upgrade.display_name}. Need {result.cost}."
            )
        elif result.reason == "max_level_reached":
            self.last_message = f"{selected_upgrade.display_name} is already maxed."
        else:
            self.last_message = "Purchase failed."

        return None, changed_profile

    def _draw_upgrade_tile(
        self,
        *,
        surface: pygame.Surface,
        body_font: pygame.font.Font,
        small_font: pygame.font.Font,
        rect: pygame.Rect,
        upgrade: UpgradeDefinition,
        profile: PlayerProfile,
        selected: bool,
        hovered: bool,
    ) -> None:
        level = profile.upgrades.get(upgrade.upgrade_id, 0)
        maxed = level >= upgrade.max_level
        cost = None if maxed else compute_upgrade_cost(upgrade, level)
        affordable = cost is not None and profile.meta_currency >= cost

        bg = (34, 38, 46)
        border = (88, 96, 108)
        accent = (88, 96, 108)
        cost_color = (214, 214, 214)
        if maxed:
            accent = (116, 186, 122)
            cost_color = (166, 222, 168)
        elif affordable:
            accent = (216, 186, 94)
            cost_color = (244, 221, 132)
        else:
            accent = (134, 144, 164)
            cost_color = (200, 200, 200)

        if hovered:
            bg = (52, 58, 70)
            border = (140, 150, 165)
        if selected:
            bg = (64, 72, 86)
            border = (255, 235, 120)

        pygame.draw.rect(surface, bg, rect, border_radius=12)
        pygame.draw.rect(surface, border, rect, width=2, border_radius=12)

        compact_tile = rect.height < 150 or rect.width < 190
        if compact_tile:
            self._draw_compact_upgrade_tile(
                surface=surface,
                body_font=body_font,
                small_font=small_font,
                rect=rect,
                upgrade=upgrade,
                level=level,
                maxed=maxed,
                cost=cost,
                cost_color=cost_color,
            )
            return

        title_lines = wrap_text(body_font, upgrade.display_name, max_width=rect.width - 20)
        title_y = rect.y + max(10, rect.height // 14)
        for line_index, line in enumerate(title_lines[:2]):
            rendered = body_font.render(line, True, (232, 232, 232))
            surface.blit(
                rendered,
                rendered.get_rect(center=(rect.centerx, title_y + (line_index * 20))),
            )

        level_y = rect.y + max(36, min(68, rect.height // 3))
        level_text = small_font.render(
            f"Level {level}/{upgrade.max_level}",
            True,
            (176, 184, 196),
        )
        surface.blit(level_text, level_text.get_rect(center=(rect.centerx, level_y)))

        cost_y = rect.bottom - max(16, rect.height // 10)
        icon_side_padding = max(12, rect.width // 7)
        icon_top = level_y + max(12, rect.height // 14)
        icon_bottom = cost_y - max(12, rect.height // 12)
        icon_height = max(12, icon_bottom - icon_top)
        icon_box = pygame.Rect(
            rect.x + icon_side_padding,
            icon_top,
            max(12, rect.width - (icon_side_padding * 2)),
            icon_height,
        )
        icon = self.icon_library.get_icon(upgrade.upgrade_id, icon_box.size)
        if icon is not None:
            surface.blit(icon, icon.get_rect(center=icon_box.center))
        else:
            pygame.draw.rect(surface, (46, 52, 62), icon_box, border_radius=10)
            pygame.draw.rect(surface, (92, 100, 114), icon_box, width=2, border_radius=10)
            placeholder = small_font.render(
                self._placeholder_label(upgrade.display_name),
                True,
                accent,
            )
            surface.blit(placeholder, placeholder.get_rect(center=icon_box.center))

        if maxed:
            cost_label = "MAXED"
        else:
            cost_label = f"Cost {cost}"
        cost_render = body_font.render(cost_label, True, cost_color)
        surface.blit(cost_render, cost_render.get_rect(center=(rect.centerx, cost_y)))

    def _draw_compact_upgrade_tile(
        self,
        *,
        surface: pygame.Surface,
        body_font: pygame.font.Font,
        small_font: pygame.font.Font,
        rect: pygame.Rect,
        upgrade: UpgradeDefinition,
        level: int,
        maxed: bool,
        cost: int | None,
        cost_color: tuple[int, int, int],
    ) -> None:
        icon_side = max(16, rect.height - 16)
        icon_side = min(icon_side, max(24, min(48, rect.width // 3)))
        text_left_padding = 8
        text_right_padding = 8
        tentative_text_left = rect.x + text_left_padding + icon_side + 8
        available_text_width = (rect.right - text_right_padding) - tentative_text_left
        if available_text_width < 74:
            icon_side = max(24, min(icon_side, 34))
        icon_box = pygame.Rect(
            rect.x + text_left_padding,
            rect.y + (rect.height - icon_side) // 2,
            icon_side,
            icon_side,
        )
        icon = self.icon_library.get_icon(upgrade.upgrade_id, icon_box.size)
        if icon is not None:
            surface.blit(icon, icon.get_rect(center=icon_box.center))

        text_left = icon_box.right + 8
        text_right = rect.right - text_right_padding
        name_width = max(60, text_right - text_left)
        name_lines = wrap_text(small_font, upgrade.display_name, max_width=name_width)
        name_y = rect.y + 8
        for line in name_lines[:2]:
            title_render = small_font.render(line, True, (232, 232, 232))
            surface.blit(title_render, (text_left, name_y))
            name_y += max(14, small_font.get_linesize() - 2)

        cost_label = "MAXED" if maxed else f"Cost {cost}"
        cost_render = small_font.render(cost_label, True, cost_color)
        cost_x = max(text_left, text_right - cost_render.get_width())
        cost_y = rect.y + max(8, rect.height // 2 - cost_render.get_height() // 2)
        surface.blit(cost_render, (cost_x, cost_y))

        level_render = small_font.render(f"Lv {level}/{upgrade.max_level}", True, (176, 184, 196))
        level_y = rect.bottom - level_render.get_height() - 6
        surface.blit(level_render, (text_left, level_y))

    def _draw_details_panel(
        self,
        surface: pygame.Surface,
        body_font: pygame.font.Font,
        small_font: pygame.font.Font,
        profile: PlayerProfile,
        margin_x: int,
        panel_top: int,
        panel_height: int,
        panel_width: int,
    ) -> None:
        panel_rect = pygame.Rect(margin_x, panel_top, panel_width, panel_height)
        pygame.draw.rect(surface, (28, 32, 38), panel_rect, border_radius=12)
        pygame.draw.rect(surface, (90, 96, 108), panel_rect, 2, border_radius=12)

        selected_upgrade = self._selected_upgrade()

        lines: list[str] = []
        if selected_upgrade is None:
            lines.append("Back")
            lines.append("Return to the main menu.")
        else:
            level = profile.upgrades.get(selected_upgrade.upgrade_id, 0)
            maxed = level >= selected_upgrade.max_level
            next_cost = None if maxed else compute_upgrade_cost(selected_upgrade, level)
            runtime_label = get_upgrade_runtime_label(selected_upgrade.upgrade_id)
            current_value = compute_upgrade_runtime_value(selected_upgrade.upgrade_id, level)
            next_value = (
                None
                if maxed
                else compute_upgrade_runtime_value(selected_upgrade.upgrade_id, level + 1)
            )

            lines.append(f"Upgrade: {selected_upgrade.display_name}")
            lines.append(
                "Effect: "
                f"+{selected_upgrade.effect_value_per_level} "
                f"{self._format_effect_label(selected_upgrade.effect_type)} per level"
            )
            lines.append(f"Current Level: {level}/{selected_upgrade.max_level}")
            lines.append(
                f"Current {runtime_label}: "
                f"{self._format_runtime_value(selected_upgrade.upgrade_id, current_value)}"
            )
            if next_value is None:
                lines.append("Next Level Value: Max Level Reached")
            else:
                lines.append(
                    f"Next {runtime_label}: "
                    f"{self._format_runtime_value(selected_upgrade.upgrade_id, next_value)}"
                )
            lines.append(f"Next Cost: {'MAXED' if next_cost is None else next_cost}")
            lines.extend(
                wrap_text(
                    body_font,
                    selected_upgrade.description,
                    max_width=max(120, panel_rect.width - 24),
                )
            )

        heading = small_font.render("Details", True, (176, 184, 196))
        surface.blit(heading, (panel_rect.x + 12, panel_rect.y + 12))

        row_height = max(24, body_font.get_linesize() + 4)
        for index, line in enumerate(lines):
            rendered = body_font.render(line, True, (220, 220, 220))
            y = panel_rect.y + 40 + (index * row_height)
            if y + row_height > panel_rect.bottom - 8:
                break
            surface.blit(rendered, (panel_rect.x + 12, y))

    def _selected_upgrade(self) -> UpgradeDefinition | None:
        if self.focus_area != "grid":
            return None
        if not (0 <= self.selected_index < len(self.upgrades)):
            return None
        return self.upgrades[self.selected_index]

    def _handle_grid_navigation(
        self,
        actions: MenuActions,
        surface: pygame.Surface,
    ) -> None:
        if not self.upgrades:
            self.focus_area = "back"
            return

        columns = self._tile_columns(surface)
        current = self.selected_index

        if actions.navigate_left:
            current = max(0, current - 1)
        if actions.navigate_right:
            current = min(len(self.upgrades) - 1, current + 1)
        if actions.navigate_up:
            if current - columns >= 0:
                current -= columns
            else:
                self.focus_area = "back"
        if actions.navigate_down and current + columns < len(self.upgrades):
            current += columns

        self.selected_index = current

    def _tile_columns(self, surface: pygame.Surface) -> int:
        upgrade_count = max(1, len(self.upgrades))
        area = self._grid_area_rect(surface)
        available_width = area.width
        available_height = area.height
        max_columns = min(4, upgrade_count)

        for columns in range(max_columns, 0, -1):
            gap_x = 16
            gap_y = 16
            tile_width = (available_width - (gap_x * (columns - 1))) // columns
            rows = max(1, math.ceil(upgrade_count / columns))
            tile_height = (available_height - (gap_y * (rows - 1))) // rows
            if tile_width >= 116 and tile_height >= 96:
                return columns
        return 1

    def _tile_rects(self, surface: pygame.Surface) -> list[pygame.Rect]:
        area = self._grid_area_rect(surface)
        columns = self._tile_columns(surface)
        rows = max(1, math.ceil(len(self.upgrades) / columns))
        gap_x = 16
        gap_y = 16
        if area.height < 360:
            gap_y = 10
        if area.width < 720:
            gap_x = 10

        tile_width = min(184, (area.width - (gap_x * (columns - 1))) // columns)
        tile_height = min(178, (area.height - (gap_y * (rows - 1))) // rows)

        total_width = (columns * tile_width) + ((columns - 1) * gap_x)
        total_height = (rows * tile_height) + ((rows - 1) * gap_y)
        start_x = area.x + max(0, (area.width - total_width) // 2)
        start_y = area.y + max(0, (area.height - total_height) // 2)

        rects: list[pygame.Rect] = []
        for index, _ in enumerate(self.upgrades):
            row = index // columns
            column = index % columns
            rects.append(
                pygame.Rect(
                    start_x + column * (tile_width + gap_x),
                    start_y + row * (tile_height + gap_y),
                    tile_width,
                    tile_height,
                )
            )
        return rects

    def _grid_area_rect(self, surface: pygame.Surface) -> pygame.Rect:
        width, _ = surface.get_size()
        margin_x, _, _, helper_y, panel_top, _ = self._header_layout(surface)
        top = helper_y + 22
        bottom = panel_top - 18
        return pygame.Rect(
            margin_x,
            top,
            width - (margin_x * 2),
            max(120, bottom - top),
        )

    def _back_rect(self, surface: pygame.Surface) -> pygame.Rect:
        width, _ = surface.get_size()
        margin_x, title_y, _, _, _, _ = self._header_layout(surface)
        back_width = max(120, min(160, width // 5))
        return pygame.Rect(width - margin_x - back_width, title_y - 12, back_width, 40)

    @staticmethod
    def _header_layout(surface: pygame.Surface) -> tuple[int, int, int, int, int, int]:
        width, height = surface.get_size()
        margin_x = max(20, width // 22)
        title_y = max(34, height // 12)
        currency_y = title_y + max(24, min(40, height // 14))
        helper_y = currency_y + max(18, min(30, height // 20))
        panel_height = max(112, min(220, int(height * 0.28)))
        panel_top = height - panel_height - max(12, height // 40)
        return margin_x, title_y, currency_y, helper_y, panel_top, panel_height

    @staticmethod
    def _draw_button(
        surface: pygame.Surface,
        font: pygame.font.Font,
        rect: pygame.Rect,
        label: str,
        *,
        selected: bool,
        hovered: bool,
    ) -> None:
        bg = (34, 38, 46)
        border = (88, 96, 108)
        if hovered:
            bg = (52, 58, 70)
            border = (140, 150, 165)
        if selected:
            bg = (64, 72, 86)
            border = (255, 235, 120)

        pygame.draw.rect(surface, bg, rect, border_radius=8)
        pygame.draw.rect(surface, border, rect, width=2, border_radius=8)
        rendered = font.render(label, True, (228, 228, 228))
        surface.blit(rendered, rendered.get_rect(center=rect.center))

    @staticmethod
    def _placeholder_label(display_name: str) -> str:
        initials = [token[0] for token in display_name.split() if token]
        return "".join(initials[:3]).upper() or "?"

    @staticmethod
    def _format_effect_label(effect_type: str) -> str:
        if effect_type == "coin_pickup_radius":
            return "coin and Blessing pickup range"
        if effect_type == "projectile_damage":
            return "rock throw damage"
        return effect_type.replace("_", " ").strip()

    @staticmethod
    def _format_runtime_value(upgrade_id: str, value: float) -> str:
        if upgrade_id == "fast_hands":
            return f"{value:.2f}s"
        return f"{value:.0f}"

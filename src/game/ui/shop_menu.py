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
from game.ui.widgets import draw_centered_text, hovered_index, wrap_text


class ShopScreen:
    def __init__(self) -> None:
        self.upgrades: list[UpgradeDefinition] = list_upgrades()
        self.selected_index = 0
        self.hover_index: int | None = None
        self.last_message = ""

    def handle_input(
        self,
        actions: MenuActions,
        profile: PlayerProfile,
        surface: pygame.Surface,
    ) -> tuple[str | None, bool]:
        changed_profile = False

        max_index = len(self.upgrades)
        if actions.navigate_up:
            self.selected_index = (self.selected_index - 1) % (max_index + 1)
        if actions.navigate_down:
            self.selected_index = (self.selected_index + 1) % (max_index + 1)

        visible_indexes, row_rects, _ = self._list_layout(surface)
        hovered = self._hovered_entry(actions.mouse_position, visible_indexes, row_rects)
        self.hover_index = hovered
        if actions.mouse_moved and hovered is not None:
            self.selected_index = hovered

        if actions.back:
            return "back", changed_profile

        if actions.mouse_left_click and hovered is not None:
            self.selected_index = hovered
            return self._activate_selected(profile)

        if actions.select:
            return self._activate_selected(profile)

        return None, changed_profile

    def render(
        self,
        surface: pygame.Surface,
        profile: PlayerProfile,
        title_font: pygame.font.Font,
        body_font: pygame.font.Font,
    ) -> None:
        width, height = surface.get_size()
        margin_x = max(24, width // 20)

        title_y = max(46, height // 11)
        currency_y = title_y + 38
        helper_y = currency_y + 28

        panel_height = max(170, min(260, height // 3))
        panel_top = height - panel_height - 16

        visible_indexes, row_rects, _ = self._list_layout(surface)

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
            body_font,
            "Run coins are earned in runs and banked into persistent currency.",
            helper_y,
            (180, 180, 180),
        )

        for list_offset, actual_index in enumerate(visible_indexes):
            row_rect = row_rects[list_offset]
            is_selected = actual_index == self.selected_index
            is_hovered = actual_index == self.hover_index

            if is_selected:
                bg = (64, 72, 86)
                border = (255, 235, 120)
            elif is_hovered:
                bg = (52, 58, 70)
                border = (140, 150, 165)
            else:
                bg = (34, 38, 46)
                border = (88, 96, 108)

            pygame.draw.rect(surface, bg, row_rect, border_radius=8)
            pygame.draw.rect(surface, border, row_rect, width=2, border_radius=8)

            if actual_index >= len(self.upgrades):
                back_text = body_font.render("Back to Main Menu", True, (220, 220, 220))
                surface.blit(
                    back_text,
                    (row_rect.x + 14, row_rect.centery - (back_text.get_height() // 2)),
                )
                continue

            upgrade = self.upgrades[actual_index]
            level = profile.upgrades.get(upgrade.upgrade_id, 0)
            maxed = level >= upgrade.max_level
            cost = None if maxed else compute_upgrade_cost(upgrade, level)
            affordable = cost is not None and profile.meta_currency >= cost

            left_text = f"{upgrade.display_name}  Lv {level}/{upgrade.max_level}"
            if maxed:
                right_text = "MAXED"
            elif affordable:
                right_text = f"Cost {cost} | BUY"
            else:
                right_text = f"Cost {cost} | LOCK"

            left_render = body_font.render(left_text, True, (220, 220, 220))
            right_render = body_font.render(right_text, True, (220, 220, 220))
            surface.blit(
                left_render,
                (row_rect.x + 14, row_rect.centery - (left_render.get_height() // 2)),
            )
            surface.blit(
                right_render,
                (
                    row_rect.right - right_render.get_width() - 14,
                    row_rect.centery - (right_render.get_height() // 2),
                ),
            )

        if self.last_message:
            message_y = panel_top - 12
            draw_centered_text(surface, body_font, self.last_message, message_y, (235, 215, 120))

        self._draw_details_panel(
            surface=surface,
            body_font=body_font,
            profile=profile,
            margin_x=margin_x,
            panel_top=panel_top,
            panel_height=panel_height,
            panel_width=width - (margin_x * 2),
        )

    def _activate_selected(self, profile: PlayerProfile) -> tuple[str | None, bool]:
        changed_profile = False
        if self.selected_index == len(self.upgrades):
            return "back", changed_profile

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

    def _list_layout(
        self,
        surface: pygame.Surface,
    ) -> tuple[list[int], list[pygame.Rect], int]:
        width, height = surface.get_size()
        margin_x = max(24, width // 20)

        title_y = max(46, height // 11)
        currency_y = title_y + 38
        helper_y = currency_y + 28

        panel_height = max(170, min(260, height // 3))
        panel_top = height - panel_height - 16

        list_top = helper_y + 40
        list_bottom = panel_top - 16
        row_height = max(44, min(52, height // 14))

        total_entries = len(self.upgrades) + 1
        max_visible = max(1, (list_bottom - list_top) // row_height)
        scroll_start = max(
            0,
            min(self.selected_index - max_visible + 1, total_entries - max_visible),
        )
        visible_end = min(total_entries, scroll_start + max_visible)
        visible_indexes = list(range(scroll_start, visible_end))

        row_rects: list[pygame.Rect] = []
        for offset, _ in enumerate(visible_indexes):
            row_y = list_top + (offset * row_height)
            row_rects.append(pygame.Rect(margin_x, row_y, width - (margin_x * 2), row_height - 4))

        return visible_indexes, row_rects, list_top

    @staticmethod
    def _hovered_entry(
        mouse_position: tuple[int, int] | None,
        visible_indexes: list[int],
        row_rects: list[pygame.Rect],
    ) -> int | None:
        hovered_row = hovered_index(mouse_position, row_rects)
        if hovered_row is None:
            return None
        if hovered_row >= len(visible_indexes):
            return None
        return visible_indexes[hovered_row]

    def _draw_details_panel(
        self,
        surface: pygame.Surface,
        body_font: pygame.font.Font,
        profile: PlayerProfile,
        margin_x: int,
        panel_top: int,
        panel_height: int,
        panel_width: int,
    ) -> None:
        panel_rect = pygame.Rect(margin_x, panel_top, panel_width, panel_height)
        pygame.draw.rect(surface, (28, 32, 38), panel_rect)
        pygame.draw.rect(surface, (90, 96, 108), panel_rect, 2)

        selected_upgrade = (
            self.upgrades[self.selected_index] if self.selected_index < len(self.upgrades) else None
        )

        lines: list[str] = []
        if selected_upgrade is None:
            lines.append("Back to Main Menu")
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

        row_height = max(24, body_font.get_linesize() + 4)
        for index, line in enumerate(lines):
            rendered = body_font.render(line, True, (220, 220, 220))
            y = panel_rect.y + 10 + (index * row_height)
            if y + row_height > panel_rect.bottom - 8:
                break
            surface.blit(rendered, (panel_rect.x + 12, y))

    @staticmethod
    def _format_effect_label(effect_type: str) -> str:
        return effect_type.replace("_", " ").strip()

    @staticmethod
    def _format_runtime_value(upgrade_id: str, value: float) -> str:
        if upgrade_id == "fast_hands":
            return f"{value:.2f}s"
        return f"{value:.0f}"

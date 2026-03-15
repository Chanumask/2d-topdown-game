import pygame

from game.core.profile import UserSettings
from game.input.menu_actions import MenuActions
from game.ui.widgets import draw_centered_text, hovered_index


class SettingsScreen:
    def __init__(self) -> None:
        self.items = [
            "Master Volume",
            "Music Volume",
            "SFX Volume",
            "Fullscreen",
            "Mouse Sensitivity",
            "Back",
        ]
        self.selected_index = 0
        self.hover_index: int | None = None

    def handle_input(
        self,
        actions: MenuActions,
        settings: UserSettings,
        surface: pygame.Surface,
    ) -> str | None:
        row_rects, control_rects = self._layout(surface)
        hovered = hovered_index(actions.mouse_position, row_rects)
        self.hover_index = hovered
        if actions.mouse_moved and hovered is not None:
            self.selected_index = hovered

        if actions.navigate_up:
            self.selected_index = (self.selected_index - 1) % len(self.items)
        if actions.navigate_down:
            self.selected_index = (self.selected_index + 1) % len(self.items)

        if actions.mouse_left_click and hovered is not None and actions.mouse_position is not None:
            self.selected_index = hovered
            clicked_item = self.items[hovered]
            if clicked_item == "Back":
                return "back"
            controls = control_rects.get(hovered, {})
            if clicked_item == "Fullscreen":
                toggle_rect = controls.get("toggle")
                if (
                    toggle_rect is None
                    or toggle_rect.collidepoint(actions.mouse_position)
                    or row_rects[hovered].collidepoint(actions.mouse_position)
                ):
                    settings.fullscreen = not settings.fullscreen
            elif clicked_item in {
                "Master Volume",
                "Music Volume",
                "SFX Volume",
                "Mouse Sensitivity",
            }:
                minus_rect = controls.get("minus")
                plus_rect = controls.get("plus")
                if minus_rect is not None and minus_rect.collidepoint(actions.mouse_position):
                    self._adjust(clicked_item, settings, -1)
                elif plus_rect is not None and plus_rect.collidepoint(actions.mouse_position):
                    self._adjust(clicked_item, settings, 1)
                elif row_rects[hovered].collidepoint(actions.mouse_position):
                    self._adjust(clicked_item, settings, 1)

        item = self.items[self.selected_index]
        if item == "Back":
            if actions.select or actions.back:
                return "back"
            return None

        if actions.navigate_left:
            self._adjust(item, settings, -1)
        if actions.navigate_right:
            self._adjust(item, settings, 1)
        if actions.select and item == "Fullscreen":
            settings.fullscreen = not settings.fullscreen

        if actions.back:
            return "back"
        return None

    def render(
        self,
        surface: pygame.Surface,
        settings: UserSettings,
        title_font: pygame.font.Font,
        body_font: pygame.font.Font,
    ) -> None:
        row_rects, control_rects = self._layout(surface)

        title_y = max(52, surface.get_height() // 8)
        draw_centered_text(surface, title_font, "Settings", title_y, (245, 245, 245))
        draw_centered_text(
            surface,
            body_font,
            "Keyboard: arrows + enter | Mouse: hover + click",
            title_y + max(28, surface.get_height() // 18),
            (175, 175, 175),
        )

        for index, item in enumerate(self.items):
            row_rect = row_rects[index]
            is_selected = index == self.selected_index
            is_hovered = index == self.hover_index

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

            label = body_font.render(item, True, (225, 225, 225))
            surface.blit(label, (row_rect.x + 16, row_rect.centery - (label.get_height() // 2)))

            controls = control_rects.get(index, {})
            if item in {"Master Volume", "Music Volume", "SFX Volume", "Mouse Sensitivity"}:
                value = (
                    f"{settings.mouse_sensitivity:.1f}"
                    if item == "Mouse Sensitivity"
                    else str(self._get_volume_value(item, settings))
                )
                self._draw_adjust_buttons(
                    surface=surface,
                    body_font=body_font,
                    minus_rect=controls["minus"],
                    plus_rect=controls["plus"],
                    value_rect=controls["value"],
                    value=value,
                )
            elif item == "Fullscreen":
                toggle_rect = controls["toggle"]
                toggle_text = "On" if settings.fullscreen else "Off"
                pygame.draw.rect(surface, (28, 32, 38), toggle_rect, border_radius=6)
                pygame.draw.rect(surface, (120, 130, 146), toggle_rect, width=2, border_radius=6)
                rendered = body_font.render(toggle_text, True, (220, 220, 220))
                surface.blit(rendered, rendered.get_rect(center=toggle_rect.center))
            elif item == "Back":
                rendered = body_font.render("Return", True, (220, 220, 220))
                surface.blit(
                    rendered,
                    rendered.get_rect(midright=(row_rect.right - 18, row_rect.centery)),
                )

    def _layout(
        self,
        surface: pygame.Surface,
    ) -> tuple[list[pygame.Rect], dict[int, dict[str, pygame.Rect]]]:
        width, height = surface.get_size()
        side_margin = max(16, width // 24)
        panel_width = min(max(320, int(width * 0.82)), width - (side_margin * 2))
        panel_x = (width - panel_width) // 2
        title_y = max(52, height // 8)
        row_start_y = title_y + max(58, height // 8)
        bottom_margin = max(18, height // 18)
        preferred_gap = max(6, min(12, height // 68))
        available_height = max(120, height - row_start_y - bottom_margin)

        row_gap = preferred_gap
        total_gap = row_gap * max(0, len(self.items) - 1)
        row_height = max(34, min(62, (available_height - total_gap) // max(1, len(self.items))))
        if row_height <= 36:
            row_gap = max(4, min(8, preferred_gap))
            total_gap = row_gap * max(0, len(self.items) - 1)
            row_height = max(
                30,
                min(62, (available_height - total_gap) // max(1, len(self.items))),
            )

        row_rects: list[pygame.Rect] = []
        control_rects: dict[int, dict[str, pygame.Rect]] = {}
        for index, item in enumerate(self.items):
            row_y = row_start_y + index * (row_height + row_gap)
            row_rect = pygame.Rect(panel_x, row_y, panel_width, row_height)
            row_rects.append(row_rect)

            control_width = max(140, min(280, int(panel_width * 0.34)))
            control_x = row_rect.right - control_width - 14
            control_y = row_rect.y + 8
            control_height = row_rect.height - 16

            if item in {"Master Volume", "Music Volume", "SFX Volume", "Mouse Sensitivity"}:
                button_width = max(32, min(44, control_width // 4))
                minus_rect = pygame.Rect(control_x, control_y, button_width, control_height)
                plus_rect = pygame.Rect(
                    control_x + control_width - button_width,
                    control_y,
                    button_width,
                    control_height,
                )
                value_rect = pygame.Rect(
                    minus_rect.right + 8,
                    control_y,
                    plus_rect.left - minus_rect.right - 16,
                    control_height,
                )
                control_rects[index] = {
                    "minus": minus_rect,
                    "plus": plus_rect,
                    "value": value_rect,
                }
            elif item == "Fullscreen":
                control_rects[index] = {
                    "toggle": pygame.Rect(control_x, control_y, control_width, control_height)
                }

        return row_rects, control_rects

    @staticmethod
    def _draw_adjust_buttons(
        surface: pygame.Surface,
        body_font: pygame.font.Font,
        minus_rect: pygame.Rect,
        plus_rect: pygame.Rect,
        value_rect: pygame.Rect,
        value: str,
    ) -> None:
        for symbol, rect in (("-", minus_rect), ("+", plus_rect)):
            pygame.draw.rect(surface, (28, 32, 38), rect, border_radius=6)
            pygame.draw.rect(surface, (120, 130, 146), rect, width=2, border_radius=6)
            rendered = body_font.render(symbol, True, (220, 220, 220))
            surface.blit(rendered, rendered.get_rect(center=rect.center))

        pygame.draw.rect(surface, (20, 24, 30), value_rect, border_radius=6)
        pygame.draw.rect(surface, (90, 98, 112), value_rect, width=1, border_radius=6)
        rendered_value = body_font.render(value, True, (220, 220, 220))
        surface.blit(rendered_value, rendered_value.get_rect(center=value_rect.center))

    @staticmethod
    def _get_volume_value(item: str, settings: UserSettings) -> int:
        if item == "Master Volume":
            return settings.master_volume
        if item == "Music Volume":
            return settings.music_volume
        return settings.sfx_volume

    @staticmethod
    def _adjust(item: str, settings: UserSettings, direction: int) -> None:
        if item == "Master Volume":
            settings.master_volume = max(0, min(100, settings.master_volume + (5 * direction)))
        elif item == "Music Volume":
            settings.music_volume = max(0, min(100, settings.music_volume + (5 * direction)))
        elif item == "SFX Volume":
            settings.sfx_volume = max(0, min(100, settings.sfx_volume + (5 * direction)))
        elif item == "Fullscreen":
            settings.fullscreen = not settings.fullscreen
        elif item == "Mouse Sensitivity":
            updated = settings.mouse_sensitivity + (0.1 * direction)
            settings.mouse_sensitivity = max(0.2, min(3.0, round(updated, 1)))

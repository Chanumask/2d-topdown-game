import pygame

from game.input.menu_actions import MenuActions
from game.ui.widgets import (
    build_centered_menu_rects,
    draw_centered_text,
    draw_menu_buttons,
    hovered_index,
)


class LobbyScreen:
    def __init__(self) -> None:
        self.selected_index = 0
        self.hover_index: int | None = None

    def handle_input(
        self,
        actions: MenuActions,
        surface: pygame.Surface,
        body_font: pygame.font.Font,
        *,
        selected_character_name: str,
        selected_map_name: str,
    ) -> str | None:
        _, panel_start_y, row_height = self._layout_metrics(surface)
        option_labels = self._option_labels(selected_character_name, selected_map_name)
        option_rects = build_centered_menu_rects(
            surface=surface,
            font=body_font,
            options=option_labels,
            start_y=panel_start_y,
            row_height=row_height,
            min_width=max(340, surface.get_width() // 3),
        )

        hovered = hovered_index(actions.mouse_position, option_rects)
        self.hover_index = hovered
        if actions.mouse_moved and hovered is not None:
            self.selected_index = hovered

        if actions.navigate_up:
            self.selected_index = (self.selected_index - 1) % len(option_labels)
        if actions.navigate_down:
            self.selected_index = (self.selected_index + 1) % len(option_labels)

        if actions.navigate_left:
            return self._command_for_navigation(self.selected_index, step=-1)
        if actions.navigate_right:
            return self._command_for_navigation(self.selected_index, step=1)

        if actions.mouse_left_click and hovered is not None:
            self.selected_index = hovered
            return self._command_for_select(self.selected_index)

        if actions.select:
            return self._command_for_select(self.selected_index)
        if actions.back:
            return "back_main_menu"
        return None

    def render(
        self,
        surface: pygame.Surface,
        title_font: pygame.font.Font,
        body_font: pygame.font.Font,
        *,
        selected_character_name: str,
        selected_map_name: str,
        character_count: int,
        map_count: int,
    ) -> None:
        title_y, panel_start_y, row_height = self._layout_metrics(surface)
        option_labels = self._option_labels(selected_character_name, selected_map_name)
        option_rects = build_centered_menu_rects(
            surface=surface,
            font=body_font,
            options=option_labels,
            start_y=panel_start_y,
            row_height=row_height,
            min_width=max(340, surface.get_width() // 3),
        )

        draw_centered_text(surface, title_font, "Lobby", title_y, (245, 245, 245))
        draw_centered_text(
            surface,
            body_font,
            f"Characters: {character_count}  |  Maps: {map_count}",
            title_y + 48,
            (188, 188, 188),
        )
        draw_centered_text(
            surface,
            body_font,
            "Use Left/Right to change selections.",
            title_y + 80,
            (168, 168, 168),
        )

        draw_menu_buttons(
            surface=surface,
            font=body_font,
            options=option_labels,
            rects=option_rects,
            selected_index=self.selected_index,
            hover_index=self.hover_index,
            normal_color=(210, 210, 210),
            selected_color=(255, 235, 120),
        )

    @staticmethod
    def _option_labels(selected_character_name: str, selected_map_name: str) -> list[str]:
        return [
            f"Character: {selected_character_name}",
            f"Map: {selected_map_name}",
            "Start Run",
            "Back to Main Menu",
        ]

    def _layout_metrics(self, surface: pygame.Surface) -> tuple[int, int, int]:
        height = surface.get_height()
        title_y = max(70, height // 7)
        row_height = max(50, min(72, height // 10))
        panel_start_y = max(title_y + 150, height // 3)
        return title_y, panel_start_y, row_height

    @staticmethod
    def _command_for_navigation(index: int, *, step: int) -> str | None:
        if index == 0:
            return "character_prev" if step < 0 else "character_next"
        if index == 1:
            return "map_prev" if step < 0 else "map_next"
        return None

    @staticmethod
    def _command_for_select(index: int) -> str | None:
        if index == 0:
            return "character_next"
        if index == 1:
            return "map_next"
        if index == 2:
            return "start_run"
        if index == 3:
            return "back_main_menu"
        return None

import pygame

from game.input.menu_actions import MenuActions
from game.ui.widgets import (
    build_centered_menu_rects,
    draw_centered_text,
    draw_menu_buttons,
    hovered_index,
)


class MainMenuScreen:
    def __init__(self) -> None:
        self.options = ["Start Run", "Shop", "Settings", "Quit"]
        self.selected_index = 0
        self.hover_index: int | None = None

    def handle_input(
        self,
        actions: MenuActions,
        surface: pygame.Surface,
        body_font: pygame.font.Font,
    ) -> str | None:
        _, start_y, row_height = self._layout_metrics(surface)
        option_rects = build_centered_menu_rects(
            surface=surface,
            font=body_font,
            options=self.options,
            start_y=start_y,
            row_height=row_height,
            min_width=max(280, surface.get_width() // 4),
        )
        hovered = hovered_index(actions.mouse_position, option_rects)
        self.hover_index = hovered

        if actions.mouse_moved and hovered is not None:
            self.selected_index = hovered

        if actions.navigate_up:
            self.selected_index = (self.selected_index - 1) % len(self.options)
        if actions.navigate_down:
            self.selected_index = (self.selected_index + 1) % len(self.options)

        if actions.mouse_left_click and hovered is not None:
            self.selected_index = hovered
            return self._command_for_selection()

        if actions.select:
            return self._command_for_selection()

        if actions.back:
            return "quit"
        return None

    def render(
        self, surface: pygame.Surface, title_font: pygame.font.Font, body_font: pygame.font.Font
    ) -> None:
        title_y, start_y, row_height = self._layout_metrics(surface)
        option_rects = build_centered_menu_rects(
            surface=surface,
            font=body_font,
            options=self.options,
            start_y=start_y,
            row_height=row_height,
            min_width=max(280, surface.get_width() // 4),
        )

        draw_centered_text(surface, title_font, "Runner2D Survival", title_y, (245, 245, 245))
        draw_centered_text(
            surface=surface,
            font=body_font,
            text="Top-down survival prototype",
            y=title_y + 48,
            color=(175, 175, 175),
        )

        draw_menu_buttons(
            surface=surface,
            font=body_font,
            options=self.options,
            rects=option_rects,
            selected_index=self.selected_index,
            hover_index=self.hover_index,
            normal_color=(200, 200, 200),
            selected_color=(255, 235, 120),
        )

    def _layout_metrics(self, surface: pygame.Surface) -> tuple[int, int, int]:
        height = surface.get_height()
        title_y = max(72, height // 6)
        row_height = max(46, min(68, height // 10))
        menu_block_height = (len(self.options) - 1) * row_height
        start_y = max(title_y + 110, (height - menu_block_height) // 2)
        return title_y, start_y, row_height

    def _command_for_selection(self) -> str | None:
        selected = self.options[self.selected_index]
        if selected == "Start Run":
            return "start_run"
        if selected == "Shop":
            return "open_shop"
        if selected == "Settings":
            return "open_settings"
        if selected == "Quit":
            return "quit"
        return None

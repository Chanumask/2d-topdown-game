import pygame

from game.core.snapshot import WorldSnapshot
from game.input.menu_actions import MenuActions
from game.ui.widgets import (
    build_centered_menu_rects,
    draw_centered_text,
    draw_menu_buttons,
    hovered_index,
)


class PauseMenuScreen:
    def __init__(self) -> None:
        self.options = ["Ready", "Settings", "Return to Main Menu"]
        self.selected_index = 0
        self.hover_index: int | None = None

    def handle_input(
        self,
        actions: MenuActions,
        surface: pygame.Surface,
        body_font: pygame.font.Font,
    ) -> str | None:
        _, _, menu_start, row_height = self._layout_metrics(surface)
        option_rects = build_centered_menu_rects(
            surface=surface,
            font=body_font,
            options=self.options,
            start_y=menu_start,
            row_height=row_height,
            min_width=max(300, surface.get_width() // 3),
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

        return None

    def render(
        self,
        surface: pygame.Surface,
        snapshot: WorldSnapshot,
        local_player_id: str,
        title_font: pygame.font.Font,
        body_font: pygame.font.Font,
    ) -> None:
        session = snapshot.session
        ready_list = session.get("ready_player_ids", [])
        ready_player_ids = set(ready_list) if isinstance(ready_list, list) else set()

        local_ready = local_player_id in ready_player_ids
        dynamic_options = self.options.copy()
        if local_ready:
            dynamic_options[0] = "Ready (Sent)"

        title_y, info_y, menu_start, row_height = self._layout_metrics(surface)
        option_rects = build_centered_menu_rects(
            surface=surface,
            font=body_font,
            options=dynamic_options,
            start_y=menu_start,
            row_height=row_height,
            min_width=max(300, surface.get_width() // 3),
        )

        draw_centered_text(surface, title_font, "Paused", title_y, (250, 250, 250))
        draw_centered_text(
            surface,
            body_font,
            f"Ready Players: {len(ready_player_ids)} / {len(snapshot.players)}",
            info_y,
            (220, 220, 220),
        )
        draw_centered_text(
            surface,
            body_font,
            "All players must press Ready to resume countdown.",
            info_y + 32,
            (190, 190, 190),
        )

        draw_menu_buttons(
            surface=surface,
            font=body_font,
            options=dynamic_options,
            rects=option_rects,
            selected_index=self.selected_index,
            hover_index=self.hover_index,
            normal_color=(210, 210, 210),
            selected_color=(255, 235, 120),
        )

    def _layout_metrics(self, surface: pygame.Surface) -> tuple[int, int, int, int]:
        height = surface.get_height()
        title_y = max(86, height // 5)
        info_y = title_y + 54
        row_height = max(46, min(64, height // 10))
        menu_start = info_y + 110
        return title_y, info_y, menu_start, row_height

    def _command_for_selection(self) -> str | None:
        selected = self.options[self.selected_index]
        if selected == "Ready":
            return "ready"
        if selected == "Settings":
            return "open_settings"
        if selected == "Return to Main Menu":
            return "return_main_menu"
        return None

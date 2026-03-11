import pygame

from game.core.profile import PlayerProfile
from game.core.run_result import RunResult
from game.input.menu_actions import MenuActions
from game.ui.widgets import (
    build_centered_menu_rects,
    draw_centered_text,
    draw_menu_buttons,
    hovered_index,
)


class GameOverScreen:
    def __init__(self) -> None:
        self.options = ["Start New Run", "Main Menu"]
        self.selected_index = 0
        self.hover_index: int | None = None

    def handle_input(
        self,
        actions: MenuActions,
        surface: pygame.Surface,
        body_font: pygame.font.Font,
    ) -> str | None:
        _, menu_start, row_height = self._layout_metrics(surface)
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

        if actions.back:
            return "main_menu"
        return None

    def render(
        self,
        surface: pygame.Surface,
        run_result: RunResult | None,
        profile: PlayerProfile,
        title_font: pygame.font.Font,
        body_font: pygame.font.Font,
    ) -> None:
        total_run_coins = run_result.total_run_coins if run_result else 0
        enemies_killed = run_result.enemies_killed_total if run_result else 0
        survival_time = run_result.survival_time_seconds if run_result else 0.0
        _, menu_start, row_height = self._layout_metrics(surface)
        option_rects = build_centered_menu_rects(
            surface=surface,
            font=body_font,
            options=self.options,
            start_y=menu_start,
            row_height=row_height,
            min_width=max(300, surface.get_width() // 3),
        )

        draw_centered_text(surface, title_font, "Game Over", 110, (245, 122, 122))
        draw_centered_text(
            surface,
            body_font,
            f"Survival Time: {survival_time:.1f}s",
            150,
            (225, 225, 225),
        )
        draw_centered_text(
            surface,
            body_font,
            f"Run Coins Earned: {total_run_coins}",
            180,
            (225, 225, 225),
        )
        draw_centered_text(
            surface,
            body_font,
            f"Enemies Killed: {enemies_killed}",
            210,
            (225, 225, 225),
        )
        draw_centered_text(
            surface,
            body_font,
            f"Persistent Meta Currency: {profile.meta_currency}",
            240,
            (225, 225, 225),
        )
        draw_centered_text(
            surface,
            body_font,
            f"Meta Currency Gained: +{total_run_coins}",
            270,
            (200, 230, 200),
        )
        draw_centered_text(
            surface,
            body_font,
            "Results are based on authoritative simulation data.",
            300,
            (190, 190, 190),
        )

        draw_menu_buttons(
            surface=surface,
            font=body_font,
            options=self.options,
            rects=option_rects,
            selected_index=self.selected_index,
            hover_index=self.hover_index,
            normal_color=(210, 210, 210),
            selected_color=(255, 235, 120),
        )

    def _layout_metrics(self, surface: pygame.Surface) -> tuple[int, int, int]:
        height = surface.get_height()
        title_y = max(96, height // 6)
        row_height = max(46, min(62, height // 10))
        menu_start = max(title_y + 250, height - (row_height * 2) - 64)
        return title_y, menu_start, row_height

    def _command_for_selection(self) -> str:
        if self.selected_index == 0:
            return "start_new_run"
        return "main_menu"

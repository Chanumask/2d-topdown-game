from dataclasses import dataclass
from enum import StrEnum


class AppScreen(StrEnum):
    MAIN_MENU = "main_menu"
    SHOP = "shop"
    SETTINGS = "settings"
    IN_RUN = "in_run"
    PAUSE_COUNTDOWN = "pause_countdown"
    PAUSED = "paused"
    RESUME_COUNTDOWN = "resume_countdown"
    GAME_OVER = "game_over"


@dataclass(slots=True)
class AppState:
    current_screen: AppScreen = AppScreen.MAIN_MENU
    settings_return_screen: AppScreen = AppScreen.MAIN_MENU
    current_run_banked: bool = False
    running: bool = True

    def open_settings(self) -> None:
        self.settings_return_screen = self.current_screen
        self.current_screen = AppScreen.SETTINGS

    def close_settings(self) -> None:
        self.current_screen = self.settings_return_screen

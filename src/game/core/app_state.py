from dataclasses import dataclass
from enum import StrEnum


class AppScreen(StrEnum):
    MAIN_MENU = "main_menu"
    LOBBY = "lobby"
    SHOP = "shop"
    SETTINGS = "settings"
    LOGBOOK = "logbook"
    IN_RUN = "in_run"
    PAUSE_COUNTDOWN = "pause_countdown"
    PAUSED = "paused"
    RESUME_COUNTDOWN = "resume_countdown"
    GAME_OVER = "game_over"


@dataclass(slots=True)
class AppState:
    current_screen: AppScreen = AppScreen.MAIN_MENU
    settings_return_screen: AppScreen = AppScreen.MAIN_MENU
    logbook_return_screen: AppScreen = AppScreen.MAIN_MENU
    selected_character_id: str = ""
    selected_map_id: str = ""
    selected_ability_id: str = ""
    selected_ability_variant_id: str = ""
    current_run_banked: bool = False
    running: bool = True

    def open_settings(self) -> None:
        self.settings_return_screen = self.current_screen
        self.current_screen = AppScreen.SETTINGS

    def close_settings(self) -> None:
        self.current_screen = self.settings_return_screen

    def open_logbook(self) -> None:
        self.logbook_return_screen = self.current_screen
        self.current_screen = AppScreen.LOGBOOK

    def close_logbook(self) -> None:
        self.current_screen = self.logbook_return_screen

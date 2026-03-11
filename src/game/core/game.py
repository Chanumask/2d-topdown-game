import pygame

from game.core.app_state import AppScreen, AppState
from game.core.gameloop import GameLoop
from game.core.profile_store import ProfileStore
from game.core.run_result import RunResult
from game.core.session_state import MatchPhase
from game.core.upgrades import build_run_modifiers
from game.core.world import World
from game.input.input_handler import InputHandler
from game.input.menu_input_handler import MenuInputHandler
from game.input.session_actions import SessionActions
from game.render.camera import Camera
from game.render.renderer import Renderer
from game.settings import SETTINGS
from game.ui import (
    GameOverScreen,
    MainMenuScreen,
    PauseMenuScreen,
    SettingsScreen,
    ShopScreen,
)
from game.ui.widgets import draw_centered_text


class GameApp:
    def __init__(self) -> None:
        self.local_player_id = "player-1"

        self.app_state = AppState()
        self.profile_store = ProfileStore()
        self.profile = self.profile_store.load_or_create_profile()

        self.screen = self._apply_display_mode()
        self.clock = pygame.time.Clock()
        self.title_font = pygame.font.Font(None, 52)
        self.body_font = pygame.font.Font(None, 30)

        self.game_input = InputHandler(local_player_id=self.local_player_id)
        self.menu_input = MenuInputHandler()

        self.main_menu = MainMenuScreen()
        self.shop_menu = ShopScreen()
        self.settings_menu = SettingsScreen()
        self.pause_menu = PauseMenuScreen()
        self.game_over_menu = GameOverScreen()

        self.camera = Camera(
            screen_width=self.screen.get_width(),
            screen_height=self.screen.get_height(),
            world_width=SETTINGS.world_width,
            world_height=SETTINGS.world_height,
        )
        self.renderer = Renderer(
            screen=self.screen,
            camera=self.camera,
            settings=SETTINGS,
            local_player_id=self.local_player_id,
        )

        self.world: World | None = None
        self.run_loop: GameLoop | None = None
        self.current_run_result: RunResult | None = None

    def run(self) -> None:
        while self.app_state.running:
            frame_dt = self.clock.tick(SETTINGS.max_render_fps) / 1000.0
            events = pygame.event.get()

            if self.app_state.current_screen in (
                AppScreen.MAIN_MENU,
                AppScreen.SHOP,
                AppScreen.SETTINGS,
            ):
                self._handle_non_run_screens(events)
                self._render_non_run_screen()
            else:
                self._handle_run_screens(events, frame_dt)
                self._render_run_screen()

            pygame.display.flip()

    def _handle_non_run_screens(self, events: list[pygame.event.Event]) -> None:
        menu_actions = self.menu_input.collect(events)
        if menu_actions.quit_requested:
            self._save_profile()
            self.app_state.running = False
            return

        if self.app_state.current_screen is AppScreen.MAIN_MENU:
            command = self.main_menu.handle_input(
                menu_actions,
                self.screen,
                self.body_font,
            )
            if command == "start_run":
                self._start_new_run()
            elif command == "open_shop":
                self.app_state.current_screen = AppScreen.SHOP
            elif command == "open_settings":
                self.app_state.open_settings()
            elif command == "quit":
                self._save_profile()
                self.app_state.running = False

        elif self.app_state.current_screen is AppScreen.SHOP:
            command, changed_profile = self.shop_menu.handle_input(
                menu_actions,
                self.profile,
                self.screen,
            )
            if changed_profile:
                self._save_profile()
            if command == "back":
                self.app_state.current_screen = AppScreen.MAIN_MENU

        elif self.app_state.current_screen is AppScreen.SETTINGS:
            before = self.profile.settings.to_dict()
            command = self.settings_menu.handle_input(
                menu_actions,
                self.profile.settings,
                self.screen,
            )
            after = self.profile.settings.to_dict()
            if after != before:
                self._save_profile()
                if before.get("fullscreen") != after.get("fullscreen"):
                    self.screen = self._apply_display_mode()
            if command == "back":
                self.app_state.close_settings()

    def _handle_run_screens(self, events: list[pygame.event.Event], frame_dt: float) -> None:
        if self.world is None or self.run_loop is None:
            self.app_state.current_screen = AppScreen.MAIN_MENU
            return

        if self.app_state.current_screen in (
            AppScreen.IN_RUN,
            AppScreen.PAUSE_COUNTDOWN,
            AppScreen.RESUME_COUNTDOWN,
        ):
            gameplay_input = self.game_input.collect(events)
            if gameplay_input.quit_requested:
                self._save_profile()
                self.app_state.running = False
                return

            self.run_loop.set_player_actions(gameplay_input.actions_by_player)
            for player_id, session_actions in gameplay_input.session_actions_by_player.items():
                self.world.apply_session_actions(player_id, session_actions)

            self.run_loop.advance(frame_dt)

        elif self.app_state.current_screen is AppScreen.PAUSED:
            menu_actions = self.menu_input.collect(events)
            if menu_actions.quit_requested:
                self._save_profile()
                self.app_state.running = False
                return

            command = self.pause_menu.handle_input(
                menu_actions,
                self.screen,
                self.body_font,
            )
            if command == "ready":
                self.world.apply_session_actions(
                    self.local_player_id,
                    SessionActions(ready_up=True),
                )
            elif command == "open_settings":
                self.app_state.open_settings()
                return
            elif command == "return_main_menu":
                self._return_to_main_menu_from_run()
                return

            self.run_loop.advance(frame_dt)

        elif self.app_state.current_screen is AppScreen.GAME_OVER:
            menu_actions = self.menu_input.collect(events)
            if menu_actions.quit_requested:
                self._save_profile()
                self.app_state.running = False
                return

            command = self.game_over_menu.handle_input(
                menu_actions,
                self.screen,
                self.body_font,
            )
            if command == "start_new_run":
                self._start_new_run()
                return
            if command == "main_menu":
                self._return_to_main_menu_from_run()
                return

        self._sync_run_screen_from_session()

    def _render_non_run_screen(self) -> None:
        self.screen.fill((16, 20, 24))

        if self.app_state.current_screen is AppScreen.MAIN_MENU:
            self.main_menu.render(self.screen, self.title_font, self.body_font)
        elif self.app_state.current_screen is AppScreen.SHOP:
            self.shop_menu.render(self.screen, self.profile, self.title_font, self.body_font)
        elif self.app_state.current_screen is AppScreen.SETTINGS:
            self.settings_menu.render(
                self.screen,
                self.profile.settings,
                self.title_font,
                self.body_font,
            )

    def _render_run_screen(self) -> None:
        if self.world is None:
            self.screen.fill((16, 20, 24))
            return

        snapshot = self.world.snapshot()
        self.renderer.render(snapshot)

        if self.app_state.current_screen is AppScreen.PAUSE_COUNTDOWN:
            self._draw_overlay_alpha(90)
            remaining = float(snapshot.session.get("countdown_remaining", 0.0))
            requester = snapshot.session.get("pause_requested_by")
            draw_centered_text(
                self.screen,
                self.title_font,
                f"Pause in {remaining:.1f}",
                180,
                (255, 230, 120),
            )
            draw_centered_text(
                self.screen,
                self.body_font,
                f"Requested by: {requester}",
                225,
                (230, 230, 230),
            )

        elif self.app_state.current_screen is AppScreen.PAUSED:
            self._draw_overlay_alpha(150)
            self.pause_menu.render(
                self.screen,
                snapshot,
                self.local_player_id,
                self.title_font,
                self.body_font,
            )

        elif self.app_state.current_screen is AppScreen.RESUME_COUNTDOWN:
            self._draw_overlay_alpha(100)
            remaining = float(snapshot.session.get("countdown_remaining", 0.0))
            draw_centered_text(
                self.screen,
                self.title_font,
                f"Resume in {remaining:.1f}",
                190,
                (150, 240, 150),
            )
            draw_centered_text(
                self.screen,
                self.body_font,
                "All players are ready.",
                235,
                (225, 225, 225),
            )

        elif self.app_state.current_screen is AppScreen.GAME_OVER:
            self._draw_overlay_alpha(170)
            self.game_over_menu.render(
                self.screen,
                self.current_run_result,
                self.profile,
                self.title_font,
                self.body_font,
            )

    def _start_new_run(self) -> None:
        run_modifiers = build_run_modifiers(self.profile.upgrades)
        self.world = World(
            settings=SETTINGS,
            world_width=SETTINGS.world_width,
            world_height=SETTINGS.world_height,
            run_modifiers=run_modifiers,
        )
        self.world.add_player(self.local_player_id)

        self.run_loop = GameLoop(
            world=self.world,
            simulation_hz=SETTINGS.simulation_hz,
            max_catchup_steps=SETTINGS.max_catchup_steps,
        )
        self.app_state.current_run_banked = False
        self.current_run_result = None
        self.app_state.current_screen = AppScreen.IN_RUN

    def _return_to_main_menu_from_run(self) -> None:
        self.world = None
        self.run_loop = None
        self.current_run_result = None
        self.app_state.current_screen = AppScreen.MAIN_MENU
        self.app_state.current_run_banked = False

    def _sync_run_screen_from_session(self) -> None:
        if self.world is None:
            return

        phase = self.world.session.phase
        mapped = AppScreen.IN_RUN
        if phase is MatchPhase.PAUSE_COUNTDOWN:
            mapped = AppScreen.PAUSE_COUNTDOWN
        elif phase is MatchPhase.PAUSED:
            mapped = AppScreen.PAUSED
        elif phase is MatchPhase.RESUME_COUNTDOWN:
            mapped = AppScreen.RESUME_COUNTDOWN
        elif phase is MatchPhase.GAME_OVER:
            mapped = AppScreen.GAME_OVER

        if phase is MatchPhase.GAME_OVER and not self.app_state.current_run_banked:
            run_result = self.world.get_run_result()
            if run_result is not None:
                self.current_run_result = run_result
                self.profile.bank_run_result(run_result)
                self._save_profile()
                self.app_state.current_run_banked = True

        self.app_state.current_screen = mapped

    def _draw_overlay_alpha(self, alpha: int) -> None:
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, alpha))
        self.screen.blit(overlay, (0, 0))

    def _save_profile(self) -> None:
        self.profile_store.save_profile(self.profile)

    def _apply_display_mode(self) -> pygame.Surface:
        if self.profile.settings.fullscreen:
            screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode((SETTINGS.screen_width, SETTINGS.screen_height))

        pygame.display.set_caption(SETTINGS.title)

        if hasattr(self, "renderer"):
            self.renderer.set_screen(screen)
        if hasattr(self, "camera"):
            self.camera.set_viewport(screen.get_width(), screen.get_height())

        return screen

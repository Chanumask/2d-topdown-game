import math

import pygame

from game.audio.audio_manager import AudioManager
from game.core.app_state import AppScreen, AppState
from game.core.gameloop import GameLoop
from game.core.lobby import (
    CharacterOption,
    MapOption,
    cycle_selected_id,
    list_character_options,
    list_map_options,
    resolve_selected_id,
)
from game.core.profile_store import ProfileStore
from game.core.run_result import RunResult
from game.core.session_state import MatchPhase
from game.core.upgrades import build_run_modifiers
from game.core.world import World
from game.input.actions import PlayerActions
from game.input.input_handler import InputHandler
from game.input.menu_input_handler import MenuInputHandler
from game.input.session_actions import SessionActions
from game.render.camera import Camera
from game.render.fonts import UIFonts, load_ui_fonts
from game.render.renderer import Renderer
from game.settings import SETTINGS
from game.ui import (
    GameOverScreen,
    LobbyScreen,
    MainMenuScreen,
    PauseMenuScreen,
    SettingsScreen,
    ShopScreen,
)
from game.ui.widgets import draw_centered_text

MENU_MUSIC_SCREENS = frozenset(
    {
        AppScreen.MAIN_MENU,
        AppScreen.LOBBY,
        AppScreen.SHOP,
        AppScreen.SETTINGS,
        AppScreen.GAME_OVER,
    }
)


class GameApp:
    def __init__(self) -> None:
        self.local_player_id = "player-1"

        self.app_state = AppState()
        self.profile_store = ProfileStore()
        self.profile = self.profile_store.load_or_create_profile()
        self.audio = AudioManager()
        self.audio.apply_settings(self.profile.settings)

        self.screen = self._apply_display_mode()
        self.clock = pygame.time.Clock()
        self.ui_fonts: UIFonts = load_ui_fonts()
        self.title_font = self.ui_fonts.title
        self.body_font = self.ui_fonts.body
        self.small_font = self.ui_fonts.small

        self.game_input = InputHandler(local_player_id=self.local_player_id)
        self.menu_input = MenuInputHandler()

        self.main_menu = MainMenuScreen()
        self.lobby_menu = LobbyScreen()
        self.shop_menu = ShopScreen()
        self.settings_menu = SettingsScreen()
        self.pause_menu = PauseMenuScreen()
        self.game_over_menu = GameOverScreen()
        self.character_options: list[CharacterOption] = list_character_options()
        self.map_options: list[MapOption] = list_map_options()
        self.app_state.selected_character_id = resolve_selected_id(
            self.character_options,
            SETTINGS.default_player_character_id,
            id_getter=lambda option: option.character_id,
        )
        self.app_state.selected_map_id = resolve_selected_id(
            self.map_options,
            "ashland_map",
            id_getter=lambda option: option.map_id,
        )

        self.camera = Camera(
            screen_width=self.screen.get_width(),
            screen_height=self.screen.get_height(),
            world_width=SETTINGS.world_width,
            world_height=SETTINGS.world_height,
            dead_zone_width_ratio=SETTINGS.camera_dead_zone_width_ratio,
            dead_zone_height_ratio=SETTINGS.camera_dead_zone_height_ratio,
        )
        self.renderer = Renderer(
            screen=self.screen,
            camera=self.camera,
            settings=SETTINGS,
            local_player_id=self.local_player_id,
            fonts=self.ui_fonts,
        )

        self.world: World | None = None
        self.run_loop: GameLoop | None = None
        self.current_run_result: RunResult | None = None
        self._countdown_audio_phase: MatchPhase | None = None
        self._countdown_audio_second: int | None = None

        # Start menu music immediately on boot.
        self._sync_music_for_current_screen()

    def run(self) -> None:
        while self.app_state.running:
            self._sync_music_for_current_screen()
            frame_dt = self.clock.tick(SETTINGS.max_render_fps) / 1000.0
            events = pygame.event.get()

            if self.app_state.current_screen in (
                AppScreen.MAIN_MENU,
                AppScreen.LOBBY,
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
            previous_index = self.main_menu.selected_index
            command = self.main_menu.handle_input(
                menu_actions,
                self.screen,
                self.body_font,
            )
            self._play_menu_audio_feedback(
                previous_index=previous_index,
                current_index=self.main_menu.selected_index,
                selected_or_clicked=menu_actions.select
                or (menu_actions.mouse_left_click and self.main_menu.hover_index is not None),
            )
            if command == "start_run":
                self.app_state.current_screen = AppScreen.LOBBY
            elif command == "open_shop":
                self.app_state.current_screen = AppScreen.SHOP
            elif command == "open_settings":
                self.app_state.open_settings()
            elif command == "quit":
                self._save_profile()
                self.app_state.running = False

        elif self.app_state.current_screen is AppScreen.LOBBY:
            previous_index = self.lobby_menu.selected_index
            command = self.lobby_menu.handle_input(
                menu_actions,
                self.screen,
                self.body_font,
                selected_character_name=self._selected_character_name(),
                selected_map_name=self._selected_map_name(),
            )
            self._play_menu_audio_feedback(
                previous_index=previous_index,
                current_index=self.lobby_menu.selected_index,
                selected_or_clicked=(
                    menu_actions.select
                    or menu_actions.mouse_left_click
                    or menu_actions.navigate_left
                    or menu_actions.navigate_right
                ),
            )
            if command == "character_prev":
                self._cycle_lobby_character(step=-1)
            elif command == "character_next":
                self._cycle_lobby_character(step=1)
            elif command == "map_prev":
                self._cycle_lobby_map(step=-1)
            elif command == "map_next":
                self._cycle_lobby_map(step=1)
            elif command == "start_run":
                self._start_new_run()
            elif command == "back_main_menu":
                self.app_state.current_screen = AppScreen.MAIN_MENU

        elif self.app_state.current_screen is AppScreen.SHOP:
            previous_index = self.shop_menu.selected_index
            command, changed_profile = self.shop_menu.handle_input(
                menu_actions,
                self.profile,
                self.screen,
            )
            self._play_menu_audio_feedback(
                previous_index=previous_index,
                current_index=self.shop_menu.selected_index,
                selected_or_clicked=menu_actions.select or menu_actions.mouse_left_click,
            )
            if changed_profile:
                self._save_profile()
            if command == "back":
                self.app_state.current_screen = AppScreen.MAIN_MENU

        elif self.app_state.current_screen is AppScreen.SETTINGS:
            previous_index = self.settings_menu.selected_index
            before = self.profile.settings.to_dict()
            command = self.settings_menu.handle_input(
                menu_actions,
                self.profile.settings,
                self.screen,
            )
            self._play_menu_audio_feedback(
                previous_index=previous_index,
                current_index=self.settings_menu.selected_index,
                selected_or_clicked=menu_actions.select or menu_actions.mouse_left_click,
            )
            after = self.profile.settings.to_dict()
            if after != before:
                self._save_profile()
                self.audio.apply_settings(self.profile.settings)
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

            self._sync_camera_to_world_focus()
            simulation_actions = self._prepare_gameplay_actions(gameplay_input.actions_by_player)
            self.run_loop.set_player_actions(simulation_actions)
            for player_id, session_actions in gameplay_input.session_actions_by_player.items():
                self.world.apply_session_actions(player_id, session_actions)

            previous_attack_tick, previous_coin_count = self._local_player_progress()
            self.run_loop.advance(frame_dt)
            current_attack_tick, current_coin_count = self._local_player_progress()
            if current_attack_tick > previous_attack_tick:
                self.audio.play_player_rock_throw()
            if current_coin_count > previous_coin_count:
                self.audio.play_world_coin_pickup()
            self._play_countdown_tick_audio()

        elif self.app_state.current_screen is AppScreen.PAUSED:
            menu_actions = self.menu_input.collect(events)
            if menu_actions.quit_requested:
                self._save_profile()
                self.app_state.running = False
                return

            previous_index = self.pause_menu.selected_index
            command = self.pause_menu.handle_input(
                menu_actions,
                self.screen,
                self.body_font,
            )
            self._play_menu_audio_feedback(
                previous_index=previous_index,
                current_index=self.pause_menu.selected_index,
                selected_or_clicked=menu_actions.select
                or (menu_actions.mouse_left_click and self.pause_menu.hover_index is not None),
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
            self._play_countdown_tick_audio()

        elif self.app_state.current_screen is AppScreen.GAME_OVER:
            menu_actions = self.menu_input.collect(events)
            if menu_actions.quit_requested:
                self._save_profile()
                self.app_state.running = False
                return

            previous_index = self.game_over_menu.selected_index
            command = self.game_over_menu.handle_input(
                menu_actions,
                self.screen,
                self.body_font,
            )
            self._play_menu_audio_feedback(
                previous_index=previous_index,
                current_index=self.game_over_menu.selected_index,
                selected_or_clicked=menu_actions.select
                or (menu_actions.mouse_left_click and self.game_over_menu.hover_index is not None),
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
        elif self.app_state.current_screen is AppScreen.LOBBY:
            self.lobby_menu.render(
                self.screen,
                self.title_font,
                self.body_font,
                selected_character_name=self._selected_character_name(),
                selected_map_name=self._selected_map_name(),
                character_count=len(self.character_options),
                map_count=len(self.map_options),
            )
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
        selected_character_id = resolve_selected_id(
            self.character_options,
            self.app_state.selected_character_id,
            id_getter=lambda option: option.character_id,
        )
        if selected_character_id:
            self.app_state.selected_character_id = selected_character_id
        else:
            selected_character_id = SETTINGS.default_player_character_id

        selected_map_id = resolve_selected_id(
            self.map_options,
            self.app_state.selected_map_id,
            id_getter=lambda option: option.map_id,
        )
        if selected_map_id:
            self.app_state.selected_map_id = selected_map_id
            try:
                self.renderer.set_active_map(selected_map_id)
            except Exception as error:
                print(f"[Lobby] Failed to load map '{selected_map_id}': {error}")
                fallback_map_id = (
                    self.map_options[0].map_id
                    if self.map_options
                    else self.app_state.selected_map_id
                )
                if fallback_map_id:
                    self.app_state.selected_map_id = fallback_map_id
                    self.renderer.set_active_map(fallback_map_id)

        run_modifiers = build_run_modifiers(self.profile.upgrades)
        fixed_map = self.renderer.ground_layer.fixed_map
        map_world_width = float(fixed_map.cols * fixed_map.tile_size)
        map_world_height = float(fixed_map.rows * fixed_map.tile_size)
        run_world_width = max(
            map_world_width,
            float(self.screen.get_width()),
            SETTINGS.world_width,
        )
        run_world_height = max(
            map_world_height,
            float(self.screen.get_height()),
            SETTINGS.world_height,
        )
        self.world = World(
            settings=SETTINGS,
            world_width=run_world_width,
            world_height=run_world_height,
            blocking_grid=fixed_map.merged_blocking_grid,
            blocking_tile_size=float(fixed_map.tile_size),
            run_modifiers=run_modifiers,
        )
        self.world.add_player(
            self.local_player_id,
            character_id=selected_character_id,
        )
        self.camera.set_world_bounds(run_world_width, run_world_height)

        self.run_loop = GameLoop(
            world=self.world,
            simulation_hz=SETTINGS.simulation_hz,
            max_catchup_steps=SETTINGS.max_catchup_steps,
        )
        self.app_state.current_run_banked = False
        self.current_run_result = None
        self._countdown_audio_phase = None
        self._countdown_audio_second = None
        self.app_state.current_screen = AppScreen.IN_RUN

    def _return_to_main_menu_from_run(self) -> None:
        self.world = None
        self.run_loop = None
        self.current_run_result = None
        self._countdown_audio_phase = None
        self._countdown_audio_second = None
        self.app_state.current_screen = AppScreen.MAIN_MENU
        self.app_state.current_run_banked = False
        self.camera.set_world_bounds(SETTINGS.world_width, SETTINGS.world_height)

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

    def _sync_music_for_current_screen(self) -> None:
        if self.app_state.current_screen in MENU_MUSIC_SCREENS:
            self.audio.play_menu_music()
            return
        self.audio.play_gameplay_music()

    def _play_menu_audio_feedback(
        self,
        *,
        previous_index: int,
        current_index: int,
        selected_or_clicked: bool,
    ) -> None:
        if current_index != previous_index:
            self.audio.play_ui_hover()
        if selected_or_clicked:
            self.audio.play_ui_confirm()

    def _play_countdown_tick_audio(self) -> None:
        if self.world is None:
            self._countdown_audio_phase = None
            self._countdown_audio_second = None
            return

        phase = self.world.session.phase
        if phase not in {MatchPhase.PAUSE_COUNTDOWN, MatchPhase.RESUME_COUNTDOWN}:
            self._countdown_audio_phase = None
            self._countdown_audio_second = None
            return

        if self._countdown_audio_phase is not phase:
            self._countdown_audio_phase = phase
            self._countdown_audio_second = None

        remaining = max(0.0, float(self.world.session.countdown_remaining))
        current_second = math.ceil(remaining - 1e-6)
        if current_second <= 0:
            self._countdown_audio_second = 0
            return

        if self._countdown_audio_second != current_second:
            self.audio.play_ui_timer_tick()
            self._countdown_audio_second = current_second

    def _local_player_progress(self) -> tuple[int, int]:
        if self.world is None:
            return -1, 0
        player = self.world.players.get(self.local_player_id)
        if player is None:
            return -1, 0
        return player.last_attack_tick, player.coins

    def _selected_character_name(self) -> str:
        selected_id = self.app_state.selected_character_id
        for option in self.character_options:
            if option.character_id == selected_id:
                return option.display_name
        return "None"

    def _selected_map_name(self) -> str:
        selected_id = self.app_state.selected_map_id
        for option in self.map_options:
            if option.map_id == selected_id:
                return option.display_name
        return "None"

    def _cycle_lobby_character(self, *, step: int) -> None:
        self.app_state.selected_character_id = cycle_selected_id(
            self.character_options,
            self.app_state.selected_character_id,
            id_getter=lambda option: option.character_id,
            step=step,
        )

    def _cycle_lobby_map(self, *, step: int) -> None:
        self.app_state.selected_map_id = cycle_selected_id(
            self.map_options,
            self.app_state.selected_map_id,
            id_getter=lambda option: option.map_id,
            step=step,
        )

    def _prepare_gameplay_actions(
        self,
        actions_by_player: dict[str, PlayerActions],
    ) -> dict[str, PlayerActions]:
        transformed: dict[str, PlayerActions] = {}
        for player_id, actions in actions_by_player.items():
            aim_world = None
            if actions.aim_position is not None:
                aim_world = self.camera.screen_to_world(actions.aim_position)

            transformed[player_id] = PlayerActions(
                move_up=actions.move_up,
                move_down=actions.move_down,
                move_left=actions.move_left,
                move_right=actions.move_right,
                aim_position=aim_world,
                throw=actions.throw,
                throw_pressed=actions.throw_pressed,
                throw_held=actions.throw_held,
            )
        return transformed

    def _sync_camera_to_world_focus(self) -> None:
        if self.world is None:
            return

        focus_player = self.world.players.get(self.local_player_id)
        if focus_player is None:
            focus_player = next(iter(self.world.players.values()), None)

        focus_position = None
        if focus_player is not None:
            focus_position = (focus_player.position.x, focus_player.position.y)
        self.camera.update(focus_position)

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
            if self.world is not None:
                self.world.ensure_min_bounds(screen.get_width(), screen.get_height())
                self.camera.set_world_bounds(self.world.world_width, self.world.world_height)
            else:
                self.camera.set_world_bounds(SETTINGS.world_width, SETTINGS.world_height)

        return screen

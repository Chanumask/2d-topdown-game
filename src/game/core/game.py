import math
import warnings

import pygame

from game.active_abilities import list_active_abilities, resolve_ability_selection
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
from game.render.fonts import UIFonts, load_ui_fonts, scale_ui_fonts
from game.render.renderer import Renderer
from game.settings import SETTINGS
from game.ui import (
    GameOverScreen,
    LobbyScreen,
    LogbookScreen,
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
    _MIN_WINDOWED_WIDTH = 960
    _MIN_WINDOWED_HEIGHT = 600

    def __init__(self) -> None:
        self.local_player_id = "player-1"

        self.app_state = AppState()
        self.profile_store = ProfileStore()
        self.profile = self.profile_store.load_or_create_profile()
        self.audio = AudioManager()
        self.audio.apply_settings(self.profile.settings)
        self._windowed_size = self._clamp_windowed_size(self._compute_default_windowed_size())
        self._fullscreen_active = False

        self.screen = self._apply_display_mode()
        self.clock = pygame.time.Clock()
        self._base_ui_fonts: UIFonts = load_ui_fonts()
        self._responsive_font_cache: dict[tuple[int, int, int], UIFonts] = {}
        self.ui_fonts: UIFonts = self._base_ui_fonts
        self.title_font = self.ui_fonts.title
        self.body_font = self.ui_fonts.body
        self.small_font = self.ui_fonts.small

        self.game_input = InputHandler(
            local_player_id=self.local_player_id,
            settings=self.profile.settings,
        )
        self.menu_input = MenuInputHandler()

        self.main_menu = MainMenuScreen()
        self.lobby_menu = LobbyScreen()
        self.logbook_menu = LogbookScreen()
        self.shop_menu = ShopScreen()
        self.settings_menu = SettingsScreen()
        self.pause_menu = PauseMenuScreen()
        self.game_over_menu = GameOverScreen()
        self.character_options: list[CharacterOption] = list_character_options()
        self.map_options: list[MapOption] = list_map_options()
        self.ability_options = list_active_abilities()
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
        default_ability, default_variant = resolve_ability_selection("", "")
        self.app_state.selected_ability_id = default_ability.ability_id
        self.app_state.selected_ability_variant_id = default_variant.variant_id

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
        self._sync_active_fonts()

    def run(self) -> None:
        while self.app_state.running:
            self._sync_music_for_current_screen()
            frame_dt = self.clock.tick(SETTINGS.max_render_fps) / 1000.0
            events = pygame.event.get()
            self._handle_window_events(events)
            self._sync_active_fonts()

            if self.app_state.current_screen in (
                AppScreen.MAIN_MENU,
                AppScreen.LOBBY,
                AppScreen.LOGBOOK,
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
            elif command == "open_logbook":
                self.app_state.open_logbook()
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
                selected_character_id=self.app_state.selected_character_id,
                selected_map_name=self._selected_map_name(),
                selected_ability_id=self.app_state.selected_ability_id,
                selected_ability_name=self._selected_ability_name(),
                selected_variant_id=self.app_state.selected_ability_variant_id,
                selected_variant_name=self._selected_ability_variant_name(),
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
            elif command == "ability_prev":
                self._cycle_lobby_ability(step=-1)
            elif command == "ability_next":
                self._cycle_lobby_ability(step=1)
            elif command == "variant_prev":
                self._cycle_lobby_ability_variant(step=-1)
            elif command == "variant_next":
                self._cycle_lobby_ability_variant(step=1)
            elif isinstance(command, str) and command.startswith("variant_set:"):
                self._set_lobby_ability_variant(command.split(":", 1)[1])
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

        elif self.app_state.current_screen is AppScreen.LOGBOOK:
            previous_signature = self.logbook_menu.selection_signature()
            command = self.logbook_menu.handle_input(
                menu_actions,
                self.screen,
                self.profile,
            )
            current_signature = self.logbook_menu.selection_signature()
            self._play_menu_audio_feedback(
                previous_index=hash(previous_signature),
                current_index=hash(current_signature),
                selected_or_clicked=menu_actions.select or menu_actions.mouse_left_click,
            )
            if command == "back":
                self.app_state.close_logbook()

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
            self._update_logbook_progress_from_world()
            self._play_world_audio_events()
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
            elif command == "open_logbook":
                self.app_state.open_logbook()
                return
            elif command == "open_settings":
                self.app_state.open_settings()
                return
            elif command == "return_main_menu":
                self._return_to_main_menu_from_run()
                return

            self.run_loop.advance(frame_dt)
            self._update_logbook_progress_from_world()
            self._play_world_audio_events()
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
                selected_character_id=self.app_state.selected_character_id,
                selected_map_name=self._selected_map_name(),
                selected_ability_id=self.app_state.selected_ability_id,
                selected_ability_name=self._selected_ability_name(),
                selected_variant_id=self.app_state.selected_ability_variant_id,
                selected_variant_name=self._selected_ability_variant_name(),
                character_count=len(self.character_options),
                map_count=len(self.map_options),
                ability_count=len(self.ability_options),
                small_font=self.small_font,
            )
        elif self.app_state.current_screen is AppScreen.SHOP:
            self.shop_menu.render(
                self.screen,
                self.profile,
                self.title_font,
                self.body_font,
                self.small_font,
            )
        elif self.app_state.current_screen is AppScreen.LOGBOOK:
            self.logbook_menu.render(
                self.screen,
                self.profile,
                self.title_font,
                self.body_font,
                self.small_font,
            )
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
            active_ability_id=self.app_state.selected_ability_id,
            active_ability_variant_id=self.app_state.selected_ability_variant_id,
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
        if self.app_state.current_screen is AppScreen.LOGBOOK:
            if self.app_state.logbook_return_screen in {
                AppScreen.IN_RUN,
                AppScreen.PAUSE_COUNTDOWN,
                AppScreen.PAUSED,
                AppScreen.RESUME_COUNTDOWN,
                AppScreen.GAME_OVER,
            }:
                self.audio.play_gameplay_music()
                return
            self.audio.play_menu_music()
            return
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

    def _update_logbook_progress_from_world(self) -> None:
        if self.world is None:
            return

        changed = False
        for event in self.world.consume_profile_progress_events():
            event_kind = event.get("kind", "").strip()
            entry_id = event.get("id", "").strip()
            if not entry_id:
                continue

            if event_kind == "enemy":
                changed = self.profile.mark_enemy_encountered(entry_id) or changed
            elif event_kind == "blessing":
                changed = self.profile.mark_blessing_encountered(entry_id) or changed

        if changed:
            self._save_profile()

    def _play_world_audio_events(self) -> None:
        if self.world is None:
            return

        for event in self.world.consume_audio_events():
            sfx_key = str(event.get("sfx_key", "")).strip()
            if not sfx_key:
                continue
            self.audio.play_sfx(sfx_key)

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

    def _selected_ability_name(self) -> str:
        ability, _ = resolve_ability_selection(
            self.app_state.selected_ability_id,
            self.app_state.selected_ability_variant_id,
        )
        self.app_state.selected_ability_id = ability.ability_id
        return ability.display_name

    def _selected_ability_variant_name(self) -> str:
        ability, variant = resolve_ability_selection(
            self.app_state.selected_ability_id,
            self.app_state.selected_ability_variant_id,
        )
        self.app_state.selected_ability_id = ability.ability_id
        self.app_state.selected_ability_variant_id = variant.variant_id
        return f"{variant.display_name} ({variant.description})"

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

    def _cycle_lobby_ability(self, *, step: int) -> None:
        if not self.ability_options:
            return
        ability_ids = [ability.ability_id for ability in self.ability_options]
        current_id = self.app_state.selected_ability_id
        if current_id not in ability_ids:
            current_id = ability_ids[0]
        current_index = ability_ids.index(current_id)
        next_ability = self.ability_options[(current_index + step) % len(self.ability_options)]
        self.app_state.selected_ability_id = next_ability.ability_id
        self.app_state.selected_ability_variant_id = next_ability.variants[0].variant_id

    def _cycle_lobby_ability_variant(self, *, step: int) -> None:
        ability, variant = resolve_ability_selection(
            self.app_state.selected_ability_id,
            self.app_state.selected_ability_variant_id,
        )
        variants = list(ability.variants)
        current_index = variants.index(variant)
        next_variant = variants[(current_index + step) % len(variants)]
        self.app_state.selected_ability_id = ability.ability_id
        self.app_state.selected_ability_variant_id = next_variant.variant_id

    def _set_lobby_ability_variant(self, variant_id: str) -> None:
        ability, variant = resolve_ability_selection(
            self.app_state.selected_ability_id,
            variant_id,
        )
        self.app_state.selected_ability_id = ability.ability_id
        self.app_state.selected_ability_variant_id = variant.variant_id

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
                activate_ability=actions.activate_ability,
                activate_ability_pressed=actions.activate_ability_pressed,
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
        target_fullscreen = bool(self.profile.settings.fullscreen)
        current_surface = pygame.display.get_surface()
        if target_fullscreen and not self._fullscreen_active and current_surface is not None:
            self._windowed_size = self._clamp_windowed_size(current_surface.get_size())

        flags = pygame.FULLSCREEN if target_fullscreen else pygame.RESIZABLE
        size = (0, 0) if target_fullscreen else self._clamp_windowed_size(self._windowed_size)
        with warnings.catch_warnings():
            warnings.filterwarnings(
                "ignore",
                message="Requested window was forcibly resized by the OS\\.",
                category=RuntimeWarning,
            )
            screen = pygame.display.set_mode(size, flags)

        self._fullscreen_active = target_fullscreen
        if not target_fullscreen:
            self._windowed_size = self._clamp_windowed_size(screen.get_size())

        pygame.display.set_caption(SETTINGS.title)
        self._sync_display_surface(screen)

        return screen

    def _compute_default_windowed_size(self) -> tuple[int, int]:
        desktop_sizes = pygame.display.get_desktop_sizes()
        if desktop_sizes:
            desktop_width, desktop_height = desktop_sizes[0]
        else:
            display_info = pygame.display.Info()
            desktop_width = max(SETTINGS.screen_width, int(display_info.current_w or 0))
            desktop_height = max(SETTINGS.screen_height, int(display_info.current_h or 0))

        usable_width = max(320, int(desktop_width) - 80)
        usable_height = max(240, int(desktop_height) - 120)
        target_width = min(usable_width, max(SETTINGS.screen_width, int(desktop_width * 0.88)))
        target_height = min(usable_height, max(SETTINGS.screen_height, int(desktop_height * 0.88)))
        return self._clamp_windowed_size((target_width, target_height))

    def _clamp_windowed_size(self, size: tuple[int, int]) -> tuple[int, int]:
        width, height = size
        return (
            max(self._MIN_WINDOWED_WIDTH, int(width)),
            max(self._MIN_WINDOWED_HEIGHT, int(height)),
        )

    def _fonts_for_surface(self) -> UIFonts:
        width = max(320, self.screen.get_width())
        height = max(240, self.screen.get_height())
        base_scale = min(width / SETTINGS.screen_width, height / SETTINGS.screen_height)
        body_scale = max(0.72, min(1.0, base_scale))
        title_scale = max(0.68, min(1.0, body_scale - 0.04))
        hud_scale = max(0.74, min(1.0, body_scale))
        key = (
            int(round(body_scale * 100)),
            int(round(title_scale * 100)),
            int(round(hud_scale * 100)),
        )
        cached = self._responsive_font_cache.get(key)
        if cached is not None:
            return cached

        responsive = scale_ui_fonts(
            self._base_ui_fonts,
            scale=body_scale,
            title_scale=title_scale,
            heading_scale=body_scale,
            hud_scale=hud_scale,
        )
        self._responsive_font_cache[key] = responsive
        return responsive

    def _sync_active_fonts(self) -> None:
        active_fonts = self._fonts_for_surface()
        self.ui_fonts = active_fonts
        self.title_font = active_fonts.title
        self.body_font = active_fonts.body
        self.small_font = active_fonts.small
        if hasattr(self, "renderer"):
            self.renderer.set_fonts(active_fonts)

    def _handle_window_events(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            if event.type in {
                pygame.WINDOWRESIZED,
                pygame.WINDOWSIZECHANGED,
                pygame.VIDEORESIZE,
            }:
                if not self._fullscreen_active:
                    width = int(
                        getattr(event, "x", 0) or getattr(event, "w", 0) or self.screen.get_width()
                    )
                    height = int(
                        getattr(event, "y", 0) or getattr(event, "h", 0) or self.screen.get_height()
                    )
                    clamped = self._clamp_windowed_size((width, height))
                    self._windowed_size = clamped
                    if (width, height) != clamped:
                        with warnings.catch_warnings():
                            warnings.filterwarnings(
                                "ignore",
                                message="Requested window was forcibly resized by the OS\\.",
                                category=RuntimeWarning,
                            )
                            resized_screen = pygame.display.set_mode(clamped, pygame.RESIZABLE)
                        self._sync_display_surface(resized_screen)
                        continue
                self._sync_display_surface(pygame.display.get_surface())

    def _sync_display_surface(self, screen: pygame.Surface | None) -> None:
        if screen is None:
            return

        self.screen = screen
        if hasattr(self, "renderer"):
            self.renderer.set_screen(screen)
        if hasattr(self, "camera"):
            self.camera.set_viewport(screen.get_width(), screen.get_height())
            if self.world is not None:
                self.world.ensure_min_bounds(screen.get_width(), screen.get_height())
                self.camera.set_world_bounds(self.world.world_width, self.world.world_height)
            else:
                self.camera.set_world_bounds(SETTINGS.world_width, SETTINGS.world_height)
        if hasattr(self, "_base_ui_fonts"):
            self._sync_active_fonts()

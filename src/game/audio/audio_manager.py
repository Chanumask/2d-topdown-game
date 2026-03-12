from __future__ import annotations

from pathlib import Path

import pygame

from game.audio.audio_assets import (
    MUSIC_ASSETS,
    MUSIC_GAMEPLAY,
    MUSIC_MENU,
    SFX_ASSETS,
    SFX_ENEMY_DEATH,
    SFX_ENEMY_HIT,
    SFX_PLAYER_ROCK_THROW,
    SFX_UI_CONFIRM,
    SFX_UI_HOVER,
    SFX_WORLD_COIN_PICKUP,
    AudioAsset,
)
from game.core.profile import UserSettings

PROJECT_ROOT = Path(__file__).resolve().parents[3]


class AudioManager:
    def __init__(self, project_root: Path = PROJECT_ROOT) -> None:
        self.project_root = project_root
        self.master_volume = 1.0
        self.music_volume = 1.0
        self.sfx_volume = 1.0

        self._sound_cache: dict[str, pygame.mixer.Sound | None] = {}
        self._missing_asset_logs: set[str] = set()
        self._current_music_key: str | None = None
        self._mixer_available = self._init_mixer()

    def apply_settings(self, settings: UserSettings) -> None:
        self.master_volume = _normalize_percent(settings.master_volume)
        self.music_volume = _normalize_percent(settings.music_volume)
        self.sfx_volume = _normalize_percent(settings.sfx_volume)

        if self._mixer_available:
            pygame.mixer.music.set_volume(self._effective_music_volume())

    def play_menu_music(self) -> bool:
        return self.play_music(MUSIC_MENU)

    def play_gameplay_music(self) -> bool:
        return self.play_music(MUSIC_GAMEPLAY)

    def stop_music(self) -> None:
        if not self._mixer_available:
            return
        pygame.mixer.music.stop()
        self._current_music_key = None

    def play_music(self, key: str, *, restart: bool = False) -> bool:
        if not self._mixer_available:
            return False
        asset = MUSIC_ASSETS.get(key)
        if asset is None:
            self._log_once(f"unknown_music:{key}", f"[Audio] Unknown music key: {key}")
            return False

        if self._current_music_key == key and pygame.mixer.music.get_busy() and not restart:
            return True

        resolved = self._resolve_asset_path(asset)
        if not resolved.exists():
            self._log_once(
                f"missing_music:{key}",
                f"[Audio] Missing music file: {asset.path}",
            )
            return False

        try:
            pygame.mixer.music.load(str(resolved))
            pygame.mixer.music.set_volume(self._effective_music_volume(asset.base_volume))
            pygame.mixer.music.play(-1)
            self._current_music_key = key
            return True
        except Exception as error:
            self._log_once(
                f"music_error:{key}",
                f"[Audio] Failed to play music '{key}': {error}",
            )
            return False

    def play_ui_hover(self) -> bool:
        return self.play_sfx(SFX_UI_HOVER)

    def play_ui_confirm(self) -> bool:
        return self.play_sfx(SFX_UI_CONFIRM)

    def play_player_rock_throw(self) -> bool:
        return self.play_sfx(SFX_PLAYER_ROCK_THROW)

    def play_world_coin_pickup(self) -> bool:
        return self.play_sfx(SFX_WORLD_COIN_PICKUP)

    def play_enemy_hit(self) -> bool:
        return self.play_sfx(SFX_ENEMY_HIT)

    def play_enemy_death(self) -> bool:
        return self.play_sfx(SFX_ENEMY_DEATH)

    def play_sfx(self, key: str) -> bool:
        if not self._mixer_available:
            return False

        asset = SFX_ASSETS.get(key)
        if asset is None:
            self._log_once(f"unknown_sfx:{key}", f"[Audio] Unknown SFX key: {key}")
            return False

        sound = self._load_sound(key, asset)
        if sound is None:
            return False

        sound.set_volume(self._effective_sfx_volume(asset.base_volume))
        sound.play()
        return True

    def _load_sound(self, key: str, asset: AudioAsset) -> pygame.mixer.Sound | None:
        if key in self._sound_cache:
            return self._sound_cache[key]

        resolved = self._resolve_asset_path(asset)
        if not resolved.exists():
            self._log_once(
                f"missing_sfx:{key}",
                f"[Audio] Missing SFX file: {asset.path}",
            )
            self._sound_cache[key] = None
            return None

        try:
            sound = pygame.mixer.Sound(str(resolved))
            self._sound_cache[key] = sound
            return sound
        except Exception as error:
            self._log_once(
                f"sfx_error:{key}",
                f"[Audio] Failed to load SFX '{key}': {error}",
            )
            self._sound_cache[key] = None
            return None

    def _resolve_asset_path(self, asset: AudioAsset) -> Path:
        return (self.project_root / asset.path).resolve()

    def _effective_music_volume(self, base: float = 1.0) -> float:
        return _clamp01(self.master_volume * self.music_volume * base)

    def _effective_sfx_volume(self, base: float = 1.0) -> float:
        return _clamp01(self.master_volume * self.sfx_volume * base)

    def _init_mixer(self) -> bool:
        try:
            if pygame.mixer.get_init() is None:
                pygame.mixer.init()
            return True
        except Exception as error:
            self._log_once(
                "mixer_init",
                f"[Audio] Mixer unavailable, audio disabled: {error}",
            )
            return False

    def _log_once(self, key: str, message: str) -> None:
        if key in self._missing_asset_logs:
            return
        self._missing_asset_logs.add(key)
        print(message)


def _normalize_percent(value: int | float) -> float:
    return _clamp01(float(value) / 100.0)


def _clamp01(value: float) -> float:
    return max(0.0, min(1.0, value))

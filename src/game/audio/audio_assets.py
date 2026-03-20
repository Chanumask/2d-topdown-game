from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class AudioAsset:
    key: str
    path: Path
    category: str
    base_volume: float = 1.0


def _asset(path: str) -> Path:
    return Path(path)


MUSIC_MENU = "music_menu"
MUSIC_GAMEPLAY = "music_gameplay"

SFX_UI_HOVER = "sfx_ui_hover"
SFX_UI_CONFIRM = "sfx_ui_confirm"
SFX_UI_TIMER_TICK = "sfx_ui_timer_tick"
SFX_PLAYER_ROCK_THROW = "sfx_player_rock_throw"
SFX_WORLD_COIN_PICKUP = "sfx_world_coin_pickup"
SFX_ENEMY_HIT = "sfx_enemy_hit"
SFX_ENEMY_DEATH = "sfx_enemy_death"
SFX_ENEMY_ELITE_SPAWN = "sfx_enemy_elite_spawn"
SFX_ENEMY_BOSS_SPAWN = "sfx_enemy_boss_spawn"

MUSIC_ASSETS: dict[str, AudioAsset] = {
    MUSIC_MENU: AudioAsset(
        key=MUSIC_MENU,
        path=_asset("assets/audio/music/menu.ogg"),
        category="music",
        base_volume=1.0,
    ),
    MUSIC_GAMEPLAY: AudioAsset(
        key=MUSIC_GAMEPLAY,
        path=_asset("assets/audio/music/gameplay.ogg"),
        category="music",
        base_volume=1.0,
    ),
}

SFX_ASSETS: dict[str, AudioAsset] = {
    SFX_UI_HOVER: AudioAsset(
        key=SFX_UI_HOVER,
        path=_asset("assets/audio/sfx/ui/button_hover.wav"),
        category="ui",
        base_volume=0.6,
    ),
    SFX_UI_CONFIRM: AudioAsset(
        key=SFX_UI_CONFIRM,
        path=_asset("assets/audio/sfx/ui/button_confirm.wav"),
        category="ui",
        base_volume=0.75,
    ),
    SFX_UI_TIMER_TICK: AudioAsset(
        key=SFX_UI_TIMER_TICK,
        path=_asset("assets/audio/sfx/ui/timer_tick.wav"),
        category="ui",
        base_volume=0.7,
    ),
    SFX_PLAYER_ROCK_THROW: AudioAsset(
        key=SFX_PLAYER_ROCK_THROW,
        path=_asset("assets/audio/sfx/player/rock_throw.wav"),
        category="player",
        base_volume=0.9,
    ),
    SFX_WORLD_COIN_PICKUP: AudioAsset(
        key=SFX_WORLD_COIN_PICKUP,
        path=_asset("assets/audio/sfx/world/coin_pickup.wav"),
        category="world",
        base_volume=0.8,
    ),
    SFX_ENEMY_HIT: AudioAsset(
        key=SFX_ENEMY_HIT,
        path=_asset("assets/audio/sfx/enemies/enemy_hit.wav"),
        category="enemies",
        base_volume=0.9,
    ),
    SFX_ENEMY_DEATH: AudioAsset(
        key=SFX_ENEMY_DEATH,
        path=_asset("assets/audio/sfx/enemies/enemy_death.wav"),
        category="enemies",
        base_volume=1.0,
    ),
    SFX_ENEMY_ELITE_SPAWN: AudioAsset(
        key=SFX_ENEMY_ELITE_SPAWN,
        path=_asset("assets/audio/sfx/enemies/elite_spawn.wav"),
        category="enemies",
        base_volume=1.0,
    ),
    SFX_ENEMY_BOSS_SPAWN: AudioAsset(
        key=SFX_ENEMY_BOSS_SPAWN,
        path=_asset("assets/audio/sfx/enemies/boss_spawn.wav"),
        category="enemies",
        base_volume=1.0,
    ),
}

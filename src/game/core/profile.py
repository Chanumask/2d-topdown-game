from dataclasses import dataclass, field

from game.core.run_result import RunResult
from game.core.upgrades import PurchaseResult, clamp_upgrade_levels, purchase_upgrade


@dataclass(slots=True)
class UserSettings:
    master_volume: int = 100
    music_volume: int = 80
    sfx_volume: int = 90
    fullscreen: bool = False
    mouse_sensitivity: float = 1.0
    activate_ability_key: str = "space"

    def to_dict(self) -> dict[str, object]:
        return {
            "master_volume": self.master_volume,
            "music_volume": self.music_volume,
            "sfx_volume": self.sfx_volume,
            "fullscreen": self.fullscreen,
            "mouse_sensitivity": self.mouse_sensitivity,
            "activate_ability_key": self.activate_ability_key,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, object]) -> "UserSettings":
        return cls(
            master_volume=int(payload.get("master_volume", 100)),
            music_volume=int(payload.get("music_volume", 80)),
            sfx_volume=int(payload.get("sfx_volume", 90)),
            fullscreen=bool(payload.get("fullscreen", False)),
            mouse_sensitivity=float(payload.get("mouse_sensitivity", 1.0)),
            activate_ability_key=str(payload.get("activate_ability_key", "space")),
        )


@dataclass(slots=True)
class LogbookProgress:
    encountered_enemy_ids: set[str] = field(default_factory=set)
    encountered_blessing_ids: set[str] = field(default_factory=set)

    def mark_enemy_encountered(self, enemy_id: str) -> bool:
        normalized = str(enemy_id).strip()
        if not normalized or normalized in self.encountered_enemy_ids:
            return False
        self.encountered_enemy_ids.add(normalized)
        return True

    def mark_blessing_encountered(self, blessing_id: str) -> bool:
        normalized = str(blessing_id).strip()
        if not normalized or normalized in self.encountered_blessing_ids:
            return False
        self.encountered_blessing_ids.add(normalized)
        return True

    def to_dict(self) -> dict[str, object]:
        return {
            "encountered_enemy_ids": sorted(self.encountered_enemy_ids),
            "encountered_blessing_ids": sorted(self.encountered_blessing_ids),
        }

    @classmethod
    def from_dict(cls, payload: dict[str, object]) -> "LogbookProgress":
        raw_enemy_ids = payload.get("encountered_enemy_ids", [])
        raw_blessing_ids = payload.get("encountered_blessing_ids", [])
        enemy_ids = {
            str(value).strip()
            for value in raw_enemy_ids
            if isinstance(value, str) and str(value).strip()
        }
        blessing_ids = {
            str(value).strip()
            for value in raw_blessing_ids
            if isinstance(value, str) and str(value).strip()
        }
        return cls(
            encountered_enemy_ids=enemy_ids,
            encountered_blessing_ids=blessing_ids,
        )


@dataclass(slots=True)
class PlayerProfile:
    profile_id: str = "local-profile"
    meta_currency: int = 0
    last_run_coins: int = 0
    last_run_survival_time_seconds: float = 0.0
    last_run_enemies_killed: int = 0
    last_run_result: dict[str, object] | None = None
    lifetime_meta_earned: int = 0
    lifetime_runs_completed: int = 0
    lifetime_enemies_killed: int = 0
    upgrades: dict[str, int] = field(default_factory=dict)
    settings: UserSettings = field(default_factory=UserSettings)
    logbook: LogbookProgress = field(default_factory=LogbookProgress)

    def bank_run_result(self, run_result: RunResult) -> None:
        coins = max(0, int(run_result.total_run_coins))
        enemies_killed = max(0, int(run_result.enemies_killed_total))

        self.last_run_coins = coins
        self.last_run_survival_time_seconds = float(run_result.survival_time_seconds)
        self.last_run_enemies_killed = enemies_killed
        self.last_run_result = run_result.to_dict()

        self.meta_currency += coins
        self.lifetime_meta_earned += coins
        self.lifetime_runs_completed += 1
        self.lifetime_enemies_killed += enemies_killed

    def purchase_upgrade(self, upgrade_id: str) -> PurchaseResult:
        return purchase_upgrade(self, upgrade_id)

    def mark_enemy_encountered(self, enemy_id: str) -> bool:
        return self.logbook.mark_enemy_encountered(enemy_id)

    def mark_blessing_encountered(self, blessing_id: str) -> bool:
        return self.logbook.mark_blessing_encountered(blessing_id)

    def to_dict(self) -> dict[str, object]:
        return {
            "profile_id": self.profile_id,
            "meta_currency": self.meta_currency,
            "last_run_coins": self.last_run_coins,
            "last_run_survival_time_seconds": self.last_run_survival_time_seconds,
            "last_run_enemies_killed": self.last_run_enemies_killed,
            "last_run_result": self.last_run_result,
            "lifetime_meta_earned": self.lifetime_meta_earned,
            "lifetime_runs_completed": self.lifetime_runs_completed,
            "lifetime_enemies_killed": self.lifetime_enemies_killed,
            "upgrades": clamp_upgrade_levels(self.upgrades),
            "settings": self.settings.to_dict(),
            "logbook": self.logbook.to_dict(),
        }

    @classmethod
    def from_dict(cls, payload: dict[str, object]) -> "PlayerProfile":
        raw_settings = payload.get("settings")
        raw_upgrades = payload.get("upgrades")
        raw_logbook = payload.get("logbook")
        settings_payload = raw_settings if isinstance(raw_settings, dict) else {}
        upgrades_payload = raw_upgrades if isinstance(raw_upgrades, dict) else {}
        logbook_payload = raw_logbook if isinstance(raw_logbook, dict) else {}
        parsed_upgrades: dict[str, int] = {}
        for key, value in upgrades_payload.items():
            try:
                parsed_upgrades[str(key)] = int(value)
            except (TypeError, ValueError):
                continue

        return cls(
            profile_id=str(payload.get("profile_id", "local-profile")),
            meta_currency=int(payload.get("meta_currency", 0)),
            last_run_coins=int(payload.get("last_run_coins", 0)),
            last_run_survival_time_seconds=float(
                payload.get("last_run_survival_time_seconds", 0.0)
            ),
            last_run_enemies_killed=int(payload.get("last_run_enemies_killed", 0)),
            last_run_result=(
                payload.get("last_run_result")
                if isinstance(payload.get("last_run_result"), dict)
                else None
            ),
            lifetime_meta_earned=int(payload.get("lifetime_meta_earned", 0)),
            lifetime_runs_completed=int(payload.get("lifetime_runs_completed", 0)),
            lifetime_enemies_killed=int(payload.get("lifetime_enemies_killed", 0)),
            upgrades=clamp_upgrade_levels(parsed_upgrades),
            settings=UserSettings.from_dict(settings_payload),
            logbook=LogbookProgress.from_dict(logbook_payload),
        )

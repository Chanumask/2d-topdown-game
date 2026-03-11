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

    def to_dict(self) -> dict[str, object]:
        return {
            "master_volume": self.master_volume,
            "music_volume": self.music_volume,
            "sfx_volume": self.sfx_volume,
            "fullscreen": self.fullscreen,
            "mouse_sensitivity": self.mouse_sensitivity,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, object]) -> "UserSettings":
        return cls(
            master_volume=int(payload.get("master_volume", 100)),
            music_volume=int(payload.get("music_volume", 80)),
            sfx_volume=int(payload.get("sfx_volume", 90)),
            fullscreen=bool(payload.get("fullscreen", False)),
            mouse_sensitivity=float(payload.get("mouse_sensitivity", 1.0)),
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
        }

    @classmethod
    def from_dict(cls, payload: dict[str, object]) -> "PlayerProfile":
        raw_settings = payload.get("settings")
        raw_upgrades = payload.get("upgrades")
        settings_payload = raw_settings if isinstance(raw_settings, dict) else {}
        upgrades_payload = raw_upgrades if isinstance(raw_upgrades, dict) else {}
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
        )

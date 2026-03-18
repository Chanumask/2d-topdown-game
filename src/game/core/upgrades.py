from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from game.settings import SETTINGS, GameSettings

if TYPE_CHECKING:
    from game.core.profile import PlayerProfile


@dataclass(frozen=True, slots=True)
class UpgradeDefinition:
    upgrade_id: str
    display_name: str
    description: str
    icon_path: str
    base_cost: int
    cost_scaling: float
    max_level: int
    effect_type: str
    effect_value_per_level: float


@dataclass(frozen=True, slots=True)
class PurchaseResult:
    upgrade_id: str
    success: bool
    reason: str
    cost: int | None
    previous_level: int
    new_level: int
    max_level: int
    meta_currency_remaining: int


@dataclass(frozen=True, slots=True)
class RunModifiers:
    player_max_health_bonus: int = 0
    player_speed_bonus: float = 0.0
    throw_cooldown_reduction: float = 0.0
    projectile_damage_bonus: int = 0
    coin_pickup_radius_bonus: float = 0.0


UPGRADE_CATALOG: dict[str, UpgradeDefinition] = {
    "health_boost": UpgradeDefinition(
        upgrade_id="health_boost",
        display_name="Health Boost",
        description="Increase maximum player health.",
        icon_path="assets/upgrades/health_boost.png",
        base_cost=80,
        cost_scaling=1.45,
        max_level=10,
        effect_type="player_max_health",
        effect_value_per_level=20.0,
    ),
    "quick_boots": UpgradeDefinition(
        upgrade_id="quick_boots",
        display_name="Quick Boots",
        description="Increase player movement speed.",
        icon_path="assets/upgrades/quick_boots.png",
        base_cost=90,
        cost_scaling=1.50,
        max_level=10,
        effect_type="player_speed",
        effect_value_per_level=40.0,
    ),
    "fast_hands": UpgradeDefinition(
        upgrade_id="fast_hands",
        display_name="Fast Hands",
        description="Reduce throw cooldown for faster rock throws.",
        icon_path="assets/upgrades/fast_hands.png",
        base_cost=110,
        cost_scaling=1.55,
        max_level=10,
        effect_type="throw_cooldown_reduction",
        effect_value_per_level=0.08,
    ),
    "heavy_rocks": UpgradeDefinition(
        upgrade_id="heavy_rocks",
        display_name="Heavy Rocks",
        description="Increase basic rock throw damage.",
        icon_path="assets/effects/Rock.png",
        base_cost=120,
        cost_scaling=1.60,
        max_level=10,
        effect_type="projectile_damage",
        effect_value_per_level=2.0,
    ),
    "magnet": UpgradeDefinition(
        upgrade_id="magnet",
        display_name="Magnet",
        description="Increase coin and Blessing pickup range.",
        icon_path="assets/upgrades/magnet.png",
        base_cost=70,
        cost_scaling=1.40,
        max_level=10,
        effect_type="coin_pickup_radius",
        effect_value_per_level=10.0,
    ),
}

UPGRADE_RUNTIME_LABELS: dict[str, str] = {
    "health_boost": "Max Health",
    "quick_boots": "Move Speed",
    "fast_hands": "Throw Cooldown",
    "heavy_rocks": "Rock Damage",
    "magnet": "Pickup Range (Coins + Blessings)",
}


def list_upgrades() -> list[UpgradeDefinition]:
    return list(UPGRADE_CATALOG.values())


def get_upgrade(upgrade_id: str) -> UpgradeDefinition | None:
    return UPGRADE_CATALOG.get(upgrade_id)


def get_upgrade_runtime_label(upgrade_id: str) -> str:
    return UPGRADE_RUNTIME_LABELS.get(upgrade_id, "Value")


def compute_upgrade_cost(upgrade: UpgradeDefinition, current_level: int) -> int:
    return max(1, int(round(upgrade.base_cost * (upgrade.cost_scaling**current_level))))


def clamp_upgrade_levels(upgrades: dict[str, int]) -> dict[str, int]:
    sanitized: dict[str, int] = {}
    for upgrade_id, level in upgrades.items():
        definition = get_upgrade(upgrade_id)
        if definition is None:
            continue

        sanitized[upgrade_id] = max(0, min(int(level), definition.max_level))
    return sanitized


def purchase_upgrade(profile: PlayerProfile, upgrade_id: str) -> PurchaseResult:
    definition = get_upgrade(upgrade_id)
    if definition is None:
        return PurchaseResult(
            upgrade_id=upgrade_id,
            success=False,
            reason="unknown_upgrade",
            cost=None,
            previous_level=0,
            new_level=0,
            max_level=0,
            meta_currency_remaining=profile.meta_currency,
        )

    current_level = int(profile.upgrades.get(upgrade_id, 0))
    current_level = max(0, min(current_level, definition.max_level))

    if current_level >= definition.max_level:
        return PurchaseResult(
            upgrade_id=upgrade_id,
            success=False,
            reason="max_level_reached",
            cost=None,
            previous_level=current_level,
            new_level=current_level,
            max_level=definition.max_level,
            meta_currency_remaining=profile.meta_currency,
        )

    cost = compute_upgrade_cost(definition, current_level)
    if profile.meta_currency < cost:
        return PurchaseResult(
            upgrade_id=upgrade_id,
            success=False,
            reason="insufficient_funds",
            cost=cost,
            previous_level=current_level,
            new_level=current_level,
            max_level=definition.max_level,
            meta_currency_remaining=profile.meta_currency,
        )

    profile.meta_currency -= cost
    upgraded_level = current_level + 1
    profile.upgrades[upgrade_id] = upgraded_level

    return PurchaseResult(
        upgrade_id=upgrade_id,
        success=True,
        reason="purchased",
        cost=cost,
        previous_level=current_level,
        new_level=upgraded_level,
        max_level=definition.max_level,
        meta_currency_remaining=profile.meta_currency,
    )


def build_run_modifiers(upgrades: dict[str, int]) -> RunModifiers:
    levels = clamp_upgrade_levels(upgrades)

    def _value(upgrade_id: str) -> float:
        definition = UPGRADE_CATALOG[upgrade_id]
        return float(levels.get(upgrade_id, 0)) * definition.effect_value_per_level

    return RunModifiers(
        player_max_health_bonus=int(round(_value("health_boost"))),
        player_speed_bonus=_value("quick_boots"),
        throw_cooldown_reduction=_value("fast_hands"),
        projectile_damage_bonus=int(round(_value("heavy_rocks"))),
        coin_pickup_radius_bonus=_value("magnet"),
    )


def compute_upgrade_runtime_value(
    upgrade_id: str,
    level: int,
    settings: GameSettings = SETTINGS,
) -> float:
    definition = get_upgrade(upgrade_id)
    if definition is None:
        return 0.0

    safe_level = max(0, min(int(level), definition.max_level))
    scaled = float(safe_level) * definition.effect_value_per_level

    if upgrade_id == "health_boost":
        return float(settings.player_max_health + scaled)
    if upgrade_id == "quick_boots":
        return float(settings.player_speed + scaled)
    if upgrade_id == "fast_hands":
        return max(0.05, float(settings.throw_cooldown_seconds - scaled))
    if upgrade_id == "heavy_rocks":
        return float(settings.projectile_damage + scaled)
    if upgrade_id == "magnet":
        pickup_radius = max(settings.player_radius, settings.player_radius + scaled)
        # Effective pickup range is center distance threshold in circles_overlap.
        return float(pickup_radius + settings.coin_radius)

    return 0.0

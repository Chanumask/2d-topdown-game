from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.core.profile import PlayerProfile


@dataclass(frozen=True, slots=True)
class UpgradeDefinition:
    upgrade_id: str
    display_name: str
    description: str
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
    projectile_speed_bonus: float = 0.0
    coin_pickup_radius_bonus: float = 0.0


UPGRADE_CATALOG: dict[str, UpgradeDefinition] = {
    "health_boost": UpgradeDefinition(
        upgrade_id="health_boost",
        display_name="Health Boost",
        description="Increase maximum player health.",
        base_cost=80,
        cost_scaling=1.45,
        max_level=5,
        effect_type="player_max_health",
        effect_value_per_level=12.0,
    ),
    "quick_boots": UpgradeDefinition(
        upgrade_id="quick_boots",
        display_name="Quick Boots",
        description="Increase player movement speed.",
        base_cost=90,
        cost_scaling=1.50,
        max_level=5,
        effect_type="player_speed",
        effect_value_per_level=15.0,
    ),
    "fast_hands": UpgradeDefinition(
        upgrade_id="fast_hands",
        display_name="Fast Hands",
        description="Reduce throw cooldown for faster rock throws.",
        base_cost=110,
        cost_scaling=1.55,
        max_level=6,
        effect_type="throw_cooldown_reduction",
        effect_value_per_level=0.015,
    ),
    "high_velocity_ammo": UpgradeDefinition(
        upgrade_id="high_velocity_ammo",
        display_name="High Velocity Ammo",
        description="Increase rock projectile speed.",
        base_cost=95,
        cost_scaling=1.50,
        max_level=5,
        effect_type="projectile_speed",
        effect_value_per_level=35.0,
    ),
    "magnet": UpgradeDefinition(
        upgrade_id="magnet",
        display_name="Magnet",
        description="Increase coin pickup radius.",
        base_cost=70,
        cost_scaling=1.40,
        max_level=6,
        effect_type="coin_pickup_radius",
        effect_value_per_level=6.0,
    ),
}


def list_upgrades() -> list[UpgradeDefinition]:
    return list(UPGRADE_CATALOG.values())


def get_upgrade(upgrade_id: str) -> UpgradeDefinition | None:
    return UPGRADE_CATALOG.get(upgrade_id)


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
        projectile_speed_bonus=_value("high_velocity_ammo"),
        coin_pickup_radius_bonus=_value("magnet"),
    )

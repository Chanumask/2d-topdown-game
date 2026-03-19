from __future__ import annotations

import random
from dataclasses import dataclass, field
from enum import StrEnum


class BlessingCategory(StrEnum):
    INSTANT = "instant"
    RUN_BOON = "run_boon"


def blessing_category_label(category: BlessingCategory) -> str:
    if category is BlessingCategory.RUN_BOON:
        return "Run Boon"
    return "Instant"


@dataclass(frozen=True, slots=True)
class BlessingDefinition:
    blessing_id: str
    display_name: str
    description: str
    icon_path: str
    category: BlessingCategory = BlessingCategory.INSTANT
    animated_effect_id: str | None = None
    has_behavior_vfx: bool = False
    run_boon_modifier: RunBoonModifier = field(default_factory=lambda: RunBoonModifier())


@dataclass(frozen=True, slots=True)
class RunBoonModifier:
    coin_heal_on_pickup: int = 0
    golden_momentum_stacks: int = 0
    fury_stacks: int = 0
    chilling_field_stacks: int = 0
    chain_spark_stacks: int = 0
    impact_pulse_stacks: int = 0

    def is_neutral(self) -> bool:
        return (
            self.coin_heal_on_pickup == 0
            and self.golden_momentum_stacks == 0
            and self.fury_stacks == 0
            and self.chilling_field_stacks == 0
            and self.chain_spark_stacks == 0
            and self.impact_pulse_stacks == 0
        )


@dataclass(frozen=True, slots=True)
class CoinVacuumConfig:
    pull_speed: float = 1200.0


@dataclass(frozen=True, slots=True)
class DamageAuraConfig:
    duration_seconds: float = 20.0
    radius: float = 96.0
    tick_interval_seconds: float = 0.5
    damage_per_tick: int = 50


BLESSING_COIN_VACUUM = "coin_vacuum"
BLESSING_SACRED_RENEWAL = "sacred_renewal"
BLESSING_DIVINE_PURGE = "divine_purge"
BLESSING_DAMAGE_AURA = "damage_aura"
BLESSING_HEALING_COIN = "healing_coin"
BLESSING_GOLDEN_MOMENTUM = "golden_momentum"
BLESSING_FURY_STACKS = "fury_stacks"
BLESSING_CHILLING_FIELD = "chilling_field"
BLESSING_CHAIN_SPARK = "chain_spark"
BLESSING_IMPACT_PULSE = "impact_pulse"
BLESSING_VFX_SACRED_RENEWAL = "blessing_sacred_renewal_green"
BLESSING_VFX_DIVINE_PURGE = "blessing_divine_purge_red"
BLESSING_VFX_DAMAGE_AURA = "blessing_damage_aura_blue"

GOLDEN_MOMENTUM_SPEED_PER_STACK = 0.05
GOLDEN_MOMENTUM_DURATION_SECONDS = 1.0
FURY_STACKS_ATTACK_SPEED_PER_STACK = 0.08
FURY_STACKS_DURATION_SECONDS = 3.0
CHILLING_FIELD_RADIUS = 80.0
CHILLING_FIELD_SLOW_PER_STACK = 0.06
CHILLING_FIELD_MIN_SPEED_MULTIPLIER = 0.5
CHAIN_SPARK_PROC_CHANCE_PER_STACK = 0.06
CHAIN_SPARK_MAX_PROC_CHANCE = 0.50
CHAIN_SPARK_RANGE = 100.0
CHAIN_SPARK_MAX_SECONDARY_TARGETS = 2
CHAIN_SPARK_DAMAGE_MULTIPLIER = 0.50
IMPACT_PULSE_BASE_RADIUS = 40.0
IMPACT_PULSE_RADIUS_PER_STACK = 10.0
IMPACT_PULSE_DAMAGE_MULTIPLIER = 0.50
COIN_VACUUM_CONFIG = CoinVacuumConfig()
DAMAGE_AURA_CONFIG = DamageAuraConfig()


BLESSING_CATALOG: dict[str, BlessingDefinition] = {
    BLESSING_COIN_VACUUM: BlessingDefinition(
        blessing_id=BLESSING_COIN_VACUUM,
        display_name="Coin Vacuum",
        description="Collect all coins currently on the map instantly.",
        icon_path="assets/blessings/coin_vacuum.png",
        category=BlessingCategory.INSTANT,
        has_behavior_vfx=True,
    ),
    BLESSING_SACRED_RENEWAL: BlessingDefinition(
        blessing_id=BLESSING_SACRED_RENEWAL,
        display_name="Sacred Renewal",
        description="Restore all players to maximum health.",
        icon_path="assets/blessings/sacred_renewal.png",
        category=BlessingCategory.INSTANT,
        animated_effect_id=BLESSING_VFX_SACRED_RENEWAL,
    ),
    BLESSING_DIVINE_PURGE: BlessingDefinition(
        blessing_id=BLESSING_DIVINE_PURGE,
        display_name="Divine Purge",
        description=(
            "Defeat normal enemies, deal half current health to elites, and leave bosses "
            "unaffected."
        ),
        icon_path="assets/blessings/divine_purge.png",
        category=BlessingCategory.INSTANT,
        animated_effect_id=BLESSING_VFX_DIVINE_PURGE,
    ),
    BLESSING_DAMAGE_AURA: BlessingDefinition(
        blessing_id=BLESSING_DAMAGE_AURA,
        display_name="Damage Aura",
        description="Emit a damaging aura around the player for 30 seconds.",
        icon_path="assets/blessings/damage_aura.png",
        category=BlessingCategory.INSTANT,
        animated_effect_id=BLESSING_VFX_DAMAGE_AURA,
    ),
    BLESSING_HEALING_COIN: BlessingDefinition(
        blessing_id=BLESSING_HEALING_COIN,
        display_name="Healing Coin",
        description="Heal 1 HP whenever you collect a coin this run. Stacks.",
        icon_path="assets/blessings/healing_coin.png",
        category=BlessingCategory.RUN_BOON,
        run_boon_modifier=RunBoonModifier(coin_heal_on_pickup=1),
    ),
    BLESSING_GOLDEN_MOMENTUM: BlessingDefinition(
        blessing_id=BLESSING_GOLDEN_MOMENTUM,
        display_name="Golden Momentum",
        description="Gain +5% move speed per stack for 1 second after picking up a coin.",
        icon_path="assets/blessings/golden_momentum.png",
        category=BlessingCategory.RUN_BOON,
        run_boon_modifier=RunBoonModifier(golden_momentum_stacks=1),
    ),
    BLESSING_FURY_STACKS: BlessingDefinition(
        blessing_id=BLESSING_FURY_STACKS,
        display_name="Fury Stacks",
        description="Gain +8% attack speed per stack for 3 seconds after killing an enemy.",
        icon_path="assets/blessings/fury_stacks.png",
        category=BlessingCategory.RUN_BOON,
        run_boon_modifier=RunBoonModifier(fury_stacks=1),
    ),
    BLESSING_CHILLING_FIELD: BlessingDefinition(
        blessing_id=BLESSING_CHILLING_FIELD,
        display_name="Chilling Field",
        description="Nearby enemies are slowed by 6% per stack, up to a maximum of 50%.",
        icon_path="assets/blessings/chillng_field.png",
        category=BlessingCategory.RUN_BOON,
        run_boon_modifier=RunBoonModifier(chilling_field_stacks=1),
    ),
    BLESSING_CHAIN_SPARK: BlessingDefinition(
        blessing_id=BLESSING_CHAIN_SPARK,
        display_name="Chain Spark",
        description=(
            "Hits have a 6% chance per stack to chain 50% damage to nearby enemies, "
            "up to 50% chance."
        ),
        icon_path="assets/blessings/chain_spark.png",
        category=BlessingCategory.RUN_BOON,
        run_boon_modifier=RunBoonModifier(chain_spark_stacks=1),
    ),
    BLESSING_IMPACT_PULSE: BlessingDefinition(
        blessing_id=BLESSING_IMPACT_PULSE,
        display_name="Impact Pulse",
        description=(
            "Hits create a splash pulse that deals 50% damage to nearby enemies. "
            "Pulse radius increases by 10 per stack."
        ),
        icon_path="assets/blessings/impact_pulse.png",
        category=BlessingCategory.RUN_BOON,
        run_boon_modifier=RunBoonModifier(impact_pulse_stacks=1),
    ),
}


def list_blessings() -> list[BlessingDefinition]:
    category_order = {
        BlessingCategory.INSTANT: 0,
        BlessingCategory.RUN_BOON: 1,
    }
    return sorted(
        BLESSING_CATALOG.values(),
        key=lambda blessing: (
            category_order.get(blessing.category, 99),
            blessing.display_name.lower(),
            blessing.blessing_id,
        ),
    )


def get_blessing(blessing_id: str) -> BlessingDefinition | None:
    return BLESSING_CATALOG.get(blessing_id)


def golden_momentum_speed_multiplier(stack_count: int) -> float:
    safe_stacks = max(0, int(stack_count))
    return 1.0 + (GOLDEN_MOMENTUM_SPEED_PER_STACK * safe_stacks)


def fury_throw_cooldown_multiplier(stack_count: int) -> float:
    safe_stacks = max(0, int(stack_count))
    return 1.0 / (1.0 + (FURY_STACKS_ATTACK_SPEED_PER_STACK * safe_stacks))


def chilling_field_speed_multiplier(stack_count: int) -> float:
    safe_stacks = max(0, int(stack_count))
    return max(
        CHILLING_FIELD_MIN_SPEED_MULTIPLIER,
        1.0 - (CHILLING_FIELD_SLOW_PER_STACK * safe_stacks),
    )


def chain_spark_proc_chance(stack_count: int) -> float:
    safe_stacks = max(0, int(stack_count))
    return min(CHAIN_SPARK_MAX_PROC_CHANCE, CHAIN_SPARK_PROC_CHANCE_PER_STACK * safe_stacks)


def impact_pulse_radius(stack_count: int) -> float:
    safe_stacks = max(0, int(stack_count))
    return IMPACT_PULSE_BASE_RADIUS + (IMPACT_PULSE_RADIUS_PER_STACK * safe_stacks)


def random_blessing_id(rng: random.Random) -> str | None:
    if not BLESSING_CATALOG:
        return None
    return rng.choice(list(BLESSING_CATALOG))

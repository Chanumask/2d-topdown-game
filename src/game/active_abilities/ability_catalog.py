from __future__ import annotations

from dataclasses import dataclass

ABILITY_GUARDIAN_SPIRIT = "guardian_spirit"
ABILITY_SHOCKWAVE = "shockwave"
ABILITY_STONE_FRENZY = "stone_frenzy"


@dataclass(frozen=True, slots=True)
class ActiveAbilityVariant:
    variant_id: str
    display_name: str
    description: str
    stat_multipliers: dict[str, float]
    cooldown_multiplier: float = 1.0


@dataclass(frozen=True, slots=True)
class ActiveAbilityDefinition:
    ability_id: str
    display_name: str
    description: str
    hud_label: str
    base_cooldown_seconds: float
    base_stats: dict[str, float]
    difficulty_scaling: dict[str, float]
    variants: tuple[ActiveAbilityVariant, ...]
    activation_vfx_effect_id: str | None = None


ABILITY_CATALOG: dict[str, ActiveAbilityDefinition] = {
    ABILITY_GUARDIAN_SPIRIT: ActiveAbilityDefinition(
        ability_id=ABILITY_GUARDIAN_SPIRIT,
        display_name="Guardian Spirit",
        description="Gain a brief defensive ward and heal over a short duration.",
        hud_label="Guardian",
        base_cooldown_seconds=26.0,
        base_stats={
            "invulnerability_seconds": 1.7,
            "heal_duration_seconds": 4.0,
            "heal_total": 36.0,
            "damage_reduction_ratio": 1.0,
        },
        difficulty_scaling={
            "invulnerability_seconds": 0.15,
            "heal_total": 0.80,
        },
        variants=(
            ActiveAbilityVariant(
                variant_id="a",
                display_name="A",
                description="Stronger invulnerability duration.",
                stat_multipliers={"invulnerability_seconds": 1.4},
            ),
            ActiveAbilityVariant(
                variant_id="b",
                display_name="B",
                description="Stronger healing.",
                stat_multipliers={"heal_total": 1.4},
            ),
            ActiveAbilityVariant(
                variant_id="c",
                display_name="C",
                description="Lower cooldown.",
                stat_multipliers={},
                cooldown_multiplier=0.75,
            ),
        ),
        activation_vfx_effect_id=None,
    ),
    ABILITY_SHOCKWAVE: ActiveAbilityDefinition(
        ability_id=ABILITY_SHOCKWAVE,
        display_name="Shockwave",
        description="Unleash a short-range frontal blast that heavily damages enemies.",
        hud_label="Shockwave",
        base_cooldown_seconds=14.0,
        base_stats={
            "range": 152.0,
            "cone_degrees": 72.0,
            "damage": 42.0,
        },
        difficulty_scaling={
            "damage": 1.0,
            "range": 0.20,
        },
        variants=(
            ActiveAbilityVariant(
                variant_id="a",
                display_name="A",
                description="Longer range.",
                stat_multipliers={"range": 1.35},
            ),
            ActiveAbilityVariant(
                variant_id="b",
                display_name="B",
                description="Higher damage.",
                stat_multipliers={"damage": 1.35},
            ),
            ActiveAbilityVariant(
                variant_id="c",
                display_name="C",
                description="Lower cooldown.",
                stat_multipliers={},
                cooldown_multiplier=0.75,
            ),
        ),
        activation_vfx_effect_id="active_ability.shockwave.activate",
    ),
    ABILITY_STONE_FRENZY: ActiveAbilityDefinition(
        ability_id=ABILITY_STONE_FRENZY,
        display_name="Stone Frenzy",
        description=(
            "Temporarily enter a rapid-fire rock throw state with auto-targeting."
        ),
        hud_label="Frenzy",
        base_cooldown_seconds=18.0,
        base_stats={
            "duration_seconds": 4.8,
            "shots_per_second": 5.0,
            "projectile_damage_multiplier": 1.10,
            "auto_target_range": 500.0,
        },
        difficulty_scaling={
            "shots_per_second": 0.45,
            "projectile_damage_multiplier": 0.55,
            "duration_seconds": 0.20,
        },
        variants=(
            ActiveAbilityVariant(
                variant_id="a",
                display_name="A",
                description="Faster attack speed.",
                stat_multipliers={"shots_per_second": 1.35},
            ),
            ActiveAbilityVariant(
                variant_id="b",
                display_name="B",
                description="Longer duration.",
                stat_multipliers={"duration_seconds": 1.40},
            ),
            ActiveAbilityVariant(
                variant_id="c",
                display_name="C",
                description="Stronger damage.",
                stat_multipliers={"projectile_damage_multiplier": 1.30},
            ),
        ),
        activation_vfx_effect_id="active_ability.stone_frenzy.activate",
    ),
}


def list_active_abilities() -> list[ActiveAbilityDefinition]:
    return [ABILITY_CATALOG[ability_id] for ability_id in sorted(ABILITY_CATALOG)]


def get_ability_definition(ability_id: str) -> ActiveAbilityDefinition | None:
    return ABILITY_CATALOG.get(ability_id)


def get_variant_definition(
    ability: ActiveAbilityDefinition,
    variant_id: str,
) -> ActiveAbilityVariant | None:
    for variant in ability.variants:
        if variant.variant_id == variant_id:
            return variant
    return None


def resolve_ability_selection(
    ability_id: str,
    variant_id: str,
) -> tuple[ActiveAbilityDefinition, ActiveAbilityVariant]:
    ability = get_ability_definition(ability_id)
    if ability is None:
        ability = next(iter(ABILITY_CATALOG.values()))

    variant = get_variant_definition(ability, variant_id)
    if variant is None:
        variant = ability.variants[0]

    return ability, variant


def build_scaled_stats(
    ability: ActiveAbilityDefinition,
    variant: ActiveAbilityVariant,
    difficulty_factor: float,
) -> dict[str, float]:
    stats: dict[str, float] = {}
    progression = max(0.0, float(difficulty_factor) - 1.0)
    for key, base_value in ability.base_stats.items():
        scaled_value = float(base_value)
        multiplier = float(variant.stat_multipliers.get(key, 1.0))
        scaled_value *= max(0.01, multiplier)

        scaling_factor = float(ability.difficulty_scaling.get(key, 0.0))
        if scaling_factor != 0.0:
            scaled_value *= max(0.01, 1.0 + (progression * scaling_factor))

        stats[key] = scaled_value

    return stats


def cooldown_seconds(ability: ActiveAbilityDefinition, variant: ActiveAbilityVariant) -> float:
    return max(0.05, float(ability.base_cooldown_seconds) * float(variant.cooldown_multiplier))

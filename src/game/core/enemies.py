from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class EnemyTier(StrEnum):
    NORMAL = "normal"
    ELITE = "elite"
    BOSS = "boss"


class EnemyHookTrigger(StrEnum):
    ON_SPAWN = "on_spawn"
    ON_DEATH = "on_death"
    INTERVAL = "interval"


class EnemyInfluenceTarget(StrEnum):
    OTHER_ENEMIES = "other_enemies"
    ALL_ENEMIES = "all_enemies"
    SPAWNER = "spawner"


@dataclass(frozen=True, slots=True)
class EnemyStats:
    max_health: int
    speed: float
    touch_damage: int
    coin_drop_value: int
    radius: float


@dataclass(frozen=True, slots=True)
class EnemyAbilityDefinition:
    ability_id: str
    display_name: str
    description: str = ""


@dataclass(frozen=True, slots=True)
class EnemyStatModifier:
    max_health_flat: int = 0
    max_health_multiplier: float = 1.0
    speed_flat: float = 0.0
    speed_multiplier: float = 1.0
    touch_damage_flat: int = 0
    touch_damage_multiplier: float = 1.0
    coin_drop_value_flat: int = 0
    coin_drop_value_multiplier: float = 1.0
    radius_flat: float = 0.0
    radius_multiplier: float = 1.0

    def is_neutral(self) -> bool:
        return (
            self.max_health_flat == 0
            and self.max_health_multiplier == 1.0
            and self.speed_flat == 0.0
            and self.speed_multiplier == 1.0
            and self.touch_damage_flat == 0
            and self.touch_damage_multiplier == 1.0
            and self.coin_drop_value_flat == 0
            and self.coin_drop_value_multiplier == 1.0
            and self.radius_flat == 0.0
            and self.radius_multiplier == 1.0
        )


@dataclass(frozen=True, slots=True)
class EnemyInfluenceDefinition:
    influence_id: str
    target: EnemyInfluenceTarget = EnemyInfluenceTarget.OTHER_ENEMIES
    target_tiers: tuple[EnemyTier, ...] = ()
    required_tags: tuple[str, ...] = ()
    excluded_tags: tuple[str, ...] = ()
    stat_modifier: EnemyStatModifier = field(default_factory=EnemyStatModifier)
    spawn_interval_multiplier: float = 1.0
    spawn_batch_bonus: int = 0
    duration_seconds: float | None = None


@dataclass(frozen=True, slots=True)
class EnemyHookDefinition:
    hook_id: str
    trigger: EnemyHookTrigger
    emitted_influences: tuple[EnemyInfluenceDefinition, ...] = ()
    interval_seconds: float | None = None


@dataclass(frozen=True, slots=True)
class EnemyProfile:
    profile_id: str
    display_name: str
    tier: EnemyTier
    stats: EnemyStats
    abilities: tuple[EnemyAbilityDefinition, ...] = ()
    passive_influences: tuple[EnemyInfluenceDefinition, ...] = ()
    hooks: tuple[EnemyHookDefinition, ...] = ()
    tags: tuple[str, ...] = ()
    spawn_weight: float = 0.0


@dataclass(frozen=True, slots=True)
class EnemySpawnRequest:
    profile_id: str
    tier: EnemyTier
    stats: EnemyStats
    tags: tuple[str, ...]


def combine_enemy_stat_modifiers(
    modifiers: list[EnemyStatModifier],
) -> EnemyStatModifier:
    if not modifiers:
        return EnemyStatModifier()

    max_health_flat = 0
    max_health_multiplier = 1.0
    speed_flat = 0.0
    speed_multiplier = 1.0
    touch_damage_flat = 0
    touch_damage_multiplier = 1.0
    coin_drop_value_flat = 0
    coin_drop_value_multiplier = 1.0
    radius_flat = 0.0
    radius_multiplier = 1.0

    for modifier in modifiers:
        max_health_flat += modifier.max_health_flat
        max_health_multiplier *= modifier.max_health_multiplier
        speed_flat += modifier.speed_flat
        speed_multiplier *= modifier.speed_multiplier
        touch_damage_flat += modifier.touch_damage_flat
        touch_damage_multiplier *= modifier.touch_damage_multiplier
        coin_drop_value_flat += modifier.coin_drop_value_flat
        coin_drop_value_multiplier *= modifier.coin_drop_value_multiplier
        radius_flat += modifier.radius_flat
        radius_multiplier *= modifier.radius_multiplier

    return EnemyStatModifier(
        max_health_flat=max_health_flat,
        max_health_multiplier=max_health_multiplier,
        speed_flat=speed_flat,
        speed_multiplier=speed_multiplier,
        touch_damage_flat=touch_damage_flat,
        touch_damage_multiplier=touch_damage_multiplier,
        coin_drop_value_flat=coin_drop_value_flat,
        coin_drop_value_multiplier=coin_drop_value_multiplier,
        radius_flat=radius_flat,
        radius_multiplier=radius_multiplier,
    )


def apply_enemy_stat_modifier(base: EnemyStats, modifier: EnemyStatModifier) -> EnemyStats:
    max_health = max(
        1,
        int(round((base.max_health + modifier.max_health_flat) * modifier.max_health_multiplier)),
    )
    speed = max(1.0, (base.speed + modifier.speed_flat) * modifier.speed_multiplier)
    touch_damage = max(
        1,
        int(
            round(
                (base.touch_damage + modifier.touch_damage_flat) * modifier.touch_damage_multiplier
            )
        ),
    )
    coin_drop_value = max(
        0,
        int(
            round(
                (base.coin_drop_value + modifier.coin_drop_value_flat)
                * modifier.coin_drop_value_multiplier
            )
        ),
    )
    radius = max(1.0, (base.radius + modifier.radius_flat) * modifier.radius_multiplier)
    return EnemyStats(
        max_health=max_health,
        speed=speed,
        touch_damage=touch_damage,
        coin_drop_value=coin_drop_value,
        radius=radius,
    )

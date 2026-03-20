from __future__ import annotations

import random
from dataclasses import dataclass, field
from enum import StrEnum

ENHANCEMENT_FIRST_TRIGGER_DIFFICULTY = 3.0
ENHANCEMENT_TRIGGER_STEP = 2.0
ENHANCEMENT_MAX_DAMAGE_REDUCTION = 0.75

_GUARDIAN_SPIRIT_ABILITY_ID = "guardian_spirit"
_SHOCKWAVE_ABILITY_ID = "shockwave"
_STONE_FRENZY_ABILITY_ID = "stone_frenzy"


class EnhancementPool(StrEnum):
    CORE_ATTACK = "core_attack"
    ABILITY = "ability"
    UTILITY = "utility"


def enhancement_pool_label(pool: EnhancementPool) -> str:
    if pool is EnhancementPool.CORE_ATTACK:
        return "Core Attack"
    if pool is EnhancementPool.ABILITY:
        return "Ability"
    return "Utility"


class EnhancementIconRole(StrEnum):
    ROCK = "rock"
    ABILITY = "ability"
    UTILITY = "utility"


@dataclass(frozen=True, slots=True)
class EnhancementModifier:
    stone_damage_bonus: float = 0.0
    throw_attack_speed_bonus: float = 0.0
    projectile_speed_bonus: float = 0.0
    ability_cooldown_reduction: float = 0.0
    ability_duration_bonus: float = 0.0
    ability_power_bonus: float = 0.0
    max_health_bonus: int = 0
    move_speed_bonus: float = 0.0
    pickup_radius_bonus: float = 0.0
    damage_reduction_bonus: float = 0.0

    def __add__(self, other: EnhancementModifier) -> EnhancementModifier:
        return EnhancementModifier(
            stone_damage_bonus=self.stone_damage_bonus + other.stone_damage_bonus,
            throw_attack_speed_bonus=(
                self.throw_attack_speed_bonus + other.throw_attack_speed_bonus
            ),
            projectile_speed_bonus=self.projectile_speed_bonus + other.projectile_speed_bonus,
            ability_cooldown_reduction=(
                self.ability_cooldown_reduction + other.ability_cooldown_reduction
            ),
            ability_duration_bonus=self.ability_duration_bonus + other.ability_duration_bonus,
            ability_power_bonus=self.ability_power_bonus + other.ability_power_bonus,
            max_health_bonus=self.max_health_bonus + other.max_health_bonus,
            move_speed_bonus=self.move_speed_bonus + other.move_speed_bonus,
            pickup_radius_bonus=self.pickup_radius_bonus + other.pickup_radius_bonus,
            damage_reduction_bonus=self.damage_reduction_bonus + other.damage_reduction_bonus,
        )


@dataclass(frozen=True, slots=True)
class EnhancementDefinition:
    enhancement_id: str
    pool: EnhancementPool
    display_name: str
    description: str
    icon_role: EnhancementIconRole
    modifier: EnhancementModifier


@dataclass(frozen=True, slots=True)
class EnhancementOffer:
    trigger_difficulty_factor: float
    option_ids: tuple[str, str, str]

    def option_id_at(self, index: int) -> str | None:
        if 0 <= index < len(self.option_ids):
            return self.option_ids[index]
        return None


@dataclass(slots=True)
class PlayerEnhancementState:
    counts_by_id: dict[str, int] = field(default_factory=dict)

    def add(self, enhancement_id: str) -> int:
        new_count = self.count(enhancement_id) + 1
        self.counts_by_id[enhancement_id] = new_count
        return new_count

    def count(self, enhancement_id: str) -> int:
        return max(0, int(self.counts_by_id.get(enhancement_id, 0)))

    def aggregated_modifier(self) -> EnhancementModifier:
        total = EnhancementModifier()
        for enhancement_id, count in self.counts_by_id.items():
            definition = get_enhancement(enhancement_id)
            if definition is None or count <= 0:
                continue
            for _ in range(int(count)):
                total = total + definition.modifier
        return total


@dataclass(slots=True)
class EnhancementRuntime:
    by_player_id: dict[str, PlayerEnhancementState] = field(default_factory=dict)
    pending_offers_by_player_id: dict[str, EnhancementOffer] = field(default_factory=dict)
    next_trigger_difficulty_factor: float = ENHANCEMENT_FIRST_TRIGGER_DIFFICULTY

    def ensure_player(self, player_id: str) -> None:
        self.by_player_id.setdefault(player_id, PlayerEnhancementState())

    def modifier_for_player(self, player_id: str) -> EnhancementModifier:
        state = self.by_player_id.get(player_id)
        if state is None:
            return EnhancementModifier()
        return state.aggregated_modifier()

    def pending_offer_for_player(self, player_id: str) -> EnhancementOffer | None:
        return self.pending_offers_by_player_id.get(player_id)

    def has_pending_offer(self, player_id: str) -> bool:
        return player_id in self.pending_offers_by_player_id

    def update_trigger(
        self,
        *,
        difficulty_factor: float,
        player_ids: list[str],
        rng: random.Random,
    ) -> bool:
        if not player_ids or self.pending_offers_by_player_id:
            return False
        if float(difficulty_factor) < float(self.next_trigger_difficulty_factor):
            return False

        trigger_value = float(self.next_trigger_difficulty_factor)
        for player_id in sorted(player_ids):
            self.ensure_player(player_id)
            self.pending_offers_by_player_id[player_id] = self._generate_offer(
                rng=rng,
                trigger_difficulty_factor=trigger_value,
            )
        self.next_trigger_difficulty_factor += ENHANCEMENT_TRIGGER_STEP
        return True

    def apply_choice_index(
        self,
        player_id: str,
        option_index: int,
    ) -> EnhancementDefinition | None:
        offer = self.pending_offers_by_player_id.get(player_id)
        if offer is None:
            return None

        option_id = offer.option_id_at(option_index)
        definition = get_enhancement(option_id or "")
        if definition is None:
            return None

        state = self.by_player_id.setdefault(player_id, PlayerEnhancementState())
        state.add(definition.enhancement_id)
        self.pending_offers_by_player_id.pop(player_id, None)
        return definition

    def _generate_offer(
        self,
        *,
        rng: random.Random,
        trigger_difficulty_factor: float,
    ) -> EnhancementOffer:
        option_ids = tuple(
            rng.choice(list_enhancements_for_pool(pool)).enhancement_id for pool in POOL_ORDER
        )
        return EnhancementOffer(
            trigger_difficulty_factor=trigger_difficulty_factor,
            option_ids=option_ids,
        )


ENHANCEMENT_CATALOG: dict[str, EnhancementDefinition] = {
    "core_stone_damage": EnhancementDefinition(
        enhancement_id="core_stone_damage",
        pool=EnhancementPool.CORE_ATTACK,
        display_name="Heavy Throw",
        description="Increase stone damage by 15%.",
        icon_role=EnhancementIconRole.ROCK,
        modifier=EnhancementModifier(stone_damage_bonus=0.15),
    ),
    "core_attack_speed": EnhancementDefinition(
        enhancement_id="core_attack_speed",
        pool=EnhancementPool.CORE_ATTACK,
        display_name="Quick Release",
        description="Increase attack speed by 12%.",
        icon_role=EnhancementIconRole.ROCK,
        modifier=EnhancementModifier(throw_attack_speed_bonus=0.12),
    ),
    "core_projectile_speed": EnhancementDefinition(
        enhancement_id="core_projectile_speed",
        pool=EnhancementPool.CORE_ATTACK,
        display_name="Swift Stone",
        description="Increase projectile speed by 15%.",
        icon_role=EnhancementIconRole.ROCK,
        modifier=EnhancementModifier(projectile_speed_bonus=0.15),
    ),
    "ability_cooldown": EnhancementDefinition(
        enhancement_id="ability_cooldown",
        pool=EnhancementPool.ABILITY,
        display_name="Quickened Ability",
        description="Reduce ability cooldown by 12%.",
        icon_role=EnhancementIconRole.ABILITY,
        modifier=EnhancementModifier(ability_cooldown_reduction=0.12),
    ),
    "ability_duration": EnhancementDefinition(
        enhancement_id="ability_duration",
        pool=EnhancementPool.ABILITY,
        display_name="Lasting Ability",
        description="Increase ability duration by 20%.",
        icon_role=EnhancementIconRole.ABILITY,
        modifier=EnhancementModifier(ability_duration_bonus=0.20),
    ),
    "ability_power": EnhancementDefinition(
        enhancement_id="ability_power",
        pool=EnhancementPool.ABILITY,
        display_name="Empowered Ability",
        description="Increase ability power by 20%.",
        icon_role=EnhancementIconRole.ABILITY,
        modifier=EnhancementModifier(ability_power_bonus=0.20),
    ),
    "utility_max_health": EnhancementDefinition(
        enhancement_id="utility_max_health",
        pool=EnhancementPool.UTILITY,
        display_name="Vital Reserve",
        description="Increase max health by 25.",
        icon_role=EnhancementIconRole.UTILITY,
        modifier=EnhancementModifier(max_health_bonus=25),
    ),
    "utility_move_speed": EnhancementDefinition(
        enhancement_id="utility_move_speed",
        pool=EnhancementPool.UTILITY,
        display_name="Fleet Footing",
        description="Increase move speed by 10%.",
        icon_role=EnhancementIconRole.UTILITY,
        modifier=EnhancementModifier(move_speed_bonus=0.10),
    ),
    "utility_pickup_radius": EnhancementDefinition(
        enhancement_id="utility_pickup_radius",
        pool=EnhancementPool.UTILITY,
        display_name="Long Reach",
        description="Increase pickup radius by 12.",
        icon_role=EnhancementIconRole.UTILITY,
        modifier=EnhancementModifier(pickup_radius_bonus=12.0),
    ),
    "utility_damage_reduction": EnhancementDefinition(
        enhancement_id="utility_damage_reduction",
        pool=EnhancementPool.UTILITY,
        display_name="Iron Guard",
        description="Reduce damage taken by 8%.",
        icon_role=EnhancementIconRole.UTILITY,
        modifier=EnhancementModifier(damage_reduction_bonus=0.08),
    ),
}

POOL_ORDER: tuple[EnhancementPool, EnhancementPool, EnhancementPool] = (
    EnhancementPool.CORE_ATTACK,
    EnhancementPool.ABILITY,
    EnhancementPool.UTILITY,
)


def list_enhancements() -> list[EnhancementDefinition]:
    return [ENHANCEMENT_CATALOG[key] for key in sorted(ENHANCEMENT_CATALOG)]


def get_enhancement(enhancement_id: str) -> EnhancementDefinition | None:
    return ENHANCEMENT_CATALOG.get(enhancement_id)


def list_enhancements_for_pool(pool: EnhancementPool) -> list[EnhancementDefinition]:
    return [
        definition
        for definition in list_enhancements()
        if definition.pool is pool
    ]


def core_attack_cooldown_multiplier(modifier: EnhancementModifier) -> float:
    return 1.0 / (1.0 + max(0.0, float(modifier.throw_attack_speed_bonus)))


def stone_damage_multiplier(modifier: EnhancementModifier) -> float:
    return 1.0 + max(0.0, float(modifier.stone_damage_bonus))


def projectile_speed_multiplier(modifier: EnhancementModifier) -> float:
    return 1.0 + max(0.0, float(modifier.projectile_speed_bonus))


def move_speed_multiplier(modifier: EnhancementModifier) -> float:
    return 1.0 + max(0.0, float(modifier.move_speed_bonus))


def ability_cooldown_multiplier(modifier: EnhancementModifier) -> float:
    reduction = max(0.0, min(0.75, float(modifier.ability_cooldown_reduction)))
    return max(0.25, 1.0 - reduction)


def damage_reduction_multiplier(modifier: EnhancementModifier) -> float:
    reduction = max(0.0, min(ENHANCEMENT_MAX_DAMAGE_REDUCTION, modifier.damage_reduction_bonus))
    return max(0.0, 1.0 - reduction)


def apply_ability_enhancement_modifiers(
    ability_id: str,
    stats: dict[str, float],
    modifier: EnhancementModifier,
) -> dict[str, float]:
    adjusted = dict(stats)
    duration_multiplier = 1.0 + max(0.0, float(modifier.ability_duration_bonus))
    power_multiplier = 1.0 + max(0.0, float(modifier.ability_power_bonus))

    if ability_id == _GUARDIAN_SPIRIT_ABILITY_ID:
        adjusted["invulnerability_seconds"] = (
            adjusted.get("invulnerability_seconds", 0.0) * duration_multiplier
        )
        adjusted["heal_duration_seconds"] = (
            adjusted.get("heal_duration_seconds", 0.0) * duration_multiplier
        )
        adjusted["heal_total"] = adjusted.get("heal_total", 0.0) * power_multiplier
    elif ability_id == _SHOCKWAVE_ABILITY_ID:
        adjusted["range"] = adjusted.get("range", 0.0) * duration_multiplier
        adjusted["damage"] = adjusted.get("damage", 0.0) * power_multiplier
    elif ability_id == _STONE_FRENZY_ABILITY_ID:
        adjusted["duration_seconds"] = adjusted.get("duration_seconds", 0.0) * duration_multiplier
        adjusted["shots_per_second"] = adjusted.get("shots_per_second", 0.0) * power_multiplier

    return adjusted

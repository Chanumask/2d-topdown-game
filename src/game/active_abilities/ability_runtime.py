from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from game.active_abilities.ability_catalog import (
    ABILITY_GUARDIAN_SPIRIT,
    ABILITY_SHOCKWAVE,
    ABILITY_STONE_FRENZY,
    build_scaled_stats,
    cooldown_seconds,
    resolve_ability_selection,
)
from game.active_abilities.ability_effects import (
    apply_shockwave,
    resolve_attack_direction,
    try_fire_frenzy_projectile,
)

if TYPE_CHECKING:
    from game.core.world import World


@dataclass(slots=True)
class ActiveAbilityState:
    ability_id: str
    variant_id: str
    cooldown_total_seconds: float
    cooldown_remaining_seconds: float = 0.0
    active_remaining_seconds: float = 0.0
    heal_remaining_total: float = 0.0
    heal_fractional_pool: float = 0.0
    frenzy_shot_timer_seconds: float = 0.0

    def to_dict(self) -> dict[str, object]:
        return {
            "ability_id": self.ability_id,
            "variant_id": self.variant_id,
            "cooldown_total_seconds": float(self.cooldown_total_seconds),
            "cooldown_remaining_seconds": float(self.cooldown_remaining_seconds),
            "active_remaining_seconds": float(self.active_remaining_seconds),
        }


@dataclass(slots=True)
class ActiveAbilityRuntime:
    by_player_id: dict[str, ActiveAbilityState] = field(default_factory=dict)

    def equip_player(self, player_id: str, ability_id: str, variant_id: str) -> None:
        ability, variant = resolve_ability_selection(ability_id, variant_id)
        self.by_player_id[player_id] = ActiveAbilityState(
            ability_id=ability.ability_id,
            variant_id=variant.variant_id,
            cooldown_total_seconds=cooldown_seconds(ability, variant),
        )

    def try_activate(self, world: World, player_id: str) -> bool:
        player = world.players.get(player_id)
        if player is None or not player.alive:
            return False

        state = self.by_player_id.get(player_id)
        if state is None:
            return False
        if state.cooldown_remaining_seconds > 0.0:
            return False

        ability, variant = resolve_ability_selection(state.ability_id, state.variant_id)
        stats = build_scaled_stats(ability, variant, world.difficulty_factor)

        activated = False
        if ability.ability_id == ABILITY_GUARDIAN_SPIRIT:
            state.active_remaining_seconds = max(
                0.05,
                float(stats.get("invulnerability_seconds", 0.0)),
            )
            state.heal_remaining_total = max(0.0, float(stats.get("heal_total", 0.0)))
            state.heal_fractional_pool = 0.0
            activated = True

        elif ability.ability_id == ABILITY_SHOCKWAVE:
            direction = resolve_attack_direction(player)
            apply_shockwave(world, player, stats)
            if ability.activation_vfx_effect_id:
                angle = math.degrees(math.atan2(direction.y, direction.x))
                spawn_offset = max(
                    player.radius + 10.0,
                    float(stats.get("range", 120.0)) * 0.16,
                )
                world.emit_world_vfx(
                    ability.activation_vfx_effect_id,
                    player.position + (direction * spawn_offset),
                    angle_degrees=angle,
                    travel_distance=max(0.0, float(stats.get("range", 120.0)) - spawn_offset),
                )
            activated = True

        elif ability.ability_id == ABILITY_STONE_FRENZY:
            state.active_remaining_seconds = max(0.1, float(stats.get("duration_seconds", 0.0)))
            state.frenzy_shot_timer_seconds = 0.0
            activated = True

        if not activated:
            return False

        state.cooldown_total_seconds = cooldown_seconds(ability, variant)
        state.cooldown_remaining_seconds = state.cooldown_total_seconds
        if ability.activation_vfx_effect_id and ability.ability_id != ABILITY_SHOCKWAVE:
            world.emit_world_vfx(ability.activation_vfx_effect_id, player.position.copy())
        return True

    def update(self, world: World, dt: float) -> None:
        for player_id, state in self.by_player_id.items():
            player = world.players.get(player_id)
            if player is None:
                continue

            state.cooldown_remaining_seconds = max(0.0, state.cooldown_remaining_seconds - dt)
            if state.active_remaining_seconds <= 0.0:
                continue
            if not player.alive:
                state.active_remaining_seconds = 0.0
                state.heal_remaining_total = 0.0
                continue

            ability, variant = resolve_ability_selection(state.ability_id, state.variant_id)
            stats = build_scaled_stats(ability, variant, world.difficulty_factor)
            previous_remaining = state.active_remaining_seconds
            state.active_remaining_seconds = max(0.0, state.active_remaining_seconds - dt)
            active_dt = min(previous_remaining, dt)

            if ability.ability_id == ABILITY_GUARDIAN_SPIRIT:
                self._update_guardian(player, state, stats, active_dt)
            elif ability.ability_id == ABILITY_STONE_FRENZY:
                self._update_stone_frenzy(world, player, state, stats, active_dt)

    def modify_incoming_damage(self, world: World, player_id: str, damage: int) -> int:
        if damage <= 0:
            return 0

        state = self.by_player_id.get(player_id)
        if state is None:
            return damage

        ability, variant = resolve_ability_selection(state.ability_id, state.variant_id)
        if ability.ability_id != ABILITY_GUARDIAN_SPIRIT:
            return damage
        if state.active_remaining_seconds <= 0.0:
            return damage

        stats = build_scaled_stats(ability, variant, world.difficulty_factor)
        reduction_ratio = max(0.0, min(1.0, float(stats.get("damage_reduction_ratio", 1.0))))
        reduced = int(round(float(damage) * (1.0 - reduction_ratio)))
        return max(0, reduced)

    def snapshot_payload(self, world: World, player_id: str) -> dict[str, object] | None:
        state = self.by_player_id.get(player_id)
        if state is None:
            return None

        ability, variant = resolve_ability_selection(state.ability_id, state.variant_id)
        return {
            "ability_id": ability.ability_id,
            "ability_name": ability.display_name,
            "ability_hud_label": ability.hud_label,
            "variant_id": variant.variant_id,
            "variant_name": variant.display_name,
            "cooldown_total_seconds": float(state.cooldown_total_seconds),
            "cooldown_remaining_seconds": float(state.cooldown_remaining_seconds),
            "active_remaining_seconds": float(state.active_remaining_seconds),
            "ready": state.cooldown_remaining_seconds <= 0.0,
            "difficulty_factor": float(world.difficulty_factor),
        }

    @staticmethod
    def _update_guardian(
        player,
        state: ActiveAbilityState,
        stats: dict[str, float],
        active_dt: float,
    ) -> None:
        if active_dt <= 0.0:
            return

        heal_duration = max(0.05, float(stats.get("heal_duration_seconds", 0.0)))
        heal_rate = max(0.0, float(stats.get("heal_total", 0.0)) / heal_duration)
        if heal_rate <= 0.0 or state.heal_remaining_total <= 0.0:
            return

        heal_amount = min(state.heal_remaining_total, heal_rate * active_dt)
        state.heal_remaining_total = max(0.0, state.heal_remaining_total - heal_amount)
        state.heal_fractional_pool += heal_amount

        apply_int = int(state.heal_fractional_pool)
        if apply_int <= 0:
            return

        state.heal_fractional_pool -= apply_int
        player.health = min(player.max_health, player.health + apply_int)

    @staticmethod
    def _update_stone_frenzy(
        world: World,
        player,
        state: ActiveAbilityState,
        stats: dict[str, float],
        active_dt: float,
    ) -> None:
        if active_dt <= 0.0:
            return

        shots_per_second = max(1.0, float(stats.get("shots_per_second", 1.0)))
        shot_interval = 1.0 / shots_per_second
        state.frenzy_shot_timer_seconds -= active_dt
        max_auto_shots = 6
        shot_count = 0
        while state.frenzy_shot_timer_seconds <= 0.0 and shot_count < max_auto_shots:
            fired = try_fire_frenzy_projectile(world, player, stats)
            state.frenzy_shot_timer_seconds += shot_interval
            shot_count += 1
            if not fired:
                break


__all__ = ["ActiveAbilityRuntime", "ActiveAbilityState"]

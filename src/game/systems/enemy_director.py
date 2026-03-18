import random
from dataclasses import dataclass
from typing import TYPE_CHECKING

from game.core.enemies import (
    EnemyHookDefinition,
    EnemyHookTrigger,
    EnemyInfluenceDefinition,
    EnemyInfluenceTarget,
    EnemyProfile,
    EnemySpawnRequest,
    EnemyStatModifier,
    apply_enemy_stat_modifier,
    combine_enemy_stat_modifiers,
)
from game.core.enemy_catalog import CRIMSON_IMP_PROFILE_ID, get_enemy_profiles

if TYPE_CHECKING:
    from game.core.world import World
    from game.entities.enemy import Enemy


@dataclass(slots=True)
class ActiveEnemyInfluence:
    source_enemy_id: int | None
    source_profile_id: str | None
    definition: EnemyInfluenceDefinition
    remaining_seconds: float


class EnemyDirector:
    def __init__(
        self,
        rng: random.Random,
        profiles: dict[str, EnemyProfile] | None = None,
    ) -> None:
        self.rng = rng
        self.profiles = profiles or get_enemy_profiles()
        self._interval_hook_cooldowns: dict[tuple[int, str], float] = {}
        self._active_influences: list[ActiveEnemyInfluence] = []

    def build_spawn_request(self, world: World, profile_id: str | None = None) -> EnemySpawnRequest:
        profile = self._resolve_spawn_profile(world, profile_id)
        elapsed = world.simulation_time
        difficulty_modifier = EnemyStatModifier(
            max_health_flat=int(elapsed // 25.0) * 4,
            speed_flat=(elapsed // 18.0) * 3.0,
        )
        stats = apply_enemy_stat_modifier(profile.stats, difficulty_modifier)
        return EnemySpawnRequest(
            profile_id=profile.profile_id,
            tier=profile.tier,
            stats=stats,
            tags=profile.tags,
        )

    def update(self, world: World, dt: float) -> None:
        self._update_active_influences(dt)
        self._update_interval_hooks(world, dt)
        self._refresh_enemy_runtime_stats(world)
        self._prune_state(world)

    def on_enemy_spawn(self, world: World, enemy: Enemy) -> None:
        self._run_hooks(enemy, EnemyHookTrigger.ON_SPAWN, source_enemy_id=enemy.entity_id)
        self._refresh_enemy_runtime_stats(world)

    def on_enemy_death(self, world: World, enemy: Enemy) -> None:
        self._interval_hook_cooldowns = {
            key: remaining
            for key, remaining in self._interval_hook_cooldowns.items()
            if key[0] != enemy.entity_id
        }
        self._active_influences = [
            influence
            for influence in self._active_influences
            if influence.source_enemy_id != enemy.entity_id
        ]
        self._run_hooks(enemy, EnemyHookTrigger.ON_DEATH, source_enemy_id=None)

    def current_spawn_interval_multiplier(self, world: World) -> float:
        multiplier = 1.0
        for _, influence in self._iter_all_influences(world):
            if influence.target is not EnemyInfluenceTarget.SPAWNER:
                continue
            multiplier *= max(0.1, float(influence.spawn_interval_multiplier))
        return max(0.1, multiplier)

    def current_spawn_batch_bonus(self, world: World) -> int:
        bonus = 0
        for _, influence in self._iter_all_influences(world):
            if influence.target is not EnemyInfluenceTarget.SPAWNER:
                continue
            bonus += int(influence.spawn_batch_bonus)
        return max(0, bonus)

    def _resolve_spawn_profile(self, world: World, profile_id: str | None) -> EnemyProfile:
        if profile_id is not None and profile_id in self.profiles:
            return self.profiles[profile_id]

        weighted_profiles = [
            profile
            for profile in self.profiles.values()
            if float(profile.spawn_weight) > 0.0
            and float(world.difficulty_factor) >= float(profile.min_difficulty_factor)
        ]
        if not weighted_profiles:
            return self.profiles[CRIMSON_IMP_PROFILE_ID]

        total_weight = sum(profile.spawn_weight for profile in weighted_profiles)
        roll = self.rng.uniform(0.0, total_weight)
        running_total = 0.0
        for profile in weighted_profiles:
            running_total += profile.spawn_weight
            if roll <= running_total:
                return profile
        return weighted_profiles[-1]

    def _update_active_influences(self, dt: float) -> None:
        if not self._active_influences:
            return

        kept: list[ActiveEnemyInfluence] = []
        for influence in self._active_influences:
            influence.remaining_seconds -= dt
            if influence.remaining_seconds > 0.0:
                kept.append(influence)
        self._active_influences = kept

    def _update_interval_hooks(self, world: World, dt: float) -> None:
        for enemy in world.enemies.values():
            if not enemy.alive:
                continue

            profile = self.profiles.get(enemy.profile_id)
            if profile is None:
                continue

            for hook in profile.hooks:
                if hook.trigger is not EnemyHookTrigger.INTERVAL:
                    continue
                if hook.interval_seconds is None or hook.interval_seconds <= 0.0:
                    continue

                key = (enemy.entity_id, hook.hook_id)
                cooldown = self._interval_hook_cooldowns.get(key, hook.interval_seconds) - dt
                if cooldown > 0.0:
                    self._interval_hook_cooldowns[key] = cooldown
                    continue

                self._run_hook(enemy, hook, source_enemy_id=enemy.entity_id)
                self._interval_hook_cooldowns[key] = hook.interval_seconds

    def _refresh_enemy_runtime_stats(self, world: World) -> None:
        alive_enemies = [enemy for enemy in world.enemies.values() if enemy.alive]
        if not alive_enemies:
            return

        for enemy in alive_enemies:
            modifiers = self._modifiers_for_enemy(world, enemy)
            effective_stats = apply_enemy_stat_modifier(enemy.base_stats(), modifiers)
            enemy.apply_runtime_stats(effective_stats)

    def _modifiers_for_enemy(self, world: World, enemy: Enemy) -> EnemyStatModifier:
        matching_modifiers: list[EnemyStatModifier] = []
        for source_enemy_id, influence in self._iter_all_influences(world):
            if influence.target not in (
                EnemyInfluenceTarget.ALL_ENEMIES,
                EnemyInfluenceTarget.OTHER_ENEMIES,
            ):
                continue
            if (
                influence.target is EnemyInfluenceTarget.OTHER_ENEMIES
                and source_enemy_id == enemy.entity_id
            ):
                continue
            if not self._enemy_matches_influence(enemy, influence):
                continue
            if influence.stat_modifier.is_neutral():
                continue
            matching_modifiers.append(influence.stat_modifier)

        return combine_enemy_stat_modifiers(matching_modifiers)

    def _enemy_matches_influence(self, enemy: Enemy, influence: EnemyInfluenceDefinition) -> bool:
        if influence.target_tiers and enemy.tier not in {
            tier.value for tier in influence.target_tiers
        }:
            return False

        enemy_tags = set(enemy.tags)
        if influence.required_tags and not set(influence.required_tags).issubset(enemy_tags):
            return False
        if influence.excluded_tags and enemy_tags.intersection(influence.excluded_tags):
            return False
        return True

    def _run_hooks(
        self,
        enemy: Enemy,
        trigger: EnemyHookTrigger,
        *,
        source_enemy_id: int | None,
    ) -> None:
        profile = self.profiles.get(enemy.profile_id)
        if profile is None:
            return

        for hook in profile.hooks:
            if hook.trigger is trigger:
                self._run_hook(enemy, hook, source_enemy_id=source_enemy_id)

    def _run_hook(
        self,
        enemy: Enemy,
        hook: EnemyHookDefinition,
        *,
        source_enemy_id: int | None,
    ) -> None:
        for influence in hook.emitted_influences:
            duration = influence.duration_seconds
            if duration is None or duration <= 0.0:
                continue
            self._active_influences.append(
                ActiveEnemyInfluence(
                    source_enemy_id=source_enemy_id,
                    source_profile_id=enemy.profile_id,
                    definition=influence,
                    remaining_seconds=float(duration),
                )
            )

    def _iter_all_influences(self, world: World):
        for enemy in world.enemies.values():
            if not enemy.alive:
                continue
            profile = self.profiles.get(enemy.profile_id)
            if profile is None:
                continue
            for influence in profile.passive_influences:
                yield enemy.entity_id, influence

        for active in self._active_influences:
            yield active.source_enemy_id, active.definition

    def _prune_state(self, world: World) -> None:
        alive_enemy_ids = {enemy.entity_id for enemy in world.enemies.values() if enemy.alive}
        self._interval_hook_cooldowns = {
            key: remaining
            for key, remaining in self._interval_hook_cooldowns.items()
            if key[0] in alive_enemy_ids
        }
        self._active_influences = [
            influence
            for influence in self._active_influences
            if influence.source_enemy_id is None or influence.source_enemy_id in alive_enemy_ids
        ]

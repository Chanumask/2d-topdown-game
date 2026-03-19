from __future__ import annotations

from typing import TYPE_CHECKING

from game.core.blessings import (
    BLESSING_COIN_VACUUM,
    BLESSING_DAMAGE_AURA,
    BLESSING_DIVINE_PURGE,
    BLESSING_SACRED_RENEWAL,
    BlessingCategory,
    BlessingDefinition,
    get_blessing,
)
from game.core.enemies import EnemyTier

if TYPE_CHECKING:
    from game.core.world import World


class BlessingSystem:
    def apply_blessing(self, world: World, collector_player_id: str, blessing_id: str) -> None:
        definition = get_blessing(blessing_id)
        if definition is None:
            return
        animated_effect_id = definition.animated_effect_id

        if blessing_id == BLESSING_COIN_VACUUM:
            self._apply_coin_vacuum(world, collector_player_id)
            return
        if blessing_id == BLESSING_SACRED_RENEWAL:
            self._apply_sacred_renewal(world, animated_effect_id=animated_effect_id)
            return
        if blessing_id == BLESSING_DIVINE_PURGE:
            self._apply_divine_purge(
                world,
                collector_player_id,
                animated_effect_id=animated_effect_id,
            )
            return
        if blessing_id == BLESSING_DAMAGE_AURA:
            self._apply_damage_aura(world, collector_player_id)
            return
        if (
            definition.category is BlessingCategory.RUN_BOON
            and not definition.run_boon_modifier.is_neutral()
        ):
            self._apply_run_boon(world, collector_player_id, definition)

    @staticmethod
    def _apply_coin_vacuum(world: World, collector_player_id: str) -> None:
        world.activate_coin_vacuum(collector_player_id)

    @staticmethod
    def _apply_sacred_renewal(world: World, animated_effect_id: str | None) -> None:
        for player in world.players.values():
            player.health = player.max_health
            player.alive = True
            if animated_effect_id is not None:
                world.emit_world_vfx(animated_effect_id, player.position.copy())

    @staticmethod
    def _apply_divine_purge(
        world: World,
        collector_player_id: str,
        animated_effect_id: str | None,
    ) -> None:
        alive_enemies = [enemy for enemy in world.enemies.values() if enemy.alive]
        for enemy in alive_enemies:
            if enemy.tier == EnemyTier.BOSS.value:
                continue

            if animated_effect_id is not None:
                world.emit_world_vfx(animated_effect_id, enemy.position.copy())

            if enemy.tier == EnemyTier.ELITE.value:
                elite_damage = max(1, (int(enemy.health) + 1) // 2)
                world.damage_enemy(
                    enemy,
                    elite_damage,
                    killer_player_id=collector_player_id,
                    trigger_run_boons=False,
                )
                continue

            world.defeat_enemy(enemy, killer_player_id=collector_player_id)

    @staticmethod
    def _apply_damage_aura(world: World, collector_player_id: str) -> None:
        world.activate_damage_aura(collector_player_id)

    @staticmethod
    def _apply_run_boon(
        world: World,
        collector_player_id: str,
        definition: BlessingDefinition,
    ) -> None:
        collector = world.players.get(collector_player_id)
        if collector is None:
            return
        modifier = definition.run_boon_modifier
        collector.coin_heal_on_pickup += int(modifier.coin_heal_on_pickup)
        collector.golden_momentum_stacks += int(modifier.golden_momentum_stacks)
        collector.fury_stacks += int(modifier.fury_stacks)
        collector.chilling_field_stacks += int(modifier.chilling_field_stacks)
        collector.chain_spark_stacks += int(modifier.chain_spark_stacks)
        collector.impact_pulse_stacks += int(modifier.impact_pulse_stacks)

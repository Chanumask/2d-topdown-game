from __future__ import annotations

from typing import TYPE_CHECKING

from game.core.blessings import (
    BLESSING_COIN_VACUUM,
    BLESSING_DAMAGE_AURA,
    BLESSING_DIVINE_PURGE,
    BLESSING_SACRED_RENEWAL,
    get_blessing,
)

if TYPE_CHECKING:
    from game.core.world import World


class BlessingSystem:
    def apply_blessing(self, world: World, collector_player_id: str, blessing_id: str) -> None:
        definition = get_blessing(blessing_id)
        animated_effect_id = definition.animated_effect_id if definition is not None else None

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
            if animated_effect_id is not None:
                world.emit_world_vfx(animated_effect_id, enemy.position.copy())
            world.defeat_enemy(enemy, killer_player_id=collector_player_id)

    @staticmethod
    def _apply_damage_aura(world: World, collector_player_id: str) -> None:
        world.activate_damage_aura(collector_player_id)

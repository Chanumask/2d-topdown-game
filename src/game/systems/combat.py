from __future__ import annotations

from typing import TYPE_CHECKING

from game.entities import Player, Projectile
from game.systems.collision import circles_overlap

if TYPE_CHECKING:
    from game.core.world import World


class CombatSystem:
    def __init__(
        self,
        projectile_speed: float,
        projectile_damage: int,
        projectile_ttl_seconds: float,
        projectile_radius: float,
    ) -> None:
        self.projectile_speed = projectile_speed
        self.projectile_damage = projectile_damage
        self.projectile_ttl_seconds = projectile_ttl_seconds
        self.projectile_radius = projectile_radius

    def try_throw_projectile(self, world: World, player: Player) -> bool:
        if not player.can_throw() or not player.alive:
            return False

        direction = player.aim_position - player.position
        if direction.length_squared() == 0:
            return False

        velocity = direction.normalized() * self.projectile_speed
        world.spawn_projectile(
            position=player.position.copy(),
            velocity=velocity,
            owner_player_id=player.player_id,
            damage=self.projectile_damage,
            ttl_seconds=self.projectile_ttl_seconds,
            radius=self.projectile_radius,
        )
        player.on_projectile_thrown(world.tick)
        return True

    def update_projectiles(self, world: World, dt: float) -> None:
        for projectile in world.projectiles.values():
            projectile.update(dt)

            if not self._is_in_world_bounds(projectile, world.world_width, world.world_height):
                projectile.alive = False

    def resolve(self, world: World) -> None:
        self._projectile_hits_enemy(world)
        self._projectile_hits_player(world)
        self._enemy_contacts_player(world)

    def _projectile_hits_enemy(self, world: World) -> None:
        for projectile in world.projectiles.values():
            if not projectile.alive:
                continue
            if projectile.source_faction != "player":
                continue

            for enemy in world.enemies.values():
                if not enemy.alive:
                    continue
                if not circles_overlap(
                    projectile.position,
                    projectile.radius,
                    enemy.position,
                    enemy.radius,
                ):
                    continue

                world.damage_enemy(
                    enemy,
                    projectile.damage,
                    killer_player_id=projectile.owner_player_id or None,
                    source_player_id=projectile.owner_player_id or None,
                    trigger_run_boons=True,
                )
                projectile.alive = False
                break

    def _projectile_hits_player(self, world: World) -> None:
        for projectile in world.projectiles.values():
            if not projectile.alive:
                continue
            if projectile.source_faction != "enemy":
                continue

            for player in world.players.values():
                if not player.alive:
                    continue
                if not circles_overlap(
                    projectile.position,
                    projectile.radius,
                    player.position,
                    player.radius,
                ):
                    continue

                world.apply_player_damage(player, projectile.damage)
                projectile.alive = False
                break

    def _enemy_contacts_player(self, world: World) -> None:
        for enemy in world.enemies.values():
            if not enemy.alive:
                continue

            for player in world.players.values():
                if not player.alive:
                    continue
                if not circles_overlap(
                    player.position, player.radius, enemy.position, enemy.radius
                ):
                    continue

                if world.handle_enemy_player_contact(enemy, player):
                    continue
                world.apply_player_damage(player, enemy.touch_damage)

    @staticmethod
    def _is_in_world_bounds(projectile: Projectile, width: float, height: float) -> bool:
        x = projectile.position.x
        y = projectile.position.y
        return 0.0 <= x <= width and 0.0 <= y <= height

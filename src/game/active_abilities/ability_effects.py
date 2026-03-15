from __future__ import annotations

import math
from dataclasses import dataclass
from typing import TYPE_CHECKING

from game.entities.entity import Vec2

if TYPE_CHECKING:
    from game.core.world import World
    from game.entities.enemy import Enemy
    from game.entities.player import Player


@dataclass(slots=True)
class ShockwaveResult:
    enemies_hit: int = 0


def apply_shockwave(world: World, player: Player, stats: dict[str, float]) -> ShockwaveResult:
    attack_direction = resolve_attack_direction(player)
    max_range = max(1.0, float(stats.get("range", 0.0)))
    cone_degrees = max(1.0, min(359.0, float(stats.get("cone_degrees", 60.0))))
    damage = max(1, int(round(float(stats.get("damage", 1.0)))))

    half_angle_cos = math.cos(math.radians(cone_degrees * 0.5))
    result = ShockwaveResult()
    for enemy in list(world.enemies.values()):
        if not enemy.alive:
            continue
        if not _enemy_in_cone(player, enemy, attack_direction, max_range, half_angle_cos):
            continue

        enemy.take_damage(damage)
        result.enemies_hit += 1
        if not enemy.alive:
            world.resolve_enemy_damage_defeat(enemy, killer_player_id=player.player_id)

    return result


def try_fire_frenzy_projectile(
    world: World,
    player: Player,
    stats: dict[str, float],
) -> bool:
    direction = _resolve_frenzy_direction(world, player, stats)
    if direction.length_squared() <= 0.0:
        return False

    projectile_damage = max(
        1,
        int(
            round(
                float(world.combat.projectile_damage)
                * max(0.05, float(stats.get("projectile_damage_multiplier", 1.0)))
            )
        ),
    )

    world.spawn_projectile(
        position=player.position.copy(),
        velocity=direction.normalized() * float(world.combat.projectile_speed),
        owner_player_id=player.player_id,
        damage=projectile_damage,
        ttl_seconds=float(world.combat.projectile_ttl_seconds),
        radius=float(world.combat.projectile_radius),
    )
    player.on_projectile_thrown(world.tick)
    return True


def _enemy_in_cone(
    player: Player,
    enemy: Enemy,
    attack_direction: Vec2,
    max_range: float,
    half_angle_cos: float,
) -> bool:
    to_enemy = enemy.position - player.position
    distance_sq = to_enemy.length_squared()
    if distance_sq <= 0.0:
        return True
    if distance_sq > max_range * max_range:
        return False

    enemy_direction = to_enemy.normalized()
    dot = (attack_direction.x * enemy_direction.x) + (attack_direction.y * enemy_direction.y)
    return dot >= half_angle_cos


def _resolve_attack_direction(player: Player) -> Vec2:
    aim_delta = player.aim_position - player.position
    if aim_delta.length_squared() > 0.0:
        return aim_delta.normalized()
    if player.velocity.length_squared() > 0.0:
        return player.velocity.normalized()
    return Vec2(1.0, 0.0)


def resolve_attack_direction(player: Player) -> Vec2:
    return _resolve_attack_direction(player)


def _resolve_frenzy_direction(world: World, player: Player, stats: dict[str, float]) -> Vec2:
    max_range = max(1.0, float(stats.get("auto_target_range", 320.0)))
    nearest_enemy: Enemy | None = None
    nearest_distance_sq = float("inf")

    for enemy in world.enemies.values():
        if not enemy.alive:
            continue
        to_enemy = enemy.position - player.position
        distance_sq = to_enemy.length_squared()
        if distance_sq > max_range * max_range:
            continue
        if distance_sq < nearest_distance_sq:
            nearest_enemy = enemy
            nearest_distance_sq = distance_sq

    if nearest_enemy is not None:
        return nearest_enemy.position - player.position

    return player.aim_position - player.position

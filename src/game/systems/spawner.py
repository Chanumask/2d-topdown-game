from __future__ import annotations

import random
from typing import TYPE_CHECKING

from game.entities import Vec2

if TYPE_CHECKING:
    from game.core.world import World


class EnemySpawner:
    def __init__(
        self,
        rng: random.Random,
        base_interval_seconds: float,
        min_interval_seconds: float,
        acceleration_per_second: float,
    ) -> None:
        self.rng = rng
        self.base_interval_seconds = base_interval_seconds
        self.min_interval_seconds = min_interval_seconds
        self.acceleration_per_second = acceleration_per_second
        self.timer = base_interval_seconds

    def update(self, world: World, dt: float) -> None:
        self.timer -= dt
        spawn_interval = self.current_interval(world.simulation_time)

        while self.timer <= 0.0:
            self._spawn_enemy(world)
            self.timer += spawn_interval

    def current_interval(self, elapsed_seconds: float) -> float:
        return max(
            self.min_interval_seconds,
            self.base_interval_seconds - (elapsed_seconds * self.acceleration_per_second),
        )

    def _spawn_enemy(self, world: World) -> None:
        spawn_position = self._random_edge_position(world.world_width, world.world_height)

        elapsed = world.simulation_time
        health_bonus = int(elapsed // 25.0) * 4
        speed_bonus = (elapsed // 18.0) * 3.0

        world.spawn_enemy(
            position=spawn_position,
            health=world.settings.enemy_base_health + health_bonus,
            speed=world.settings.enemy_base_speed + speed_bonus,
            touch_damage=world.settings.enemy_touch_damage,
        )

    def _random_edge_position(self, world_width: float, world_height: float) -> Vec2:
        edge = self.rng.choice(("top", "bottom", "left", "right"))
        if edge == "top":
            return Vec2(self.rng.uniform(0.0, world_width), 0.0)
        if edge == "bottom":
            return Vec2(self.rng.uniform(0.0, world_width), world_height)
        if edge == "left":
            return Vec2(0.0, self.rng.uniform(0.0, world_height))
        return Vec2(world_width, self.rng.uniform(0.0, world_height))

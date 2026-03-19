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
        boss_profile_id = world.enemy_director.consume_boss_spawn_profile_id(world)
        if boss_profile_id:
            self._spawn_enemy(world, profile_id=boss_profile_id)
            self.timer = self.current_interval(
                world.simulation_time,
                interval_multiplier=world.enemy_director.current_spawn_interval_multiplier(world),
            )
            return

        self.timer -= dt
        spawn_interval = self.current_interval(
            world.simulation_time,
            interval_multiplier=world.enemy_director.current_spawn_interval_multiplier(world),
        )

        while self.timer <= 0.0:
            spawn_count = 1 + world.enemy_director.current_spawn_batch_bonus(world)
            for _ in range(max(1, spawn_count)):
                self._spawn_enemy(world)
            self.timer += spawn_interval

    def current_interval(self, elapsed_seconds: float, interval_multiplier: float = 1.0) -> float:
        base_interval = max(
            self.min_interval_seconds,
            self.base_interval_seconds - (elapsed_seconds * self.acceleration_per_second),
        )
        return max(self.min_interval_seconds * 0.25, base_interval * max(0.1, interval_multiplier))

    def _spawn_enemy(self, world: World, profile_id: str | None = None) -> None:
        spawn_position = self._random_edge_position(world.world_width, world.world_height)
        world.spawn_enemy(position=spawn_position, profile_id=profile_id)

    def _random_edge_position(self, world_width: float, world_height: float) -> Vec2:
        edge = self.rng.choice(("top", "bottom", "left", "right"))
        if edge == "top":
            return Vec2(self.rng.uniform(0.0, world_width), 0.0)
        if edge == "bottom":
            return Vec2(self.rng.uniform(0.0, world_width), world_height)
        if edge == "left":
            return Vec2(0.0, self.rng.uniform(0.0, world_height))
        return Vec2(world_width, self.rng.uniform(0.0, world_height))

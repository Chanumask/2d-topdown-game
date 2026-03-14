from dataclasses import dataclass, field

from game.core.enemies import EnemyStats, EnemyTier
from game.core.enemy_catalog import CRIMSON_IMP_PROFILE_ID
from game.entities.entity import Entity, Vec2, clamp_to_world, vec2_from_payload


@dataclass(slots=True)
class Enemy(Entity):
    profile_id: str = CRIMSON_IMP_PROFILE_ID
    tier: str = EnemyTier.NORMAL.value
    tags: tuple[str, ...] = ()
    active_ability_id: str | None = None
    active_ability_vfx_id: str | None = None
    ability_timer_seconds: float = 0.0
    velocity: Vec2 = field(default_factory=lambda: Vec2(0.0, 0.0))
    base_radius: float = 12.0
    base_speed: float = 70.0
    base_max_health: int = 30
    base_touch_damage: int = 10
    base_coin_drop_value: int = 1
    speed: float = 70.0
    max_health: int = 30
    health: int = 30
    touch_damage: int = 10
    coin_drop_value: int = 1

    def update(self, dt: float, world_width: float, world_height: float) -> None:
        self.position.x += self.velocity.x * dt
        self.position.y += self.velocity.y * dt
        clamp_to_world(self.position, self.radius, world_width, world_height)

    def chase(self, target_position: Vec2) -> None:
        direction = target_position - self.position
        if direction.length_squared() == 0:
            self.velocity = Vec2(0.0, 0.0)
            return

        self.velocity = direction.normalized() * self.speed

    def take_damage(self, amount: int) -> None:
        self.health -= amount
        if self.health <= 0:
            self.alive = False

    def arm_ability(
        self,
        ability_id: str,
        *,
        timer_seconds: float,
        vfx_effect_id: str | None,
    ) -> None:
        self.active_ability_id = ability_id
        self.active_ability_vfx_id = vfx_effect_id
        self.ability_timer_seconds = max(0.0, float(timer_seconds))
        self.velocity = Vec2(0.0, 0.0)

    def clear_ability_state(self) -> None:
        self.active_ability_id = None
        self.active_ability_vfx_id = None
        self.ability_timer_seconds = 0.0

    def base_stats(self) -> EnemyStats:
        return EnemyStats(
            max_health=self.base_max_health,
            speed=self.base_speed,
            touch_damage=self.base_touch_damage,
            coin_drop_value=self.base_coin_drop_value,
            radius=self.base_radius,
        )

    def apply_runtime_stats(self, stats: EnemyStats) -> None:
        previous_max_health = max(1, int(self.max_health))
        missing_health = max(0, previous_max_health - int(self.health))
        self.radius = float(stats.radius)
        self.speed = float(stats.speed)
        self.touch_damage = int(stats.touch_damage)
        self.coin_drop_value = int(stats.coin_drop_value)
        self.max_health = int(stats.max_health)
        self.health = max(0, self.max_health - missing_health)
        if self.health <= 0:
            self.alive = False

    def to_dict(self) -> dict[str, object]:
        payload = self.base_to_dict()
        payload.update(
            {
                "profile_id": self.profile_id,
                "tier": self.tier,
                "tags": list(self.tags),
                "active_ability_id": self.active_ability_id,
                "active_ability_vfx_id": self.active_ability_vfx_id,
                "ability_timer_seconds": float(self.ability_timer_seconds),
                "velocity": self.velocity.to_dict(),
                "base_radius": float(self.base_radius),
                "base_speed": float(self.base_speed),
                "base_max_health": self.base_max_health,
                "base_touch_damage": self.base_touch_damage,
                "base_coin_drop_value": self.base_coin_drop_value,
                "speed": float(self.speed),
                "max_health": self.max_health,
                "health": self.health,
                "touch_damage": self.touch_damage,
                "coin_drop_value": self.coin_drop_value,
            }
        )
        return payload

    @classmethod
    def from_dict(cls, payload: dict[str, object]) -> "Enemy":
        return cls(
            entity_id=int(payload.get("entity_id", 0)),
            position=vec2_from_payload(payload, "position"),
            radius=float(payload.get("radius", 0.0)),
            alive=bool(payload.get("alive", True)),
            profile_id=str(payload.get("profile_id", CRIMSON_IMP_PROFILE_ID)),
            tier=str(payload.get("tier", EnemyTier.NORMAL.value)),
            tags=tuple(str(tag) for tag in payload.get("tags", [])),
            active_ability_id=(
                str(payload.get("active_ability_id"))
                if payload.get("active_ability_id") not in (None, "")
                else None
            ),
            active_ability_vfx_id=(
                str(payload.get("active_ability_vfx_id"))
                if payload.get("active_ability_vfx_id") not in (None, "")
                else None
            ),
            ability_timer_seconds=float(payload.get("ability_timer_seconds", 0.0)),
            velocity=vec2_from_payload(payload, "velocity"),
            base_radius=float(payload.get("base_radius", payload.get("radius", 12.0))),
            base_speed=float(payload.get("base_speed", payload.get("speed", 70.0))),
            base_max_health=int(payload.get("base_max_health", payload.get("max_health", 30))),
            base_touch_damage=int(
                payload.get("base_touch_damage", payload.get("touch_damage", 10))
            ),
            base_coin_drop_value=int(
                payload.get("base_coin_drop_value", payload.get("coin_drop_value", 1))
            ),
            speed=float(payload.get("speed", 70.0)),
            max_health=int(payload.get("max_health", 30)),
            health=int(payload.get("health", 30)),
            touch_damage=int(payload.get("touch_damage", 10)),
            coin_drop_value=int(payload.get("coin_drop_value", 1)),
        )

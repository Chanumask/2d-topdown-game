from dataclasses import dataclass, field

from game.entities.entity import Entity, Vec2, clamp_to_world, vec2_from_payload


@dataclass(slots=True)
class Enemy(Entity):
    velocity: Vec2 = field(default_factory=lambda: Vec2(0.0, 0.0))
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

    def to_dict(self) -> dict[str, object]:
        payload = self.base_to_dict()
        payload.update(
            {
                "velocity": self.velocity.to_dict(),
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
            velocity=vec2_from_payload(payload, "velocity"),
            speed=float(payload.get("speed", 70.0)),
            max_health=int(payload.get("max_health", 30)),
            health=int(payload.get("health", 30)),
            touch_damage=int(payload.get("touch_damage", 10)),
            coin_drop_value=int(payload.get("coin_drop_value", 1)),
        )

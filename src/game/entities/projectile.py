from dataclasses import dataclass, field

from game.entities.entity import Entity, Vec2, vec2_from_payload


@dataclass(slots=True)
class Projectile(Entity):
    owner_player_id: str = ""
    velocity: Vec2 = field(default_factory=lambda: Vec2(0.0, 0.0))
    damage: int = 15
    ttl_seconds: float = 1.3

    def update(self, dt: float) -> None:
        self.position.x += self.velocity.x * dt
        self.position.y += self.velocity.y * dt
        self.ttl_seconds -= dt
        if self.ttl_seconds <= 0.0:
            self.alive = False

    def to_dict(self) -> dict[str, object]:
        payload = self.base_to_dict()
        payload.update(
            {
                "owner_player_id": self.owner_player_id,
                "velocity": self.velocity.to_dict(),
                "damage": self.damage,
                "ttl_seconds": float(self.ttl_seconds),
            }
        )
        return payload

    @classmethod
    def from_dict(cls, payload: dict[str, object]) -> "Projectile":
        return cls(
            entity_id=int(payload.get("entity_id", 0)),
            position=vec2_from_payload(payload, "position"),
            radius=float(payload.get("radius", 0.0)),
            alive=bool(payload.get("alive", True)),
            owner_player_id=str(payload.get("owner_player_id", "")),
            velocity=vec2_from_payload(payload, "velocity"),
            damage=int(payload.get("damage", 15)),
            ttl_seconds=float(payload.get("ttl_seconds", 1.3)),
        )

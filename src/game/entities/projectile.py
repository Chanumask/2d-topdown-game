from dataclasses import dataclass, field

from game.entities.entity import Entity, Vec2, vec2_from_payload


@dataclass(slots=True)
class Projectile(Entity):
    owner_player_id: str = ""
    source_faction: str = "player"
    projectile_effect_id: str | None = None
    velocity: Vec2 = field(default_factory=lambda: Vec2(0.0, 0.0))
    damage: int = 15
    damage_fraction_of_target_max_health: float = 0.0
    on_hit_move_speed_multiplier: float = 1.0
    on_hit_slow_duration_seconds: float = 0.0
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
                "source_faction": self.source_faction,
                "projectile_effect_id": self.projectile_effect_id,
                "velocity": self.velocity.to_dict(),
                "damage": self.damage,
                "damage_fraction_of_target_max_health": float(
                    self.damage_fraction_of_target_max_health
                ),
                "on_hit_move_speed_multiplier": float(self.on_hit_move_speed_multiplier),
                "on_hit_slow_duration_seconds": float(self.on_hit_slow_duration_seconds),
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
            source_faction=str(payload.get("source_faction", "player")),
            projectile_effect_id=(
                str(payload.get("projectile_effect_id"))
                if payload.get("projectile_effect_id") not in (None, "")
                else None
            ),
            velocity=vec2_from_payload(payload, "velocity"),
            damage=int(payload.get("damage", 15)),
            damage_fraction_of_target_max_health=float(
                payload.get("damage_fraction_of_target_max_health", 0.0)
            ),
            on_hit_move_speed_multiplier=float(payload.get("on_hit_move_speed_multiplier", 1.0)),
            on_hit_slow_duration_seconds=float(payload.get("on_hit_slow_duration_seconds", 0.0)),
            ttl_seconds=float(payload.get("ttl_seconds", 1.3)),
        )

from dataclasses import dataclass, field

from game.entities.entity import Entity, Vec2, clamp_to_world, vec2_from_payload


@dataclass(slots=True)
class Player(Entity):
    player_id: str = ""
    character_id: str = ""
    velocity: Vec2 = field(default_factory=lambda: Vec2(0.0, 0.0))
    speed: float = 250.0
    max_health: int = 100
    health: int = 100
    coin_pickup_radius: float = 14.0
    aim_position: Vec2 = field(default_factory=lambda: Vec2(0.0, 0.0))
    coins: int = 0
    throw_cooldown_seconds: float = 0.35
    throw_cooldown_remaining: float = 0.0
    last_attack_tick: int = -1
    damage_iframe_seconds: float = 0.4
    damage_iframe_remaining: float = 0.0

    def update(self, dt: float, world_width: float, world_height: float) -> None:
        self.position.x += self.velocity.x * dt
        self.position.y += self.velocity.y * dt
        clamp_to_world(self.position, self.radius, world_width, world_height)

        self.throw_cooldown_remaining = max(0.0, self.throw_cooldown_remaining - dt)
        self.damage_iframe_remaining = max(0.0, self.damage_iframe_remaining - dt)

    def set_movement(self, move_x: float, move_y: float) -> None:
        direction = Vec2(move_x, move_y)
        if direction.length_squared() == 0:
            self.velocity = Vec2(0.0, 0.0)
            return

        normalized = direction.normalized()
        self.velocity = normalized * self.speed

    def can_throw(self) -> bool:
        return self.throw_cooldown_remaining <= 0.0 and self.alive

    def on_projectile_thrown(self, attack_tick: int | None = None) -> None:
        self.throw_cooldown_remaining = self.throw_cooldown_seconds
        if attack_tick is not None:
            self.last_attack_tick = attack_tick

    def take_damage(self, amount: int) -> None:
        if self.damage_iframe_remaining > 0.0 or not self.alive:
            return

        self.health = max(0, self.health - amount)
        self.damage_iframe_remaining = self.damage_iframe_seconds
        if self.health <= 0:
            self.alive = False

    def to_dict(self) -> dict[str, object]:
        payload = self.base_to_dict()
        payload.update(
            {
                "player_id": self.player_id,
                "character_id": self.character_id,
                "velocity": self.velocity.to_dict(),
                "speed": float(self.speed),
                "max_health": self.max_health,
                "health": self.health,
                "coin_pickup_radius": float(self.coin_pickup_radius),
                "aim_position": self.aim_position.to_dict(),
                "coins": self.coins,
                "throw_cooldown_seconds": float(self.throw_cooldown_seconds),
                "throw_cooldown_remaining": float(self.throw_cooldown_remaining),
                "last_attack_tick": int(self.last_attack_tick),
                "damage_iframe_seconds": float(self.damage_iframe_seconds),
                "damage_iframe_remaining": float(self.damage_iframe_remaining),
            }
        )
        return payload

    @classmethod
    def from_dict(cls, payload: dict[str, object]) -> "Player":
        return cls(
            entity_id=int(payload.get("entity_id", 0)),
            player_id=str(payload.get("player_id", "")),
            character_id=str(payload.get("character_id", "")),
            position=vec2_from_payload(payload, "position"),
            radius=float(payload.get("radius", 0.0)),
            alive=bool(payload.get("alive", True)),
            velocity=vec2_from_payload(payload, "velocity"),
            speed=float(payload.get("speed", 250.0)),
            max_health=int(payload.get("max_health", 100)),
            health=int(payload.get("health", 100)),
            coin_pickup_radius=float(payload.get("coin_pickup_radius", payload.get("radius", 0.0))),
            aim_position=vec2_from_payload(payload, "aim_position"),
            coins=int(payload.get("coins", 0)),
            throw_cooldown_seconds=float(
                payload.get(
                    "throw_cooldown_seconds",
                    payload.get("shoot_cooldown_seconds", 0.35),
                )
            ),
            throw_cooldown_remaining=float(
                payload.get(
                    "throw_cooldown_remaining",
                    payload.get("shoot_cooldown_remaining", 0.0),
                )
            ),
            last_attack_tick=int(payload.get("last_attack_tick", -1)),
            damage_iframe_seconds=float(payload.get("damage_iframe_seconds", 0.4)),
            damage_iframe_remaining=float(payload.get("damage_iframe_remaining", 0.0)),
        )

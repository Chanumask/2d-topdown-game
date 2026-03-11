from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(slots=True)
class Vec2:
    x: float
    y: float

    def copy(self) -> Vec2:
        return Vec2(self.x, self.y)

    def __add__(self, other: Vec2) -> Vec2:
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vec2) -> Vec2:
        return Vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> Vec2:
        return Vec2(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: float) -> Vec2:
        return self.__mul__(scalar)

    def length_squared(self) -> float:
        return (self.x * self.x) + (self.y * self.y)

    def length(self) -> float:
        return math.sqrt(self.length_squared())

    def normalized(self) -> Vec2:
        magnitude = self.length()
        if magnitude == 0:
            return Vec2(0.0, 0.0)
        return Vec2(self.x / magnitude, self.y / magnitude)

    def to_dict(self) -> dict[str, float]:
        return {"x": float(self.x), "y": float(self.y)}

    @classmethod
    def from_dict(cls, payload: dict[str, object]) -> Vec2:
        return cls(x=float(payload.get("x", 0.0)), y=float(payload.get("y", 0.0)))


@dataclass(slots=True)
class Entity:
    entity_id: int
    position: Vec2
    radius: float
    alive: bool = True

    def base_to_dict(self) -> dict[str, int | float | bool | dict[str, float]]:
        return {
            "entity_id": self.entity_id,
            "position": self.position.to_dict(),
            "radius": float(self.radius),
            "alive": self.alive,
        }


def vec2_from_payload(
    payload: dict[str, object],
    key: str,
    default: tuple[float, float] = (0.0, 0.0),
) -> Vec2:
    maybe_position = payload.get(key)
    if isinstance(maybe_position, dict):
        return Vec2.from_dict(maybe_position)
    return Vec2(*default)


def clamp_to_world(position: Vec2, radius: float, width: float, height: float) -> None:
    position.x = max(radius, min(position.x, width - radius))
    position.y = max(radius, min(position.y, height - radius))

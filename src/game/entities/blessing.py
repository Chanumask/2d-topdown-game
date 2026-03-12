from dataclasses import dataclass

from game.entities.entity import Entity, vec2_from_payload


@dataclass(slots=True)
class Blessing(Entity):
    blessing_id: str = ""

    def to_dict(self) -> dict[str, object]:
        payload = self.base_to_dict()
        payload.update({"blessing_id": self.blessing_id})
        return payload

    @classmethod
    def from_dict(cls, payload: dict[str, object]) -> "Blessing":
        return cls(
            entity_id=int(payload.get("entity_id", 0)),
            position=vec2_from_payload(payload, "position"),
            radius=float(payload.get("radius", 0.0)),
            alive=bool(payload.get("alive", True)),
            blessing_id=str(payload.get("blessing_id", "")),
        )

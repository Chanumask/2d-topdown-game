from dataclasses import dataclass

PlayerId = str


@dataclass(slots=True)
class PlayerActions:
    move_up: bool = False
    move_down: bool = False
    move_left: bool = False
    move_right: bool = False
    aim_position: tuple[float, float] | None = None
    throw: bool = False
    throw_pressed: bool = False
    throw_held: bool = False

    @property
    def move_x(self) -> float:
        return float(self.move_right) - float(self.move_left)

    @property
    def move_y(self) -> float:
        return float(self.move_down) - float(self.move_up)

    def to_dict(self) -> dict[str, bool | float | dict[str, float] | None]:
        aim = None
        if self.aim_position is not None:
            aim = {"x": float(self.aim_position[0]), "y": float(self.aim_position[1])}

        return {
            "move_up": self.move_up,
            "move_down": self.move_down,
            "move_left": self.move_left,
            "move_right": self.move_right,
            "aim": aim,
            "throw": self.throw,
            "throw_pressed": self.throw_pressed,
            "throw_held": self.throw_held,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, object]) -> "PlayerActions":
        aim_payload = payload.get("aim")
        aim_position: tuple[float, float] | None = None

        if isinstance(aim_payload, dict):
            aim_x = float(aim_payload.get("x", 0.0))
            aim_y = float(aim_payload.get("y", 0.0))
            aim_position = (aim_x, aim_y)

        throw_pressed = bool(payload.get("throw_pressed", False))
        throw_held = bool(payload.get("throw_held", False))
        throw = bool(payload.get("throw", payload.get("shoot", False)))

        return cls(
            move_up=bool(payload.get("move_up", False)),
            move_down=bool(payload.get("move_down", False)),
            move_left=bool(payload.get("move_left", False)),
            move_right=bool(payload.get("move_right", False)),
            aim_position=aim_position,
            throw=(throw or throw_pressed or throw_held),
            throw_pressed=throw_pressed,
            throw_held=throw_held,
        )

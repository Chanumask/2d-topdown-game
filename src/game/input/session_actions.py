from dataclasses import dataclass


@dataclass(slots=True)
class SessionActions:
    request_pause: bool = False
    ready_up: bool = False

    def to_dict(self) -> dict[str, bool]:
        return {
            "request_pause": self.request_pause,
            "ready_up": self.ready_up,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, object]) -> "SessionActions":
        return cls(
            request_pause=bool(payload.get("request_pause", False)),
            ready_up=bool(payload.get("ready_up", False)),
        )

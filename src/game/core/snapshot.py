from dataclasses import dataclass


@dataclass(slots=True)
class WorldSnapshot:
    tick: int
    simulation_time: float
    run_state: str
    world: dict[str, float]
    session: dict[str, object]
    players: list[dict[str, object]]
    enemies: list[dict[str, object]]
    projectiles: list[dict[str, object]]
    coins: list[dict[str, object]]
    score: dict[str, object]
    difficulty: dict[str, object]

    def to_dict(self) -> dict[str, object]:
        return {
            "tick": self.tick,
            "simulation_time": self.simulation_time,
            "run_state": self.run_state,
            "world": self.world,
            "session": self.session,
            "players": self.players,
            "enemies": self.enemies,
            "projectiles": self.projectiles,
            "coins": self.coins,
            "score": self.score,
            "difficulty": self.difficulty,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, object]) -> "WorldSnapshot":
        score_payload = payload.get("score")
        difficulty_payload = payload.get("difficulty")
        world_payload = payload.get("world")
        session_payload = payload.get("session")
        return cls(
            tick=int(payload.get("tick", 0)),
            simulation_time=float(payload.get("simulation_time", 0.0)),
            run_state=str(payload.get("run_state", "running")),
            world=world_payload if isinstance(world_payload, dict) else {},
            session=session_payload if isinstance(session_payload, dict) else {},
            players=list(payload.get("players", [])),
            enemies=list(payload.get("enemies", [])),
            projectiles=list(payload.get("projectiles", [])),
            coins=list(payload.get("coins", [])),
            score=score_payload if isinstance(score_payload, dict) else {},
            difficulty=difficulty_payload if isinstance(difficulty_payload, dict) else {},
        )

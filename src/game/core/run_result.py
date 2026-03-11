from dataclasses import dataclass


@dataclass(slots=True)
class RunResult:
    survival_time_seconds: float
    total_run_coins: int
    coins_by_player: dict[str, int]
    enemies_killed_total: int
    enemies_killed_by_player: dict[str, int]
    players: list[str]
    tick: int
    simulation_time: float

    def to_dict(self) -> dict[str, object]:
        return {
            "survival_time_seconds": self.survival_time_seconds,
            "total_run_coins": self.total_run_coins,
            "coins_by_player": self.coins_by_player,
            "enemies_killed_total": self.enemies_killed_total,
            "enemies_killed_by_player": self.enemies_killed_by_player,
            "players": self.players,
            "tick": self.tick,
            "simulation_time": self.simulation_time,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, object]) -> "RunResult":
        raw_coins_by_player = payload.get("coins_by_player")
        raw_kills_by_player = payload.get("enemies_killed_by_player")
        coins_by_player = raw_coins_by_player if isinstance(raw_coins_by_player, dict) else {}
        kills_by_player = raw_kills_by_player if isinstance(raw_kills_by_player, dict) else {}

        return cls(
            survival_time_seconds=float(payload.get("survival_time_seconds", 0.0)),
            total_run_coins=int(payload.get("total_run_coins", 0)),
            coins_by_player={str(key): int(value) for key, value in coins_by_player.items()},
            enemies_killed_total=int(payload.get("enemies_killed_total", 0)),
            enemies_killed_by_player={
                str(key): int(value) for key, value in kills_by_player.items()
            },
            players=[str(player_id) for player_id in list(payload.get("players", []))],
            tick=int(payload.get("tick", 0)),
            simulation_time=float(payload.get("simulation_time", 0.0)),
        )

from dataclasses import dataclass, field
from enum import StrEnum


class MatchPhase(StrEnum):
    RUNNING = "running"
    PAUSE_COUNTDOWN = "pause_countdown"
    PAUSED = "paused"
    RESUME_COUNTDOWN = "resume_countdown"
    GAME_OVER = "game_over"


@dataclass(slots=True)
class SessionState:
    phase: MatchPhase = MatchPhase.RUNNING
    pause_requested_by: str | None = None
    countdown_remaining: float = 0.0
    ready_player_ids: set[str] = field(default_factory=set)
    pause_countdown_seconds: float = 3.0
    resume_countdown_seconds: float = 3.0

    def request_pause(self, player_id: str) -> None:
        if self.phase is not MatchPhase.RUNNING:
            return

        self.phase = MatchPhase.PAUSE_COUNTDOWN
        self.pause_requested_by = player_id
        self.countdown_remaining = self.pause_countdown_seconds
        self.ready_player_ids.clear()

    def mark_ready(self, player_id: str) -> None:
        if self.phase is MatchPhase.PAUSED:
            self.ready_player_ids.add(player_id)

    def clear_ready(self) -> None:
        self.ready_player_ids.clear()

    def all_players_ready(self, all_player_ids: set[str]) -> bool:
        return bool(all_player_ids) and all_player_ids.issubset(self.ready_player_ids)

    def start_paused(self) -> None:
        self.phase = MatchPhase.PAUSED
        self.countdown_remaining = 0.0

    def start_resume_countdown(self) -> None:
        self.phase = MatchPhase.RESUME_COUNTDOWN
        self.countdown_remaining = self.resume_countdown_seconds

    def resume_running(self) -> None:
        self.phase = MatchPhase.RUNNING
        self.pause_requested_by = None
        self.countdown_remaining = 0.0
        self.ready_player_ids.clear()

    def set_game_over(self) -> None:
        self.phase = MatchPhase.GAME_OVER
        self.countdown_remaining = 0.0

    def to_dict(self, all_player_ids: set[str]) -> dict[str, object]:
        return {
            "phase": self.phase.value,
            "pause_requested_by": self.pause_requested_by,
            "countdown_remaining": self.countdown_remaining,
            "ready_player_ids": sorted(self.ready_player_ids),
            "all_players_ready": self.all_players_ready(all_player_ids),
        }

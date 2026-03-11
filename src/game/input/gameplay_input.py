from dataclasses import dataclass, field

from game.input.actions import PlayerActions, PlayerId
from game.input.session_actions import SessionActions


@dataclass(slots=True)
class GameplayInputFrame:
    quit_requested: bool = False
    actions_by_player: dict[PlayerId, PlayerActions] = field(default_factory=dict)
    session_actions_by_player: dict[PlayerId, SessionActions] = field(default_factory=dict)

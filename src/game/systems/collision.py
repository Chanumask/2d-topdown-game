from __future__ import annotations

from game.entities import Player, Vec2


def circles_overlap(position_a: Vec2, radius_a: float, position_b: Vec2, radius_b: float) -> bool:
    delta = position_a - position_b
    radius_sum = radius_a + radius_b
    return delta.length_squared() <= radius_sum * radius_sum


def nearest_player(target: Vec2, players: dict[str, Player]) -> Player | None:
    alive_players = [player for player in players.values() if player.alive]
    if not alive_players:
        return None

    return min(
        alive_players,
        key=lambda player: (player.position - target).length_squared(),
    )

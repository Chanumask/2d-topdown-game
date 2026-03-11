from game.core.world import World
from game.input.actions import PlayerActions


class GameLoop:
    def __init__(
        self,
        world: World,
        simulation_hz: int,
        max_catchup_steps: int,
    ) -> None:
        self.world = world
        self.fixed_dt = 1.0 / float(simulation_hz)
        self.max_catchup_steps = max_catchup_steps
        self.accumulator = 0.0
        self.latest_actions_by_player: dict[str, PlayerActions] = {}

    def set_player_actions(self, actions_by_player: dict[str, PlayerActions]) -> None:
        self.latest_actions_by_player.update(actions_by_player)

    def advance(self, frame_dt: float) -> None:
        self.accumulator += min(frame_dt, 0.25)

        steps = 0
        while self.accumulator >= self.fixed_dt and steps < self.max_catchup_steps:
            for player_id, actions in self.latest_actions_by_player.items():
                self.world.apply_actions(player_id, actions)

            self.world.update(self.fixed_dt)
            self.accumulator -= self.fixed_dt
            steps += 1

        if steps == self.max_catchup_steps and self.accumulator >= self.fixed_dt:
            self.accumulator = 0.0

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
        self.pending_throw_requests: dict[str, bool] = {}
        self.pending_ability_requests: dict[str, bool] = {}

    def set_player_actions(self, actions_by_player: dict[str, PlayerActions]) -> None:
        for player_id, incoming_actions in actions_by_player.items():
            if incoming_actions.throw:
                self.pending_throw_requests[player_id] = True
            if incoming_actions.activate_ability or incoming_actions.activate_ability_pressed:
                self.pending_ability_requests[player_id] = True

            self.latest_actions_by_player[player_id] = PlayerActions(
                move_up=incoming_actions.move_up,
                move_down=incoming_actions.move_down,
                move_left=incoming_actions.move_left,
                move_right=incoming_actions.move_right,
                aim_position=incoming_actions.aim_position,
                throw=False,
                activate_ability=False,
            )

    def advance(self, frame_dt: float) -> None:
        self.accumulator += min(frame_dt, 0.25)

        steps = 0
        while self.accumulator >= self.fixed_dt and steps < self.max_catchup_steps:
            for player_id, base_actions in self.latest_actions_by_player.items():
                should_throw = self.pending_throw_requests.pop(player_id, False)
                should_activate_ability = self.pending_ability_requests.pop(player_id, False)
                tick_actions = PlayerActions(
                    move_up=base_actions.move_up,
                    move_down=base_actions.move_down,
                    move_left=base_actions.move_left,
                    move_right=base_actions.move_right,
                    aim_position=base_actions.aim_position,
                    throw=should_throw,
                    activate_ability=should_activate_ability,
                    activate_ability_pressed=should_activate_ability,
                )
                self.world.apply_actions(player_id, tick_actions)

            self.world.update(self.fixed_dt)
            self.accumulator -= self.fixed_dt
            steps += 1

        if steps == self.max_catchup_steps and self.accumulator >= self.fixed_dt:
            self.accumulator = 0.0

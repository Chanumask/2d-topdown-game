import pygame

from game.input.actions import PlayerActions, PlayerId
from game.input.gameplay_input import GameplayInputFrame
from game.input.session_actions import SessionActions


class InputHandler:
    def __init__(self, local_player_id: PlayerId) -> None:
        self.local_player_id = local_player_id

    def collect(self, events: list[pygame.event.Event]) -> GameplayInputFrame:
        throw_pressed = False
        request_pause_pressed = False
        quit_requested = False

        for event in events:
            if event.type == pygame.QUIT:
                quit_requested = True
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                throw_pressed = True
            elif event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_p):
                request_pause_pressed = True

        keys = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed(num_buttons=3)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        throw_held = bool(mouse_buttons[0])
        throw_intent = throw_pressed or throw_held
        request_pause_held = bool(keys[pygame.K_ESCAPE] or keys[pygame.K_p])
        request_pause = request_pause_pressed or request_pause_held

        gameplay_actions = PlayerActions(
            move_up=bool(keys[pygame.K_w]),
            move_down=bool(keys[pygame.K_s]),
            move_left=bool(keys[pygame.K_a]),
            move_right=bool(keys[pygame.K_d]),
            aim_position=(float(mouse_x), float(mouse_y)),
            throw=throw_intent,
            throw_pressed=throw_pressed,
            throw_held=throw_held,
        )
        session_actions = SessionActions(request_pause=request_pause)

        return GameplayInputFrame(
            quit_requested=quit_requested,
            actions_by_player={self.local_player_id: gameplay_actions},
            session_actions_by_player={self.local_player_id: session_actions},
        )

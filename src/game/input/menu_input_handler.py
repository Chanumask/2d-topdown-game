import pygame

from game.input.menu_actions import MenuActions


class MenuInputHandler:
    def collect(self, events: list[pygame.event.Event]) -> MenuActions:
        actions = MenuActions()
        mouse_position = pygame.mouse.get_pos()
        actions.mouse_position = (int(mouse_position[0]), int(mouse_position[1]))

        for event in events:
            if event.type == pygame.QUIT:
                actions.quit_requested = True
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w):
                    actions.navigate_up = True
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    actions.navigate_down = True
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    actions.navigate_left = True
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    actions.navigate_right = True
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    actions.select = True
                elif event.key in (pygame.K_ESCAPE, pygame.K_BACKSPACE):
                    actions.back = True
            elif event.type == pygame.MOUSEMOTION:
                actions.mouse_moved = True
                actions.mouse_position = (int(event.pos[0]), int(event.pos[1]))
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                actions.mouse_left_click = True
                actions.mouse_position = (int(event.pos[0]), int(event.pos[1]))

        return actions

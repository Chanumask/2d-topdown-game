import pygame

from game.core.game import GameApp


def main() -> None:
    pygame.init()
    try:
        GameApp().run()
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()

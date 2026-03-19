from dataclasses import dataclass


@dataclass(slots=True)
class MenuActions:
    quit_requested: bool = False
    navigate_up: bool = False
    navigate_down: bool = False
    navigate_left: bool = False
    navigate_right: bool = False
    select: bool = False
    back: bool = False
    mouse_position: tuple[int, int] | None = None
    mouse_moved: bool = False
    mouse_left_click: bool = False
    scroll_y: int = 0
    text_input: str = ""
    text_backspace: bool = False

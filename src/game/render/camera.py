from dataclasses import dataclass


@dataclass(slots=True)
class Camera:
    screen_width: int
    screen_height: int
    world_width: float
    world_height: float
    offset_x: float = 0.0
    offset_y: float = 0.0

    def set_viewport(self, width: int, height: int) -> None:
        self.screen_width = width
        self.screen_height = height

    def set_world_bounds(self, width: float, height: float) -> None:
        self.world_width = width
        self.world_height = height

    def update(self, focus_position: tuple[float, float] | None) -> None:
        centered_offset_x = min(0.0, (self.world_width - self.screen_width) * 0.5)
        centered_offset_y = min(0.0, (self.world_height - self.screen_height) * 0.5)

        if focus_position is None:
            self.offset_x = centered_offset_x
            self.offset_y = centered_offset_y
            return

        if self.world_width <= self.screen_width:
            self.offset_x = centered_offset_x
        else:
            target_x = focus_position[0] - (self.screen_width * 0.5)
            max_offset_x = self.world_width - self.screen_width
            self.offset_x = max(0.0, min(target_x, max_offset_x))

        if self.world_height <= self.screen_height:
            self.offset_y = centered_offset_y
        else:
            target_y = focus_position[1] - (self.screen_height * 0.5)
            max_offset_y = self.world_height - self.screen_height
            self.offset_y = max(0.0, min(target_y, max_offset_y))

    def world_to_screen(self, position: tuple[float, float]) -> tuple[int, int]:
        return (
            round(position[0] - self.offset_x),
            round(position[1] - self.offset_y),
        )

    def screen_to_world(self, position: tuple[float, float]) -> tuple[float, float]:
        return (position[0] + self.offset_x, position[1] + self.offset_y)

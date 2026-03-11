from dataclasses import dataclass


@dataclass(slots=True)
class Camera:
    screen_width: int
    screen_height: int
    world_width: float
    world_height: float
    dead_zone_width_ratio: float = 0.5
    dead_zone_height_ratio: float = 0.5
    offset_x: float = 0.0
    offset_y: float = 0.0

    def set_viewport(self, width: int, height: int) -> None:
        self.screen_width = width
        self.screen_height = height

    def set_world_bounds(self, width: float, height: float) -> None:
        self.world_width = width
        self.world_height = height

    def update(self, focus_position: tuple[float, float] | None) -> None:
        centered_offset_x = self._centered_offset(self.world_width, self.screen_width)
        centered_offset_y = self._centered_offset(self.world_height, self.screen_height)

        if focus_position is None:
            self.offset_x = centered_offset_x
            self.offset_y = centered_offset_y
            return

        if self.world_width <= self.screen_width:
            self.offset_x = centered_offset_x
        else:
            self.offset_x = self._update_axis_with_dead_zone(
                focus=focus_position[0],
                offset=self.offset_x,
                screen_size=float(self.screen_width),
                world_size=self.world_width,
                dead_zone_ratio=self.dead_zone_width_ratio,
            )

        if self.world_height <= self.screen_height:
            self.offset_y = centered_offset_y
        else:
            self.offset_y = self._update_axis_with_dead_zone(
                focus=focus_position[1],
                offset=self.offset_y,
                screen_size=float(self.screen_height),
                world_size=self.world_height,
                dead_zone_ratio=self.dead_zone_height_ratio,
            )

    def world_to_screen(self, position: tuple[float, float]) -> tuple[int, int]:
        return (
            round(position[0] - self.offset_x),
            round(position[1] - self.offset_y),
        )

    def screen_to_world(self, position: tuple[float, float]) -> tuple[float, float]:
        return (position[0] + self.offset_x, position[1] + self.offset_y)

    @staticmethod
    def _centered_offset(world_size: float, screen_size: float) -> float:
        return min(0.0, (world_size - screen_size) * 0.5)

    @staticmethod
    def _clamp_offset(offset: float, world_size: float, screen_size: float) -> float:
        max_offset = max(0.0, world_size - screen_size)
        return max(0.0, min(offset, max_offset))

    def _update_axis_with_dead_zone(
        self,
        *,
        focus: float,
        offset: float,
        screen_size: float,
        world_size: float,
        dead_zone_ratio: float,
    ) -> float:
        dead_zone_size = max(1.0, min(screen_size, screen_size * dead_zone_ratio))
        dead_zone_margin = (screen_size - dead_zone_size) * 0.5
        dead_zone_min = offset + dead_zone_margin
        dead_zone_max = dead_zone_min + dead_zone_size

        next_offset = offset
        if focus < dead_zone_min:
            next_offset = focus - dead_zone_margin
        elif focus > dead_zone_max:
            next_offset = focus - dead_zone_margin - dead_zone_size

        return self._clamp_offset(next_offset, world_size, screen_size)

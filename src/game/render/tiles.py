from __future__ import annotations

import math
from dataclasses import dataclass

import pygame

from game.render.camera import Camera
from game.render.fixed_map import load_active_map
from game.render.map_loader import CoordGrid, GridCoord, MapDefinition


@dataclass(frozen=True, slots=True)
class LayerRenderCache:
    name: str
    coord_grid: CoordGrid
    tiles_by_coord: dict[GridCoord, pygame.Surface]


class AshlandGroundLayer:
    """Renders preloaded external map layers in deterministic order."""

    def __init__(self, map_definition: MapDefinition | None = None) -> None:
        self.fixed_map = map_definition or load_active_map()
        self.render_tile_size = self.fixed_map.tile_size
        self._layer_caches: tuple[LayerRenderCache, ...] = tuple(
            LayerRenderCache(
                name=layer.name,
                coord_grid=layer.coord_grid,
                tiles_by_coord=layer.sliced_tiles,
            )
            for layer in self.fixed_map.layers
        )

    @property
    def is_available(self) -> bool:
        return bool(self._layer_caches)

    def draw(
        self,
        surface: pygame.Surface,
        camera: Camera,
        world_width: float,
        world_height: float,
    ) -> bool:
        del world_width, world_height  # Loaded map dimensions are authoritative for rendering.
        if not self._layer_caches:
            return False

        tile_size = self.render_tile_size
        view_left = camera.offset_x
        view_top = camera.offset_y
        view_right = camera.offset_x + surface.get_width()
        view_bottom = camera.offset_y + surface.get_height()

        start_col = max(0, math.floor(view_left / tile_size))
        end_col = min(self.fixed_map.cols - 1, math.floor(view_right / tile_size) + 1)
        start_row = max(0, math.floor(view_top / tile_size))
        end_row = min(self.fixed_map.rows - 1, math.floor(view_bottom / tile_size) + 1)

        if start_col > end_col or start_row > end_row:
            return False

        for row in range(start_row, end_row + 1):
            for col in range(start_col, end_col + 1):
                screen_x = round(col * tile_size - camera.offset_x)
                screen_y = round(row * tile_size - camera.offset_y)

                for layer in self._layer_caches:
                    coord = layer.coord_grid[row][col]
                    if coord is None:
                        continue
                    tile_surface = layer.tiles_by_coord.get(coord)
                    if tile_surface is not None:
                        surface.blit(tile_surface, (screen_x, screen_y))

        return True

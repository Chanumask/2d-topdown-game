from pathlib import Path

from game.render.map_loader import (
    DEFAULT_MAPS_ROOT,
    DEFAULT_RENDER_TILE_SIZE,
    MapDefinition,
    load_map,
)

PROJECT_ROOT = Path(__file__).resolve().parents[3]
SOURCE_TILE_SIZE = 16
DEFAULT_MAP_ID = "ashland_map"
DEFAULT_MAPS_FOLDER = DEFAULT_MAPS_ROOT
DEFAULT_LAYER_RENDER_SIZE = DEFAULT_RENDER_TILE_SIZE


def load_active_map() -> MapDefinition:
    return load_map(
        DEFAULT_MAP_ID,
        maps_root=DEFAULT_MAPS_FOLDER,
        render_tile_size=DEFAULT_LAYER_RENDER_SIZE,
        project_root=PROJECT_ROOT,
    )


__all__ = [
    "DEFAULT_LAYER_RENDER_SIZE",
    "DEFAULT_MAPS_FOLDER",
    "DEFAULT_MAP_ID",
    "MapDefinition",
    "SOURCE_TILE_SIZE",
    "load_active_map",
]

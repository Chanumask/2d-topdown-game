from __future__ import annotations

from dataclasses import dataclass

SOURCE_TILE_SIZE = 16
RENDER_TILE_SIZE = 32
UNIT_MAP_COLS = 50
UNIT_MAP_ROWS = 38
TilesetCoord = tuple[int, int]


@dataclass(frozen=True, slots=True)
class StructurePlacement:
    structure_id: str
    anchor_col: int
    anchor_row: int


@dataclass(frozen=True, slots=True)
class TilePlacement:
    tile_id: str
    col: int
    row: int


@dataclass(frozen=True, slots=True)
class FixedTileMap:
    map_id: str
    tile_size: int
    cols: int
    rows: int
    base_layer: tuple[tuple[str, ...], ...]
    feature_structure_placements: tuple[StructurePlacement, ...]
    feature_standalone_placements: tuple[TilePlacement, ...]
    detail_structure_placements: tuple[StructurePlacement, ...]
    detail_standalone_placements: tuple[TilePlacement, ...]


@dataclass(frozen=True, slots=True)
class CoordPatch:
    patch_id: str
    width: int
    height: int
    coords: tuple[tuple[TilesetCoord, ...], ...]

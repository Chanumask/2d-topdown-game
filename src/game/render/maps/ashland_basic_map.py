from __future__ import annotations

from game.render.maps.a5_patch_helpers import (
    coord_grid_to_tile_id_grid,
    load_a5_tile_lookup,
    validate_coord_grid,
)
from game.render.maps.data.ashland_basic_unit_coords import ASHLAND_BASIC_UNIT_COORD_GRID
from game.render.maps.layout_helpers import (
    build_coord_patch_from_rect,
    repeat_coord_grid,
    repeat_structure_placements,
    repeat_tile_placements,
    stamp_coord_patch,
    stamp_coord_patch_along_internal_vertical_seams,
)
from game.render.maps.types import (
    RENDER_TILE_SIZE,
    UNIT_MAP_COLS,
    UNIT_MAP_ROWS,
    FixedTileMap,
    StructurePlacement,
    TilePlacement,
    TilesetCoord,
)

BASIC_MAP_UNIT_COLS = UNIT_MAP_COLS
BASIC_MAP_UNIT_ROWS = UNIT_MAP_ROWS
BASIC_MAP_REPEAT_COLS = 3
BASIC_MAP_REPEAT_ROWS = 3

BASIC_MAP_CENTER_PATCH_RECT = (0, 6, 5, 11)
BASIC_MAP_INTERNAL_SEAM_PATCH_RECT = (10, 7, 15, 10)

BASIC_MAP_FEATURE_STRUCTURES = (
    StructurePlacement(structure_id="a1_pit_blue_light_3x3", anchor_col=12, anchor_row=11),
    StructurePlacement(structure_id="a1_pit_blue_mid_4x4", anchor_col=34, anchor_row=24),
)

BASIC_MAP_DETAIL_STRUCTURES = (
    StructurePlacement(structure_id="b_wall_chunk_ash", anchor_col=21, anchor_row=6),
    StructurePlacement(structure_id="b_dead_tree_cluster", anchor_col=7, anchor_row=24),
    StructurePlacement(structure_id="b_sign_obelisk_a", anchor_col=25, anchor_row=15),
    StructurePlacement(structure_id="b_bones_shrine", anchor_col=39, anchor_row=10),
    StructurePlacement(structure_id="b_rock_ring", anchor_col=30, anchor_row=28),
)

BASIC_MAP_DETAIL_STANDALONE = (
    TilePlacement(tile_id="ash_b_r02_c00", col=6, row=8),
    TilePlacement(tile_id="ash_b_r02_c02", col=9, row=12),
    TilePlacement(tile_id="ash_b_r03_c01", col=18, row=19),
    TilePlacement(tile_id="ash_b_r04_c05", col=27, row=8),
    TilePlacement(tile_id="ash_b_r07_c09", col=36, row=19),
    TilePlacement(tile_id="ash_b_r11_c10", col=42, row=27),
)


def _build_world_coord_grid(
    *,
    unit_coord_grid: tuple[tuple[TilesetCoord, ...], ...],
) -> tuple[tuple[TilesetCoord, ...], ...]:
    repeated = repeat_coord_grid(
        unit_coord_grid,
        repeat_cols=BASIC_MAP_REPEAT_COLS,
        repeat_rows=BASIC_MAP_REPEAT_ROWS,
    )
    layer = [list(row) for row in repeated]

    center_patch = build_coord_patch_from_rect(
        "center_patch",
        col_start=BASIC_MAP_CENTER_PATCH_RECT[0],
        row_start=BASIC_MAP_CENTER_PATCH_RECT[1],
        col_end=BASIC_MAP_CENTER_PATCH_RECT[2],
        row_end=BASIC_MAP_CENTER_PATCH_RECT[3],
    )
    seam_patch = build_coord_patch_from_rect(
        "internal_seam_patch",
        col_start=BASIC_MAP_INTERNAL_SEAM_PATCH_RECT[0],
        row_start=BASIC_MAP_INTERNAL_SEAM_PATCH_RECT[1],
        col_end=BASIC_MAP_INTERNAL_SEAM_PATCH_RECT[2],
        row_end=BASIC_MAP_INTERNAL_SEAM_PATCH_RECT[3],
    )

    cols = len(layer[0])
    rows = len(layer)
    center_col = (cols - center_patch.width) // 2
    center_row = (rows - center_patch.height) // 2
    stamp_coord_patch(layer, center_patch, center_col, center_row)

    # Continuous seam path between repeated columns, spanning full map height.
    stamp_coord_patch_along_internal_vertical_seams(
        layer=layer,
        seam_patch=seam_patch,
        unit_cols=BASIC_MAP_UNIT_COLS,
        repeat_cols=BASIC_MAP_REPEAT_COLS,
    )

    return tuple(tuple(row) for row in layer)


BASIC_MAP_WORLD_COLS = BASIC_MAP_UNIT_COLS * BASIC_MAP_REPEAT_COLS
BASIC_MAP_WORLD_ROWS = BASIC_MAP_UNIT_ROWS * BASIC_MAP_REPEAT_ROWS

BASIC_MAP_TILE_LOOKUP = load_a5_tile_lookup()

BASIC_MAP_UNIT_COORD_GRID = ASHLAND_BASIC_UNIT_COORD_GRID

validate_coord_grid(
    BASIC_MAP_UNIT_COORD_GRID,
    expected_cols=BASIC_MAP_UNIT_COLS,
    expected_rows=BASIC_MAP_UNIT_ROWS,
    tile_lookup=BASIC_MAP_TILE_LOOKUP,
)

BASIC_MAP_WORLD_COORD_GRID = _build_world_coord_grid(
    unit_coord_grid=BASIC_MAP_UNIT_COORD_GRID,
)
BASIC_MAP_WORLD_TILE_ID_GRID = coord_grid_to_tile_id_grid(
    BASIC_MAP_WORLD_COORD_GRID,
    tile_lookup=BASIC_MAP_TILE_LOOKUP,
)

BASIC_MAP_FEATURE_STRUCTURE_PLACEMENTS = repeat_structure_placements(
    BASIC_MAP_FEATURE_STRUCTURES,
    unit_cols=BASIC_MAP_UNIT_COLS,
    unit_rows=BASIC_MAP_UNIT_ROWS,
    repeat_cols=BASIC_MAP_REPEAT_COLS,
    repeat_rows=BASIC_MAP_REPEAT_ROWS,
)

BASIC_MAP_DETAIL_STRUCTURE_PLACEMENTS = repeat_structure_placements(
    BASIC_MAP_DETAIL_STRUCTURES,
    unit_cols=BASIC_MAP_UNIT_COLS,
    unit_rows=BASIC_MAP_UNIT_ROWS,
    repeat_cols=BASIC_MAP_REPEAT_COLS,
    repeat_rows=BASIC_MAP_REPEAT_ROWS,
)

BASIC_MAP_DETAIL_STANDALONE_PLACEMENTS = repeat_tile_placements(
    BASIC_MAP_DETAIL_STANDALONE,
    unit_cols=BASIC_MAP_UNIT_COLS,
    unit_rows=BASIC_MAP_UNIT_ROWS,
    repeat_cols=BASIC_MAP_REPEAT_COLS,
    repeat_rows=BASIC_MAP_REPEAT_ROWS,
)

ASHLAND_BASIC_MAP = FixedTileMap(
    map_id="ashland_basic_map",
    tile_size=RENDER_TILE_SIZE,
    cols=BASIC_MAP_WORLD_COLS,
    rows=BASIC_MAP_WORLD_ROWS,
    base_layer=BASIC_MAP_WORLD_TILE_ID_GRID,
    feature_structure_placements=BASIC_MAP_FEATURE_STRUCTURE_PLACEMENTS,
    feature_standalone_placements=(),
    detail_structure_placements=BASIC_MAP_DETAIL_STRUCTURE_PLACEMENTS,
    detail_standalone_placements=BASIC_MAP_DETAIL_STANDALONE_PLACEMENTS,
)

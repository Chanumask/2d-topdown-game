from __future__ import annotations

from dataclasses import dataclass

SOURCE_TILE_SIZE = 16
RENDER_TILE_SIZE = 32

ASHLAND_FIRST_MAP_COLS = 50
ASHLAND_FIRST_MAP_ROWS = 38
MAP_REPEAT_COLS = 3
MAP_REPEAT_ROWS = 3

# First fixed Ashland map:
# - left region: ground_square family
# - center band: transition_edge family
# - right region: ground_dark family
LEFT_BACKGROUND_TILE_ID = "ash_a5_r02_c05"
RIGHT_BACKGROUND_TILE_ID = "ash_a5_r04_c08"
TRANSITION_BAND_TILE_IDS = (
    "ash_a5_r14_c08",
    "ash_a5_r14_c09",
    "ash_a5_r14_c10",
    "ash_a5_r14_c11",
)
LEFT_REGION_COLS = 23
TRANSITION_BAND_COLS = len(TRANSITION_BAND_TILE_IDS)


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


def _build_first_ashland_base_layer() -> tuple[tuple[str, ...], ...]:
    right_cols = ASHLAND_FIRST_MAP_COLS - LEFT_REGION_COLS - TRANSITION_BAND_COLS
    if right_cols <= 0:
        raise ValueError("Invalid fixed map column split for first Ashland map.")

    row = (
        (LEFT_BACKGROUND_TILE_ID,) * LEFT_REGION_COLS
        + TRANSITION_BAND_TILE_IDS
        + (RIGHT_BACKGROUND_TILE_ID,) * right_cols
    )
    return tuple(row for _ in range(ASHLAND_FIRST_MAP_ROWS))


def _repeat_base_layer(
    unit_layer: tuple[tuple[str, ...], ...],
    *,
    repeat_cols: int,
    repeat_rows: int,
) -> tuple[tuple[str, ...], ...]:
    repeated_rows: list[tuple[str, ...]] = []
    for _ in range(repeat_rows):
        for source_row in unit_layer:
            repeated_rows.append(
                tuple(tile_id for _ in range(repeat_cols) for tile_id in source_row)
            )
    return tuple(repeated_rows)


def _repeat_structure_placements(
    unit_placements: tuple[StructurePlacement, ...],
    *,
    unit_cols: int,
    unit_rows: int,
    repeat_cols: int,
    repeat_rows: int,
) -> tuple[StructurePlacement, ...]:
    placements: list[StructurePlacement] = []
    for tile_row in range(repeat_rows):
        for tile_col in range(repeat_cols):
            col_offset = tile_col * unit_cols
            row_offset = tile_row * unit_rows
            for placement in unit_placements:
                placements.append(
                    StructurePlacement(
                        structure_id=placement.structure_id,
                        anchor_col=placement.anchor_col + col_offset,
                        anchor_row=placement.anchor_row + row_offset,
                    )
                )
    return tuple(placements)


def _repeat_tile_placements(
    unit_placements: tuple[TilePlacement, ...],
    *,
    unit_cols: int,
    unit_rows: int,
    repeat_cols: int,
    repeat_rows: int,
) -> tuple[TilePlacement, ...]:
    placements: list[TilePlacement] = []
    for tile_row in range(repeat_rows):
        for tile_col in range(repeat_cols):
            col_offset = tile_col * unit_cols
            row_offset = tile_row * unit_rows
            for placement in unit_placements:
                placements.append(
                    TilePlacement(
                        tile_id=placement.tile_id,
                        col=placement.col + col_offset,
                        row=placement.row + row_offset,
                    )
                )
    return tuple(placements)


# A1 fixed feature placements (holes/pits). These are assembled from manifest templates,
# so each placement always resolves to a full multi-tile feature footprint.
ASHLAND_FIRST_MAP_FEATURE_STRUCTURES = (
    StructurePlacement(structure_id="a1_pit_blue_light_3x3", anchor_col=12, anchor_row=11),
    StructurePlacement(structure_id="a1_pit_blue_mid_4x4", anchor_col=34, anchor_row=24),
)

# B detail/prop placements. Multi-tile structures stay intact through template assembly.
ASHLAND_FIRST_MAP_DETAIL_STRUCTURES = (
    StructurePlacement(structure_id="b_wall_chunk_ash", anchor_col=21, anchor_row=6),
    StructurePlacement(structure_id="b_dead_tree_cluster", anchor_col=7, anchor_row=24),
    StructurePlacement(structure_id="b_sign_obelisk_a", anchor_col=25, anchor_row=15),
    StructurePlacement(structure_id="b_bones_shrine", anchor_col=39, anchor_row=10),
    StructurePlacement(structure_id="b_rock_ring", anchor_col=30, anchor_row=28),
)

# Sparse standalone B details. These tile ids are validated against manifest standalone flags.
ASHLAND_FIRST_MAP_DETAIL_STANDALONE = (
    TilePlacement(tile_id="ash_b_r02_c00", col=6, row=8),
    TilePlacement(tile_id="ash_b_r02_c02", col=9, row=12),
    TilePlacement(tile_id="ash_b_r03_c01", col=18, row=19),
    TilePlacement(tile_id="ash_b_r04_c05", col=27, row=8),
    TilePlacement(tile_id="ash_b_r07_c09", col=36, row=19),
    TilePlacement(tile_id="ash_b_r11_c10", col=42, row=27),
)


_ASHLAND_UNIT_BASE_LAYER = _build_first_ashland_base_layer()
ASHLAND_FIRST_MAP = FixedTileMap(
    map_id="ashland_first_fixed_map_repeated_9x9",
    tile_size=RENDER_TILE_SIZE,
    cols=ASHLAND_FIRST_MAP_COLS * MAP_REPEAT_COLS,
    rows=ASHLAND_FIRST_MAP_ROWS * MAP_REPEAT_ROWS,
    base_layer=_repeat_base_layer(
        _ASHLAND_UNIT_BASE_LAYER,
        repeat_cols=MAP_REPEAT_COLS,
        repeat_rows=MAP_REPEAT_ROWS,
    ),
    feature_structure_placements=_repeat_structure_placements(
        ASHLAND_FIRST_MAP_FEATURE_STRUCTURES,
        unit_cols=ASHLAND_FIRST_MAP_COLS,
        unit_rows=ASHLAND_FIRST_MAP_ROWS,
        repeat_cols=MAP_REPEAT_COLS,
        repeat_rows=MAP_REPEAT_ROWS,
    ),
    feature_standalone_placements=(),
    detail_structure_placements=_repeat_structure_placements(
        ASHLAND_FIRST_MAP_DETAIL_STRUCTURES,
        unit_cols=ASHLAND_FIRST_MAP_COLS,
        unit_rows=ASHLAND_FIRST_MAP_ROWS,
        repeat_cols=MAP_REPEAT_COLS,
        repeat_rows=MAP_REPEAT_ROWS,
    ),
    detail_standalone_placements=_repeat_tile_placements(
        ASHLAND_FIRST_MAP_DETAIL_STANDALONE,
        unit_cols=ASHLAND_FIRST_MAP_COLS,
        unit_rows=ASHLAND_FIRST_MAP_ROWS,
        repeat_cols=MAP_REPEAT_COLS,
        repeat_rows=MAP_REPEAT_ROWS,
    ),
)

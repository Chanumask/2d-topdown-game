from __future__ import annotations

from dataclasses import dataclass

SOURCE_TILE_SIZE = 16
RENDER_TILE_SIZE = 32

ASHLAND_FIRST_MAP_COLS = 50
ASHLAND_FIRST_MAP_ROWS = 38

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
class FixedTileMap:
    map_id: str
    tile_size: int
    cols: int
    rows: int
    base_layer: tuple[tuple[str, ...], ...]


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


ASHLAND_FIRST_MAP = FixedTileMap(
    map_id="ashland_first_fixed_map",
    tile_size=RENDER_TILE_SIZE,
    cols=ASHLAND_FIRST_MAP_COLS,
    rows=ASHLAND_FIRST_MAP_ROWS,
    base_layer=_build_first_ashland_base_layer(),
)

from __future__ import annotations

import importlib.util
from pathlib import Path

from game.render.maps.types import TilesetCoord

DEFAULT_A5_MANIFEST_PATH = (
    Path(__file__).resolve().parents[4]
    / "assets"
    / "tilesets"
    / "ashland"
    / "ashland_a5_manifest.py"
)


def load_a5_tile_lookup(
    manifest_path: Path = DEFAULT_A5_MANIFEST_PATH,
) -> dict[tuple[int, int], str]:
    if manifest_path.exists():
        try:
            spec = importlib.util.spec_from_file_location(
                "ashland_a5_manifest_fixed_map",
                manifest_path,
            )
            if spec is not None and spec.loader is not None:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                manifest = getattr(module, "ASHLAND_A5_MANIFEST", None)
                if isinstance(manifest, dict):
                    lookup: dict[tuple[int, int], str] = {}
                    for payload in manifest.values():
                        if not isinstance(payload, dict):
                            continue
                        coord = payload.get("coord")
                        tile_id = str(payload.get("id", "")).strip()
                        if isinstance(coord, list) and len(coord) == 2 and tile_id:
                            lookup[(int(coord[0]), int(coord[1]))] = tile_id
                    if lookup:
                        return lookup
        except Exception as error:
            print(f"[FixedMap] Failed to load A5 manifest lookup: {error}")

    print("[FixedMap] Falling back to A5 tile-id naming convention lookup.")
    return {(col, row): f"ash_a5_r{row:02d}_c{col:02d}" for row in range(30) for col in range(16)}


def validate_coord_grid(
    grid: tuple[tuple[TilesetCoord, ...], ...],
    *,
    expected_cols: int,
    expected_rows: int,
    tile_lookup: dict[tuple[int, int], str],
) -> None:
    if len(grid) != expected_rows:
        raise ValueError(
            f"Invalid coordinate-grid height. Expected {expected_rows}, got {len(grid)}."
        )

    for row_index, row in enumerate(grid):
        if len(row) != expected_cols:
            raise ValueError(
                "Invalid coordinate-grid width in row "
                f"{row_index}. Expected {expected_cols}, got {len(row)}."
            )
        for col_index, coord in enumerate(row):
            if not isinstance(coord, tuple) or len(coord) != 2:
                raise ValueError(
                    f"Invalid coord at ({col_index},{row_index}): expected (x,y) tuple."
                )
            col, row_value = int(coord[0]), int(coord[1])
            if (col, row_value) not in tile_lookup:
                raise ValueError(
                    f"Coordinate ({col},{row_value}) at ({col_index},{row_index}) is not present "
                    "in A5 manifest lookup."
                )


def coord_grid_to_tile_id_grid(
    grid: tuple[tuple[TilesetCoord, ...], ...],
    *,
    tile_lookup: dict[tuple[int, int], str],
) -> tuple[tuple[str, ...], ...]:
    resolved_rows: list[tuple[str, ...]] = []
    for row in grid:
        resolved_row: list[str] = []
        for coord in row:
            tile_id = tile_lookup.get((int(coord[0]), int(coord[1])))
            if tile_id is None:
                raise ValueError(f"Coordinate {coord} is not present in A5 manifest lookup.")
            resolved_row.append(tile_id)
        resolved_rows.append(tuple(resolved_row))
    return tuple(resolved_rows)

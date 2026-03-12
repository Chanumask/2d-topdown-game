from __future__ import annotations

import ast
import re
from dataclasses import dataclass
from pathlib import Path

import pygame

from game.render.spritesheet import load_image, pixelart_upscale_surface

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_MAPS_ROOT = PROJECT_ROOT / "assets" / "maps"
DEFAULT_RENDER_TILE_SIZE = 32

ALLOWED_VARS = {
    "LAYER_NAME",
    "LAYER_ORDER",
    "TILESET_PATH",
    "TILE_SIZE",
    "MAP_WIDTH",
    "MAP_HEIGHT",
    "UNIT_COORD_GRID",
    "BLOCKING_GRID",
    "MAP_ID",
    "TILESET_NAME",
}

REQUIRED_VARS = {
    "LAYER_NAME",
    "LAYER_ORDER",
    "TILESET_PATH",
    "TILE_SIZE",
    "MAP_WIDTH",
    "MAP_HEIGHT",
    "UNIT_COORD_GRID",
}

GridCoord = tuple[int, int]
TileCoord = GridCoord | None
CoordGrid = tuple[tuple[TileCoord, ...], ...]
BlockingGrid = tuple[tuple[bool, ...], ...]


@dataclass(slots=True)
class MapLayer:
    name: str
    order: int
    tileset_path: Path
    tile_size: int
    render_tile_size: int
    width: int
    height: int
    coord_grid: CoordGrid
    blocking_grid: BlockingGrid
    tileset_surface: pygame.Surface
    sliced_tiles: dict[GridCoord, pygame.Surface]
    map_id: str | None = None
    tileset_name: str | None = None
    source_file: Path | None = None


@dataclass(slots=True)
class MapDefinition:
    map_id: str
    width: int
    height: int
    layers: list[MapLayer]
    merged_blocking_grid: BlockingGrid

    @property
    def cols(self) -> int:
        return self.width

    @property
    def rows(self) -> int:
        return self.height

    @property
    def tile_size(self) -> int:
        return self.layers[0].render_tile_size if self.layers else DEFAULT_RENDER_TILE_SIZE


def _parse_layer_vars(layer_file: Path) -> dict[str, object]:
    source = layer_file.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(layer_file))

    parsed: dict[str, object] = {}

    for node in tree.body:
        if isinstance(node, ast.Assign):
            targets = [target for target in node.targets if isinstance(target, ast.Name)]
            if not targets:
                continue
            for target in targets:
                key = target.id
                if key not in ALLOWED_VARS:
                    continue
                try:
                    parsed[key] = ast.literal_eval(node.value)
                except Exception as error:
                    raise ValueError(
                        f"{layer_file.name}: failed to parse literal for '{key}': {error}"
                    ) from error
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.value:
            key = node.target.id
            if key not in ALLOWED_VARS:
                continue
            try:
                parsed[key] = ast.literal_eval(node.value)
            except Exception as error:
                raise ValueError(
                    f"{layer_file.name}: failed to parse literal for '{key}': {error}"
                ) from error

    return parsed


def _validate_grid(
    layer_file: Path,
    *,
    width: int,
    height: int,
    raw_grid: object,
) -> CoordGrid:
    if not isinstance(raw_grid, (tuple, list)):
        raise ValueError(f"{layer_file.name}: UNIT_COORD_GRID must be tuple/list rows.")
    if len(raw_grid) != height:
        raise ValueError(
            f"{layer_file.name}: UNIT_COORD_GRID row count {len(raw_grid)} != MAP_HEIGHT {height}."
        )

    rows: list[tuple[TileCoord, ...]] = []
    for row_index, raw_row in enumerate(raw_grid):
        if not isinstance(raw_row, (tuple, list)):
            raise ValueError(f"{layer_file.name}: row {row_index} is not tuple/list.")
        if len(raw_row) != width:
            raise ValueError(
                f"{layer_file.name}: row {row_index} width {len(raw_row)} != MAP_WIDTH {width}."
            )

        row: list[TileCoord] = []
        for col_index, raw_cell in enumerate(raw_row):
            if raw_cell is None:
                row.append(None)
                continue
            if not isinstance(raw_cell, (tuple, list)) or len(raw_cell) != 2:
                raise ValueError(
                    f"{layer_file.name}: cell ({col_index},{row_index}) must be (x, y) or None."
                )
            coord_x, coord_y = raw_cell
            if not isinstance(coord_x, int) or not isinstance(coord_y, int):
                raise ValueError(
                    f"{layer_file.name}: cell ({col_index},{row_index}) must contain ints."
                )
            if coord_x < 0 or coord_y < 0:
                # Treat negative tuples as explicit empty/sentinel cells for exporter compatibility.
                row.append(None)
                continue
            row.append((coord_x, coord_y))
        rows.append(tuple(row))

    return tuple(rows)


def _default_blocking_grid(width: int, height: int) -> BlockingGrid:
    return tuple(tuple(False for _ in range(width)) for _ in range(height))


def _validate_blocking_grid(
    layer_file: Path,
    *,
    width: int,
    height: int,
    raw_grid: object | None,
) -> BlockingGrid:
    if raw_grid is None:
        return _default_blocking_grid(width, height)

    if not isinstance(raw_grid, (tuple, list)):
        raise ValueError(f"{layer_file.name}: BLOCKING_GRID must be tuple/list rows.")
    if len(raw_grid) != height:
        raise ValueError(
            f"{layer_file.name}: BLOCKING_GRID row count {len(raw_grid)} != MAP_HEIGHT {height}."
        )

    rows: list[tuple[bool, ...]] = []
    for row_index, raw_row in enumerate(raw_grid):
        if not isinstance(raw_row, (tuple, list)):
            raise ValueError(f"{layer_file.name}: BLOCKING_GRID row {row_index} is not tuple/list.")
        if len(raw_row) != width:
            raise ValueError(
                f"{layer_file.name}: BLOCKING_GRID row {row_index} width {len(raw_row)} "
                f"!= MAP_WIDTH {width}."
            )

        row: list[bool] = []
        for col_index, raw_cell in enumerate(raw_row):
            if not isinstance(raw_cell, bool):
                raise ValueError(
                    f"{layer_file.name}: BLOCKING_GRID cell ({col_index},{row_index}) must be bool."
                )
            row.append(raw_cell)
        rows.append(tuple(row))
    return tuple(rows)


def _resolve_tileset_path(layer_file: Path, tileset_path_value: str, *, project_root: Path) -> Path:
    candidate = Path(tileset_path_value)
    candidates: list[Path] = []
    if candidate.is_absolute():
        candidates.append(candidate)
    else:
        candidates.extend(
            [
                (project_root / candidate).resolve(),
                (project_root / "assets" / candidate).resolve(),
                (layer_file.parent / candidate).resolve(),
                (layer_file.parent / "assets" / candidate).resolve(),
            ]
        )

    for resolved in candidates:
        if resolved.exists():
            return resolved

    if not candidate.is_absolute() and candidate.parts and candidate.parts[0] == "tilesets":
        tilesets_root = (project_root / "assets" / "tilesets").resolve()
        if tilesets_root.exists():
            by_name_matches = sorted(tilesets_root.rglob(candidate.name))
            if len(by_name_matches) == 1:
                return by_name_matches[0]
            if len(by_name_matches) > 1:
                matches = ", ".join(str(path) for path in by_name_matches)
                raise ValueError(
                    f"{layer_file.name}: TILESET_PATH '{tileset_path_value}' is ambiguous. "
                    f"Found multiple matches for '{candidate.name}': {matches}"
                )

    attempted = ", ".join(str(path) for path in candidates) if candidates else "none"
    raise ValueError(
        f"{layer_file.name}: TILESET_PATH '{tileset_path_value}' does not exist "
        f"(attempted: {attempted})."
    )


def _slice_tileset(
    layer_file: Path,
    *,
    tileset_surface: pygame.Surface,
    tile_size: int,
    render_tile_size: int,
) -> dict[GridCoord, pygame.Surface]:
    sheet_width, sheet_height = tileset_surface.get_size()
    max_x = sheet_width // tile_size
    max_y = sheet_height // tile_size
    if max_x <= 0 or max_y <= 0:
        raise ValueError(
            f"{layer_file.name}: tileset too small for TILE_SIZE={tile_size} "
            f"({sheet_width}x{sheet_height})."
        )

    sliced: dict[GridCoord, pygame.Surface] = {}
    for tile_y in range(max_y):
        for tile_x in range(max_x):
            rect = pygame.Rect(tile_x * tile_size, tile_y * tile_size, tile_size, tile_size)
            source_tile = tileset_surface.subsurface(rect).copy()
            if render_tile_size == tile_size:
                render_tile = source_tile
            elif render_tile_size % tile_size == 0:
                scale_multiple = render_tile_size // tile_size
                render_tile = pixelart_upscale_surface(source_tile, scale_multiple)
            else:
                render_tile = pygame.transform.scale(
                    source_tile,
                    (render_tile_size, render_tile_size),
                )
            sliced[(tile_x, tile_y)] = render_tile
    return sliced


def _build_layer(
    layer_file: Path,
    *,
    render_tile_size: int,
    project_root: Path,
) -> MapLayer:
    parsed = _parse_layer_vars(layer_file)
    missing = sorted(REQUIRED_VARS - parsed.keys())
    if missing:
        raise ValueError(f"{layer_file.name}: missing required variable(s): {', '.join(missing)}.")

    layer_name = parsed["LAYER_NAME"]
    layer_order = parsed["LAYER_ORDER"]
    tileset_path_value = parsed["TILESET_PATH"]
    tile_size = parsed["TILE_SIZE"]
    width = parsed["MAP_WIDTH"]
    height = parsed["MAP_HEIGHT"]

    if not isinstance(layer_name, str) or not layer_name.strip():
        raise ValueError(f"{layer_file.name}: LAYER_NAME must be a non-empty string.")
    if not isinstance(layer_order, int):
        raise ValueError(f"{layer_file.name}: LAYER_ORDER must be an int.")
    if not isinstance(tileset_path_value, str) or not tileset_path_value.strip():
        raise ValueError(f"{layer_file.name}: TILESET_PATH must be a non-empty string.")
    if not isinstance(tile_size, int) or tile_size <= 0:
        raise ValueError(f"{layer_file.name}: TILE_SIZE must be > 0.")
    if not isinstance(width, int) or width <= 0:
        raise ValueError(f"{layer_file.name}: MAP_WIDTH must be > 0.")
    if not isinstance(height, int) or height <= 0:
        raise ValueError(f"{layer_file.name}: MAP_HEIGHT must be > 0.")

    coord_grid = _validate_grid(
        layer_file,
        width=width,
        height=height,
        raw_grid=parsed["UNIT_COORD_GRID"],
    )
    blocking_grid = _validate_blocking_grid(
        layer_file,
        width=width,
        height=height,
        raw_grid=parsed.get("BLOCKING_GRID"),
    )
    tileset_path = _resolve_tileset_path(
        layer_file,
        tileset_path_value=tileset_path_value,
        project_root=project_root,
    )
    tileset_surface = load_image(tileset_path)
    if tileset_surface is None:
        raise ValueError(f"{layer_file.name}: failed to load tileset image '{tileset_path}'.")

    sliced_tiles = _slice_tileset(
        layer_file,
        tileset_surface=tileset_surface,
        tile_size=tile_size,
        render_tile_size=render_tile_size,
    )

    for row_index, row in enumerate(coord_grid):
        for col_index, coord in enumerate(row):
            if coord is None:
                continue
            if coord not in sliced_tiles:
                raise ValueError(
                    f"{layer_file.name}: coordinate {coord} at ({col_index},{row_index}) "
                    "is outside tileset bounds."
                )

    optional_map_id = parsed.get("MAP_ID")
    optional_tileset_name = parsed.get("TILESET_NAME")

    return MapLayer(
        name=layer_name.strip(),
        order=layer_order,
        tileset_path=tileset_path,
        tile_size=tile_size,
        render_tile_size=render_tile_size,
        width=width,
        height=height,
        coord_grid=coord_grid,
        blocking_grid=blocking_grid,
        tileset_surface=tileset_surface,
        sliced_tiles=sliced_tiles,
        map_id=optional_map_id if isinstance(optional_map_id, str) else None,
        tileset_name=optional_tileset_name if isinstance(optional_tileset_name, str) else None,
        source_file=layer_file,
    )


def _merge_blocking_grids(layers: list[MapLayer], *, width: int, height: int) -> BlockingGrid:
    if not layers:
        return _default_blocking_grid(width, height)

    merged_rows: list[tuple[bool, ...]] = []
    for row_index in range(height):
        merged_row: list[bool] = []
        for col_index in range(width):
            is_blocked = any(layer.blocking_grid[row_index][col_index] for layer in layers)
            merged_row.append(is_blocked)
        merged_rows.append(tuple(merged_row))

    return tuple(merged_rows)


def _parse_layer_index_from_name(layer_file: Path) -> int | None:
    match = re.search(r"layer[_-]?(\d+)$", layer_file.stem, flags=re.IGNORECASE)
    if match is None:
        return None
    return int(match.group(1))


def _normalize_layer_orders(layers: list[MapLayer], *, map_id: str) -> None:
    orders = [layer.order for layer in layers]
    if len(set(orders)) == len(orders):
        return

    indexed_layers: list[tuple[MapLayer, int]] = []
    for layer in layers:
        if layer.source_file is None:
            indexed_layers = []
            break
        parsed_index = _parse_layer_index_from_name(layer.source_file)
        if parsed_index is None:
            indexed_layers = []
            break
        indexed_layers.append((layer, parsed_index))

    if indexed_layers and len({index for _, index in indexed_layers}) == len(indexed_layers):
        for layer, parsed_index in indexed_layers:
            layer.order = parsed_index
        return

    if len(set(orders)) == 1:
        sorted_layers = sorted(
            layers,
            key=lambda layer: (
                layer.source_file.name if layer.source_file is not None else layer.name
            ),
        )
        for index, layer in enumerate(sorted_layers):
            layer.order = index
        return

    raise ValueError(f"Map '{map_id}' has duplicate LAYER_ORDER values: {orders}.")


def load_map(
    map_id: str,
    *,
    maps_root: Path = DEFAULT_MAPS_ROOT,
    render_tile_size: int = DEFAULT_RENDER_TILE_SIZE,
    project_root: Path = PROJECT_ROOT,
) -> MapDefinition:
    if not map_id.strip():
        raise ValueError("map_id must be a non-empty string.")
    if render_tile_size <= 0:
        raise ValueError("render_tile_size must be > 0.")

    map_folder = (maps_root / map_id).resolve()
    if not map_folder.exists() or not map_folder.is_dir():
        raise ValueError(f"Map folder not found: {map_folder}")

    layer_files = sorted(
        file for file in map_folder.glob("*.py") if file.is_file() and file.name != "__init__.py"
    )
    if not layer_files:
        raise ValueError(f"No layer files found in map folder: {map_folder}")

    layers = [
        _build_layer(
            layer_file,
            render_tile_size=render_tile_size,
            project_root=project_root,
        )
        for layer_file in layer_files
    ]

    first = layers[0]
    for layer in layers[1:]:
        if layer.width != first.width:
            raise ValueError(
                f"{layer.source_file.name}: MAP_WIDTH {layer.width} != {first.width} from "
                f"{first.source_file.name}."
            )
        if layer.height != first.height:
            raise ValueError(
                f"{layer.source_file.name}: MAP_HEIGHT {layer.height} != {first.height} from "
                f"{first.source_file.name}."
            )

    _normalize_layer_orders(layers, map_id=map_id)

    ordered_layers = sorted(layers, key=lambda layer: layer.order)
    merged_blocking_grid = _merge_blocking_grids(
        ordered_layers,
        width=first.width,
        height=first.height,
    )
    return MapDefinition(
        map_id=map_id,
        width=first.width,
        height=first.height,
        layers=ordered_layers,
        merged_blocking_grid=merged_blocking_grid,
    )

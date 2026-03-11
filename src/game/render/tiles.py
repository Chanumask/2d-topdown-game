from __future__ import annotations

import importlib.util
import math
from dataclasses import dataclass
from pathlib import Path

import pygame

from game.render.camera import Camera
from game.render.fixed_map import (
    ASHLAND_FIRST_MAP,
    SOURCE_TILE_SIZE,
    FixedTileMap,
    StructurePlacement,
    TilePlacement,
)
from game.render.spritesheet import load_image, pixelart_upscale_surface

ASHLAND_TILESET_ROOT = Path(__file__).resolve().parents[3] / "assets" / "tilesets" / "ashland"
ASHLAND_A5_PATH = ASHLAND_TILESET_ROOT / "tf_A5_ashlands_2.png"
ASHLAND_A1_PATH = ASHLAND_TILESET_ROOT / "tf_A1_ashlands_2.png"
ASHLAND_B_PATH = ASHLAND_TILESET_ROOT / "tf_B_ashlands_2.png"
ASHLAND_A5_MANIFEST_PATH = ASHLAND_TILESET_ROOT / "ashland_a5_manifest.py"
ASHLAND_A1_MANIFEST_PATH = ASHLAND_TILESET_ROOT / "ashland_a1_manifest.py"
ASHLAND_B_MANIFEST_PATH = ASHLAND_TILESET_ROOT / "ashland_b_manifest.py"

LayerGrid = tuple[tuple[str | None, ...], ...]


@dataclass(frozen=True, slots=True)
class TileManifestEntry:
    tile_id: str
    coord_col: int
    coord_row: int
    group: str
    tags: tuple[str, ...]
    walkable_default: bool


@dataclass(frozen=True, slots=True)
class StructureTemplateCell:
    dx: int
    dy: int
    tile_id: str


@dataclass(frozen=True, slots=True)
class StructureTemplate:
    structure_id: str
    footprint_cols: int
    footprint_rows: int
    cells: tuple[StructureTemplateCell, ...]


def _load_manifest_module(path: Path, module_name: str) -> object | None:
    if not path.exists():
        print(f"[Tiles] Manifest missing: {path.name}")
        return None

    try:
        spec = importlib.util.spec_from_file_location(module_name, path)
        if spec is None or spec.loader is None:
            print(f"[Tiles] Failed to read manifest spec: {path.name}")
            return None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    except Exception as error:
        print(f"[Tiles] Failed to import {path.name}: {error}")
        return None
    return module


def _parse_manifest_entries(raw_manifest: object) -> dict[str, TileManifestEntry]:
    if not isinstance(raw_manifest, dict):
        return {}

    entries_by_id: dict[str, TileManifestEntry] = {}
    for payload in raw_manifest.values():
        if not isinstance(payload, dict):
            continue
        tile_id = str(payload.get("id", "")).strip()
        coord = payload.get("coord")
        group = str(payload.get("group", "")).strip()
        if not tile_id or not isinstance(coord, list) or len(coord) != 2 or not group:
            continue
        entries_by_id[tile_id] = TileManifestEntry(
            tile_id=tile_id,
            coord_col=int(coord[0]),
            coord_row=int(coord[1]),
            group=group,
            tags=tuple(str(tag) for tag in payload.get("tags", []) if isinstance(tag, str)),
            walkable_default=bool(payload.get("walkable_default", False)),
        )
    return entries_by_id


def _parse_structure_templates(raw_templates: object) -> dict[str, StructureTemplate]:
    if not isinstance(raw_templates, list):
        return {}

    templates: dict[str, StructureTemplate] = {}
    for payload in raw_templates:
        if not isinstance(payload, dict):
            continue
        structure_id = str(payload.get("structure_id", "")).strip()
        footprint = payload.get("footprint")
        cells_payload = payload.get("cells")
        if (
            not structure_id
            or not isinstance(footprint, list)
            or len(footprint) != 2
            or not isinstance(cells_payload, list)
        ):
            continue

        cells: list[StructureTemplateCell] = []
        for cell in cells_payload:
            if not isinstance(cell, dict):
                continue
            tile_id = str(cell.get("tile_id", "")).strip()
            if not tile_id:
                continue
            cells.append(
                StructureTemplateCell(
                    dx=int(cell.get("dx", 0)),
                    dy=int(cell.get("dy", 0)),
                    tile_id=tile_id,
                )
            )

        templates[structure_id] = StructureTemplate(
            structure_id=structure_id,
            footprint_cols=int(footprint[0]),
            footprint_rows=int(footprint[1]),
            cells=tuple(cells),
        )
    return templates


def _load_tile_surfaces(
    *,
    tileset_path: Path,
    entries_by_id: dict[str, TileManifestEntry],
    pixel_scale: int,
    tileset_label: str,
) -> dict[str, pygame.Surface]:
    if not entries_by_id:
        return {}
    if pixel_scale <= 0:
        print(f"[Tiles] Invalid pixel scale for {tileset_label}.")
        return {}

    sheet = load_image(tileset_path)
    if sheet is None:
        print(f"[Tiles] {tileset_label} tileset unavailable; skipping layer.")
        return {}

    sheet_width, sheet_height = sheet.get_size()
    max_col = sheet_width // SOURCE_TILE_SIZE
    max_row = sheet_height // SOURCE_TILE_SIZE

    loaded: dict[str, pygame.Surface] = {}
    for tile_id, entry in entries_by_id.items():
        if (
            entry.coord_col < 0
            or entry.coord_row < 0
            or entry.coord_col >= max_col
            or entry.coord_row >= max_row
        ):
            continue
        rect = pygame.Rect(
            entry.coord_col * SOURCE_TILE_SIZE,
            entry.coord_row * SOURCE_TILE_SIZE,
            SOURCE_TILE_SIZE,
            SOURCE_TILE_SIZE,
        )
        tile_surface = sheet.subsurface(rect).copy()
        loaded[tile_id] = pixelart_upscale_surface(tile_surface, pixel_scale)
    return loaded


def _empty_layer(rows: int, cols: int) -> list[list[str | None]]:
    return [[None for _ in range(cols)] for _ in range(rows)]


def _to_tuple_layer(layer: list[list[str | None]]) -> LayerGrid:
    return tuple(tuple(row) for row in layer)


def _validate_footprint(template: StructureTemplate) -> bool:
    expected_cell_count = template.footprint_cols * template.footprint_rows
    return len(template.cells) == expected_cell_count


def _compose_overlay_layer(
    *,
    fixed_map: FixedTileMap,
    layer_name: str,
    structure_placements: tuple[StructurePlacement, ...],
    standalone_placements: tuple[TilePlacement, ...],
    templates_by_id: dict[str, StructureTemplate],
    selection_flags_by_tile_id: dict[str, dict[str, object]],
    available_tile_ids: set[str],
    exclude_flag_key: str,
) -> LayerGrid:
    layer = _empty_layer(fixed_map.rows, fixed_map.cols)

    for placement in structure_placements:
        template = templates_by_id.get(placement.structure_id)
        if template is None:
            print(
                f"[Tiles] {layer_name}: unknown structure_id "
                f"'{placement.structure_id}', skipping placement."
            )
            continue

        if not _validate_footprint(template):
            print(
                f"[Tiles] {layer_name}: template '{template.structure_id}' has incomplete "
                "cell footprint; skipping to avoid fragments."
            )
            continue

        if (
            placement.anchor_col < 0
            or placement.anchor_row < 0
            or placement.anchor_col + template.footprint_cols > fixed_map.cols
            or placement.anchor_row + template.footprint_rows > fixed_map.rows
        ):
            print(
                f"[Tiles] {layer_name}: structure '{template.structure_id}' out of bounds "
                "for fixed map; skipping placement."
            )
            continue

        structure_is_valid = True
        for cell in template.cells:
            tile_id = cell.tile_id
            flags = selection_flags_by_tile_id.get(tile_id, {})
            if tile_id not in available_tile_ids:
                structure_is_valid = False
                break
            if bool(flags.get(exclude_flag_key, False)):
                structure_is_valid = False
                break

        if not structure_is_valid:
            print(
                f"[Tiles] {layer_name}: structure '{template.structure_id}' contains "
                "excluded or unresolved tiles; skipping entire structure."
            )
            continue

        for cell in template.cells:
            col = placement.anchor_col + cell.dx
            row = placement.anchor_row + cell.dy
            layer[row][col] = cell.tile_id

    for placement in standalone_placements:
        if (
            placement.col < 0
            or placement.col >= fixed_map.cols
            or placement.row < 0
            or placement.row >= fixed_map.rows
        ):
            continue

        flags = selection_flags_by_tile_id.get(placement.tile_id, {})
        if placement.tile_id not in available_tile_ids:
            continue
        if bool(flags.get(exclude_flag_key, False)):
            continue
        if not bool(flags.get("can_place_standalone", False)):
            continue

        layer[placement.row][placement.col] = placement.tile_id

    return _to_tuple_layer(layer)


class AshlandGroundLayer:
    """Renders fixed Ashland map layers by tile-id lookup through A5/A1/B manifests."""

    def __init__(self, fixed_map: FixedTileMap = ASHLAND_FIRST_MAP) -> None:
        self.fixed_map = fixed_map
        self.render_tile_size = fixed_map.tile_size
        self.pixel_scale = self.render_tile_size // SOURCE_TILE_SIZE

        self._a5_entries_by_id: dict[str, TileManifestEntry] = {}
        self._a1_entries_by_id: dict[str, TileManifestEntry] = {}
        self._b_entries_by_id: dict[str, TileManifestEntry] = {}
        self._a1_manifest_module: object | None = None
        self._b_manifest_module: object | None = None

        self._a5_tiles_by_id: dict[str, pygame.Surface] = {}
        self._a1_tiles_by_id: dict[str, pygame.Surface] = {}
        self._b_tiles_by_id: dict[str, pygame.Surface] = {}

        self._feature_layer: LayerGrid = _to_tuple_layer(
            _empty_layer(fixed_map.rows, fixed_map.cols)
        )
        self._detail_layer: LayerGrid = _to_tuple_layer(
            _empty_layer(fixed_map.rows, fixed_map.cols)
        )

        self._missing_base_tile_ids: set[str] = set()

        self._load_manifests_and_tiles()
        self._build_overlay_layers()
        self._validate_base_tile_ids()

    @property
    def is_available(self) -> bool:
        return bool(self._a5_tiles_by_id and not self._missing_base_tile_ids)

    def draw(
        self,
        surface: pygame.Surface,
        camera: Camera,
        world_width: float,
        world_height: float,
    ) -> bool:
        del world_width, world_height  # Fixed map dimensions are authoritative.
        if not self._a5_tiles_by_id:
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

                base_tile_id = self.fixed_map.base_layer[row][col]
                base_tile = self._a5_tiles_by_id.get(base_tile_id)
                if base_tile is not None:
                    surface.blit(base_tile, (screen_x, screen_y))

                feature_tile_id = self._feature_layer[row][col]
                if feature_tile_id:
                    feature_tile = self._a1_tiles_by_id.get(feature_tile_id)
                    if feature_tile is not None:
                        surface.blit(feature_tile, (screen_x, screen_y))

                detail_tile_id = self._detail_layer[row][col]
                if detail_tile_id:
                    detail_tile = self._b_tiles_by_id.get(detail_tile_id)
                    if detail_tile is not None:
                        surface.blit(detail_tile, (screen_x, screen_y))

        return True

    def _load_manifests_and_tiles(self) -> None:
        a5_module = _load_manifest_module(ASHLAND_A5_MANIFEST_PATH, "ashland_a5_manifest")
        self._a1_manifest_module = _load_manifest_module(
            ASHLAND_A1_MANIFEST_PATH,
            "ashland_a1_manifest",
        )
        self._b_manifest_module = _load_manifest_module(
            ASHLAND_B_MANIFEST_PATH,
            "ashland_b_manifest",
        )

        if a5_module is not None:
            self._a5_entries_by_id = _parse_manifest_entries(
                getattr(a5_module, "ASHLAND_A5_MANIFEST", None)
            )
            self._a5_tiles_by_id = _load_tile_surfaces(
                tileset_path=ASHLAND_A5_PATH,
                entries_by_id=self._a5_entries_by_id,
                pixel_scale=self.pixel_scale,
                tileset_label="Ashland A5",
            )

        if self._a1_manifest_module is not None:
            self._a1_entries_by_id = _parse_manifest_entries(
                getattr(self._a1_manifest_module, "ASHLAND_A1_MANIFEST", None)
            )
            self._a1_tiles_by_id = _load_tile_surfaces(
                tileset_path=ASHLAND_A1_PATH,
                entries_by_id=self._a1_entries_by_id,
                pixel_scale=self.pixel_scale,
                tileset_label="Ashland A1",
            )

        if self._b_manifest_module is not None:
            self._b_entries_by_id = _parse_manifest_entries(
                getattr(self._b_manifest_module, "ASHLAND_B_MANIFEST", None)
            )
            self._b_tiles_by_id = _load_tile_surfaces(
                tileset_path=ASHLAND_B_PATH,
                entries_by_id=self._b_entries_by_id,
                pixel_scale=self.pixel_scale,
                tileset_label="Ashland B",
            )

    def _build_overlay_layers(self) -> None:
        a1_templates = _parse_structure_templates(
            getattr(self._a1_manifest_module, "ASHLAND_A1_STRUCTURE_TEMPLATES", None)
            if self._a1_manifest_module
            else None
        )
        a1_flags: dict[str, dict[str, object]] = (
            getattr(self._a1_manifest_module, "ASHLAND_A1_TILE_SELECTION_FLAGS", {})
            if self._a1_manifest_module
            else {}
        )
        if not isinstance(a1_flags, dict):
            a1_flags = {}

        b_templates = _parse_structure_templates(
            getattr(self._b_manifest_module, "ASHLAND_B_STRUCTURE_TEMPLATES", None)
            if self._b_manifest_module
            else None
        )
        b_flags: dict[str, dict[str, object]] = (
            getattr(self._b_manifest_module, "ASHLAND_B_TILE_SELECTION_FLAGS", {})
            if self._b_manifest_module
            else {}
        )
        if not isinstance(b_flags, dict):
            b_flags = {}

        self._feature_layer = _compose_overlay_layer(
            fixed_map=self.fixed_map,
            layer_name="A1 feature layer",
            structure_placements=self.fixed_map.feature_structure_placements,
            standalone_placements=self.fixed_map.feature_standalone_placements,
            templates_by_id=a1_templates,
            selection_flags_by_tile_id=a1_flags,
            available_tile_ids=set(self._a1_tiles_by_id),
            exclude_flag_key="exclude_from_feature_selection",
        )

        self._detail_layer = _compose_overlay_layer(
            fixed_map=self.fixed_map,
            layer_name="B detail layer",
            structure_placements=self.fixed_map.detail_structure_placements,
            standalone_placements=self.fixed_map.detail_standalone_placements,
            templates_by_id=b_templates,
            selection_flags_by_tile_id=b_flags,
            available_tile_ids=set(self._b_tiles_by_id),
            exclude_flag_key="exclude_from_detail_selection",
        )

    def _validate_base_tile_ids(self) -> None:
        missing: set[str] = set()
        for row in self.fixed_map.base_layer:
            for tile_id in row:
                if tile_id not in self._a5_tiles_by_id:
                    missing.add(tile_id)
        self._missing_base_tile_ids = missing
        if missing:
            preview = ", ".join(sorted(missing)[:8])
            print(f"[Tiles] Fixed map has unresolved A5 tile IDs: {preview}")

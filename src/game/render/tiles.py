from __future__ import annotations

import importlib.util
import math
from dataclasses import dataclass
from pathlib import Path

import pygame

from game.render.camera import Camera
from game.render.fixed_map import ASHLAND_FIRST_MAP, SOURCE_TILE_SIZE, FixedTileMap
from game.render.spritesheet import load_image, pixelart_upscale_surface

ASHLAND_TILESET_ROOT = Path(__file__).resolve().parents[3] / "assets" / "tilesets" / "ashland"
ASHLAND_A5_PATH = ASHLAND_TILESET_ROOT / "tf_A5_ashlands_2.png"
ASHLAND_A5_MANIFEST_PATH = ASHLAND_TILESET_ROOT / "ashland_a5_manifest.py"


@dataclass(frozen=True, slots=True)
class TileManifestEntry:
    tile_id: str
    coord_col: int
    coord_row: int
    group: str
    tags: tuple[str, ...]
    walkable_default: bool


class AshlandGroundLayer:
    """Renders the fixed Ashland base map by tile-id lookup through A5 manifest."""

    def __init__(self, fixed_map: FixedTileMap = ASHLAND_FIRST_MAP) -> None:
        self.fixed_map = fixed_map
        self.render_tile_size = fixed_map.tile_size
        self.pixel_scale = self.render_tile_size // SOURCE_TILE_SIZE

        self._entries_by_id: dict[str, TileManifestEntry] = {}
        self._tile_surfaces_by_id: dict[str, pygame.Surface] = {}
        self._missing_map_tile_ids: set[str] = set()

        self._load_manifest_entries()
        self._load_tile_surfaces()
        self._validate_map_tile_ids()

    @property
    def is_available(self) -> bool:
        return bool(self._tile_surfaces_by_id and not self._missing_map_tile_ids)

    def draw(
        self,
        surface: pygame.Surface,
        camera: Camera,
        world_width: float,
        world_height: float,
    ) -> bool:
        del world_width, world_height  # Fixed map is authoritative for map dimensions.
        if not self._tile_surfaces_by_id:
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

        layer = self.fixed_map.base_layer
        for row in range(start_row, end_row + 1):
            for col in range(start_col, end_col + 1):
                tile_id = layer[row][col]
                tile = self._tile_surfaces_by_id.get(tile_id)
                if tile is None:
                    continue
                screen_x = round(col * tile_size - camera.offset_x)
                screen_y = round(row * tile_size - camera.offset_y)
                surface.blit(tile, (screen_x, screen_y))
        return True

    def _load_manifest_entries(self) -> None:
        if not ASHLAND_A5_MANIFEST_PATH.exists():
            print("[Tiles] Ashland A5 manifest not found; using fallback background.")
            return

        try:
            spec = importlib.util.spec_from_file_location(
                "ashland_a5_manifest",
                ASHLAND_A5_MANIFEST_PATH,
            )
            if spec is None or spec.loader is None:
                print("[Tiles] Failed to read Ashland A5 manifest module spec.")
                return
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        except Exception as error:
            print(f"[Tiles] Failed to import Ashland A5 manifest: {error}")
            return

        manifest = getattr(module, "ASHLAND_A5_MANIFEST", None)
        if not isinstance(manifest, dict):
            print("[Tiles] Ashland A5 manifest dictionary missing.")
            return

        entries_by_id: dict[str, TileManifestEntry] = {}
        for payload in manifest.values():
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
        self._entries_by_id = entries_by_id

    def _load_tile_surfaces(self) -> None:
        if not self._entries_by_id:
            return
        if self.pixel_scale <= 0:
            print("[Tiles] Invalid pixel scale for Ashland ground layer.")
            return

        sheet = load_image(ASHLAND_A5_PATH)
        if sheet is None:
            print("[Tiles] Ashland A5 tileset unavailable; using fallback background.")
            return

        sheet_width, sheet_height = sheet.get_size()
        max_col = sheet_width // SOURCE_TILE_SIZE
        max_row = sheet_height // SOURCE_TILE_SIZE

        loaded: dict[str, pygame.Surface] = {}
        for tile_id, entry in self._entries_by_id.items():
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
            loaded[tile_id] = pixelart_upscale_surface(tile_surface, self.pixel_scale)
        self._tile_surfaces_by_id = loaded

    def _validate_map_tile_ids(self) -> None:
        missing: set[str] = set()
        for row in self.fixed_map.base_layer:
            for tile_id in row:
                if tile_id not in self._tile_surfaces_by_id:
                    missing.add(tile_id)
        self._missing_map_tile_ids = missing
        if missing:
            preview = ", ".join(sorted(missing)[:8])
            print(f"[Tiles] Fixed map has unresolved A5 tile IDs: {preview}")

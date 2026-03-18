from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

import pygame

from game.core.blessings import (
    BLESSING_VFX_DAMAGE_AURA,
    BLESSING_VFX_DIVINE_PURGE,
    BLESSING_VFX_SACRED_RENEWAL,
)
from game.core.enemies import (
    ENEMY_VFX_ELITE_BURST_PROJECTILE_PURPLE,
    ENEMY_VFX_ELITE_SPAWN_DIRECTION,
    ENEMY_VFX_FLOATING_EYE_PURPLE,
    ENEMY_VFX_WARPED_SKULL_PROJECTILE_PURPLE,
)
from game.render.spritesheet import load_image, pixelart_upscale_surface

if TYPE_CHECKING:
    from game.render.camera import Camera

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_EFFECT_FRAME_SIZE = 16
# Keep blessing VFX timing feel consistent with the previous 6-frame @ 14 FPS setup.
_BLESSING_VFX_TARGET_DURATION_SECONDS = 6.0 / 14.0
_FLOATING_EYE_PRIME_DURATION_SECONDS = _BLESSING_VFX_TARGET_DURATION_SECONDS * 2.0


@dataclass(frozen=True, slots=True)
class EffectSheetDefinition:
    sheet_key: str
    image_path: str
    frame_size: int = DEFAULT_EFFECT_FRAME_SIZE


@dataclass(frozen=True, slots=True)
class EffectDefinition:
    effect_id: str
    sheet_key: str
    frame_sequence: tuple[tuple[int, int] | tuple[tuple[int, int], ...], ...]
    fps: float = 14.0
    scale_multiple: int = 3
    loop: bool = False


@dataclass(frozen=True, slots=True)
class EffectClip:
    frames: tuple[pygame.Surface, ...]
    fps: float
    loop: bool


@dataclass(slots=True)
class LoadedEffectSheet:
    definition: EffectSheetDefinition
    columns: int
    rows: int
    frames: dict[tuple[int, int], pygame.Surface]


@dataclass(slots=True)
class ActiveWorldEffect:
    instance_id: int
    effect_id: str
    position: tuple[float, float]
    frames: tuple[pygame.Surface, ...]
    fps: float
    loop: bool
    angle_degrees: float = 0.0
    travel_distance: float = 0.0
    travel_duration_seconds: float = 0.0
    anchor_player_id: str = ""
    anchor_distance: float = 0.0
    anchor_angle_degrees: float = 0.0
    elapsed_seconds: float = 0.0
    frame_index: int = 0
    frame_progress_seconds: float = 0.0


EFFECT_SHEET_CATALOG: dict[str, EffectSheetDefinition] = {
    "green_sheet": EffectSheetDefinition(
        sheet_key="green_sheet",
        image_path="assets/effects/green_effectsheet.png",
    ),
    "red_sheet": EffectSheetDefinition(
        sheet_key="red_sheet",
        image_path="assets/effects/red_effectsheet.png",
    ),
    "blue_sheet": EffectSheetDefinition(
        sheet_key="blue_sheet",
        image_path="assets/effects/blue_effectsheet.png",
    ),
    "purple_sheet": EffectSheetDefinition(
        sheet_key="purple_sheet",
        image_path="assets/effects/purple_effectsheet.png",
    ),
    "direction_sheet": EffectSheetDefinition(
        sheet_key="direction_sheet",
        image_path="assets/effects/direction.png",
    ),
}

# Frame coordinates use a 16x16 grid, with (0, 0) at the top-left tile.
EFFECT_CATALOG: dict[str, EffectDefinition] = {
    BLESSING_VFX_SACRED_RENEWAL: EffectDefinition(
        effect_id=BLESSING_VFX_SACRED_RENEWAL,
        sheet_key="green_sheet",
        frame_sequence=((14, 3), (15, 3), (16, 3), (17, 3)),
        fps=4.0 / _BLESSING_VFX_TARGET_DURATION_SECONDS,
        scale_multiple=3,
        loop=False,
    ),
    BLESSING_VFX_DIVINE_PURGE: EffectDefinition(
        effect_id=BLESSING_VFX_DIVINE_PURGE,
        sheet_key="red_sheet",
        frame_sequence=((0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1)),
        fps=14.0,
        scale_multiple=3,
        loop=False,
    ),
    BLESSING_VFX_DAMAGE_AURA: EffectDefinition(
        effect_id=BLESSING_VFX_DAMAGE_AURA,
        sheet_key="blue_sheet",
        frame_sequence=((28, 8), (27, 8), (26, 8), (25, 8), (24, 8)),
        fps=5.0 / _BLESSING_VFX_TARGET_DURATION_SECONDS,
        scale_multiple=9,
        loop=True,
    ),
    ENEMY_VFX_FLOATING_EYE_PURPLE: EffectDefinition(
        effect_id=ENEMY_VFX_FLOATING_EYE_PURPLE,
        sheet_key="purple_sheet",
        frame_sequence=((28, 8), (27, 8), (26, 8), (25, 8), (24, 8)),
        fps=5.0 / _FLOATING_EYE_PRIME_DURATION_SECONDS,
        scale_multiple=6,
        loop=True,
    ),
    ENEMY_VFX_WARPED_SKULL_PROJECTILE_PURPLE: EffectDefinition(
        effect_id=ENEMY_VFX_WARPED_SKULL_PROJECTILE_PURPLE,
        sheet_key="purple_sheet",
        frame_sequence=((30, 0), (31, 0), (32, 0), (33, 0), (34, 0), (35, 0)),
        fps=14.0,
        scale_multiple=3,
        loop=True,
    ),
    ENEMY_VFX_ELITE_BURST_PROJECTILE_PURPLE: EffectDefinition(
        effect_id=ENEMY_VFX_ELITE_BURST_PROJECTILE_PURPLE,
        sheet_key="purple_sheet",
        frame_sequence=((19, 7), (20, 7), (21, 7), (22, 7)),
        fps=14.0,
        scale_multiple=3,
        loop=True,
    ),
    ENEMY_VFX_ELITE_SPAWN_DIRECTION: EffectDefinition(
        effect_id=ENEMY_VFX_ELITE_SPAWN_DIRECTION,
        sheet_key="direction_sheet",
        frame_sequence=((0, 0),),
        fps=1.0,
        scale_multiple=3,
        loop=False,
    ),
    "active_ability.guardian_spirit.loop": EffectDefinition(
        effect_id="active_ability.guardian_spirit.loop",
        sheet_key="green_sheet",
        frame_sequence=((7, 8), (8, 8)),
        fps=6.0,
        scale_multiple=5,
        loop=True,
    ),
    "active_ability.shockwave.activate": EffectDefinition(
        effect_id="active_ability.shockwave.activate",
        sheet_key="blue_sheet",
        frame_sequence=(
            ((10, 3), (10, 4)),
            ((11, 3), (11, 4)),
            ((12, 3), (12, 4)),
        ),
        fps=6.0,
        scale_multiple=6,
        loop=False,
    ),
}


class EffectClipLibrary:
    def __init__(
        self,
        *,
        sheet_catalog: dict[str, EffectSheetDefinition] | None = None,
        effect_catalog: dict[str, EffectDefinition] | None = None,
    ) -> None:
        self.sheet_catalog = sheet_catalog or EFFECT_SHEET_CATALOG
        self.effect_catalog = effect_catalog or EFFECT_CATALOG
        self._loaded_sheets: dict[str, LoadedEffectSheet | None] = {}
        self._clip_cache: dict[str, EffectClip | None] = {}
        self._warned_effect_ids: set[str] = set()
        self._warned_frame_coords: set[tuple[str, tuple[int, int]]] = set()

        for sheet_key in self.sheet_catalog:
            self._loaded_sheets[sheet_key] = self._load_sheet(sheet_key)

    def get_clip(self, effect_id: str) -> EffectClip | None:
        if effect_id in self._clip_cache:
            return self._clip_cache[effect_id]

        definition = self.effect_catalog.get(effect_id)
        if definition is None:
            self._warn_once_unknown_effect(effect_id)
            self._clip_cache[effect_id] = None
            return None

        sheet = self._loaded_sheets.get(definition.sheet_key)
        if sheet is None:
            self._clip_cache[effect_id] = None
            return None

        clip_frames: list[pygame.Surface] = []
        for frame_coord in definition.frame_sequence:
            source_frame = self._normalize_source_frame(frame_coord)
            frame = self._compose_source_frame(sheet, effect_id, source_frame)
            if frame is None:
                self._clip_cache[effect_id] = None
                return None
            clip_frames.append(pixelart_upscale_surface(frame, max(1, definition.scale_multiple)))

        if not clip_frames:
            self._clip_cache[effect_id] = None
            return None

        clip = EffectClip(frames=tuple(clip_frames), fps=definition.fps, loop=definition.loop)
        self._clip_cache[effect_id] = clip
        return clip

    def _compose_source_frame(
        self,
        sheet: LoadedEffectSheet,
        effect_id: str,
        source_frame: tuple[tuple[int, int], ...],
    ) -> pygame.Surface | None:
        if not source_frame:
            return None

        missing_coords: list[tuple[int, int]] = []
        for coord in source_frame:
            if coord not in sheet.frames:
                missing_coords.append(coord)
        if missing_coords:
            for coord in missing_coords:
                self._warn_once_missing_frame(effect_id, coord)
            return None

        min_col = min(coord[0] for coord in source_frame)
        max_col = max(coord[0] for coord in source_frame)
        min_row = min(coord[1] for coord in source_frame)
        max_row = max(coord[1] for coord in source_frame)
        frame_size = max(1, int(sheet.definition.frame_size))

        composed_width = (max_col - min_col + 1) * frame_size
        composed_height = (max_row - min_row + 1) * frame_size
        composed = pygame.Surface((composed_width, composed_height), pygame.SRCALPHA)

        for col, row in source_frame:
            tile = sheet.frames[(col, row)]
            target_x = (col - min_col) * frame_size
            target_y = (row - min_row) * frame_size
            composed.blit(tile, (target_x, target_y))
        return composed

    @staticmethod
    def _normalize_source_frame(
        frame_spec: tuple[int, int] | tuple[tuple[int, int], ...],
    ) -> tuple[tuple[int, int], ...]:
        if (
            len(frame_spec) == 2
            and isinstance(frame_spec[0], int)
            and isinstance(frame_spec[1], int)
        ):
            return (frame_spec,)
        return tuple(frame_spec)

    def sheet_frame_counts(self) -> dict[str, tuple[int, int]]:
        result: dict[str, tuple[int, int]] = {}
        for sheet_key, loaded in self._loaded_sheets.items():
            if loaded is not None:
                result[sheet_key] = (loaded.columns, loaded.rows)
        return result

    def _load_sheet(self, sheet_key: str) -> LoadedEffectSheet | None:
        definition = self.sheet_catalog[sheet_key]
        image = load_image(PROJECT_ROOT / definition.image_path)
        if image is None:
            return None

        frame_size = max(1, int(definition.frame_size))
        sheet_width, sheet_height = image.get_size()
        columns = sheet_width // frame_size
        rows = sheet_height // frame_size
        if columns <= 0 or rows <= 0:
            print(
                "[VFX] Invalid frame grid for sheet "
                f"'{definition.sheet_key}' ({sheet_width}x{sheet_height})."
            )
            return None

        frames: dict[tuple[int, int], pygame.Surface] = {}
        for row in range(rows):
            for col in range(columns):
                rect = pygame.Rect(col * frame_size, row * frame_size, frame_size, frame_size)
                frames[(col, row)] = image.subsurface(rect).copy()

        return LoadedEffectSheet(
            definition=definition,
            columns=columns,
            rows=rows,
            frames=frames,
        )

    def _warn_once_unknown_effect(self, effect_id: str) -> None:
        if effect_id in self._warned_effect_ids:
            return
        self._warned_effect_ids.add(effect_id)
        print(f"[VFX] Unknown effect id: {effect_id}")

    def _warn_once_missing_frame(self, effect_id: str, frame_coord: tuple[int, int]) -> None:
        warning_key = (effect_id, frame_coord)
        if warning_key in self._warned_frame_coords:
            return
        self._warned_frame_coords.add(warning_key)
        print(f"[VFX] Missing frame {frame_coord} for effect '{effect_id}'")


class WorldEffectPlayer:
    def __init__(self, library: EffectClipLibrary | None = None) -> None:
        self.library = library or EffectClipLibrary()
        self._active_effects: dict[int, ActiveWorldEffect] = {}
        self._next_instance_id = 1

    def clear(self) -> None:
        self._active_effects.clear()
        self._next_instance_id = 1

    def consume_events(self, events: list[dict[str, object]]) -> None:
        for payload in events:
            if not isinstance(payload, dict):
                continue
            effect_id = str(payload.get("effect_id", ""))
            if not effect_id:
                continue

            clip = self.library.get_clip(effect_id)
            if clip is None or not clip.frames:
                continue

            position = self._read_position(payload.get("position"))
            angle_degrees = self._read_angle(payload.get("angle_degrees"))
            travel_distance = max(0.0, self._read_float(payload.get("travel_distance")))
            travel_duration_seconds = max(
                0.0,
                self._read_float(payload.get("travel_duration_seconds")),
            )
            anchor_player_id = str(payload.get("anchor_player_id", "")).strip()
            anchor_distance = max(0.0, self._read_float(payload.get("anchor_distance")))
            anchor_angle_degrees = self._read_angle(payload.get("anchor_angle_degrees"))
            if travel_distance > 0.0 and travel_duration_seconds <= 0.0:
                travel_duration_seconds = len(clip.frames) / max(0.01, float(clip.fps))
            instance = ActiveWorldEffect(
                instance_id=self._next_instance_id,
                effect_id=effect_id,
                position=position,
                frames=clip.frames,
                fps=clip.fps,
                loop=clip.loop,
                angle_degrees=angle_degrees,
                travel_distance=travel_distance,
                travel_duration_seconds=travel_duration_seconds,
                anchor_player_id=anchor_player_id,
                anchor_distance=anchor_distance,
                anchor_angle_degrees=anchor_angle_degrees,
            )
            self._active_effects[instance.instance_id] = instance
            self._next_instance_id += 1

    def update_and_draw(
        self,
        screen: pygame.Surface,
        camera: Camera,
        render_dt: float,
        *,
        player_positions: dict[str, tuple[float, float]] | None = None,
    ) -> None:
        expired_ids: list[int] = []
        known_player_positions = player_positions or {}
        for instance_id, effect in self._active_effects.items():
            if not effect.frames:
                expired_ids.append(instance_id)
                continue

            frame = effect.frames[effect.frame_index]
            if abs(effect.angle_degrees) > 0.01:
                frame = pygame.transform.rotate(frame, -effect.angle_degrees)
            center = camera.world_to_screen(
                self._position_for_effect(effect, known_player_positions)
            )
            rect = frame.get_rect(center=center)
            screen.blit(frame, rect)

            effect.elapsed_seconds += max(0.0, render_dt)
            if self._advance(effect, render_dt):
                expired_ids.append(instance_id)

        for instance_id in expired_ids:
            self._active_effects.pop(instance_id, None)

    @staticmethod
    def _advance(effect: ActiveWorldEffect, render_dt: float) -> bool:
        if not effect.frames:
            return True

        frame_duration = 1.0 / max(0.01, float(effect.fps))
        effect.frame_progress_seconds += max(0.0, render_dt)

        while effect.frame_progress_seconds >= frame_duration:
            effect.frame_progress_seconds -= frame_duration
            if effect.frame_index < len(effect.frames) - 1:
                effect.frame_index += 1
                continue
            if effect.loop:
                effect.frame_index = 0
                continue
            return True

        return False

    @staticmethod
    def _read_position(payload: object) -> tuple[float, float]:
        if isinstance(payload, dict):
            return (float(payload.get("x", 0.0)), float(payload.get("y", 0.0)))
        return (0.0, 0.0)

    @staticmethod
    def _read_angle(payload: object) -> float:
        try:
            return float(payload)
        except (TypeError, ValueError):
            return 0.0

    @staticmethod
    def _read_float(payload: object) -> float:
        try:
            return float(payload)
        except (TypeError, ValueError):
            return 0.0

    @staticmethod
    def _position_for_effect(
        effect: ActiveWorldEffect,
        player_positions: dict[str, tuple[float, float]],
    ) -> tuple[float, float]:
        if effect.anchor_player_id:
            player_position = player_positions.get(effect.anchor_player_id)
            if player_position is not None:
                anchor_radians = math.radians(effect.anchor_angle_degrees)
                return (
                    player_position[0] + math.cos(anchor_radians) * effect.anchor_distance,
                    player_position[1] + math.sin(anchor_radians) * effect.anchor_distance,
                )
        if effect.travel_distance <= 0.0 or effect.travel_duration_seconds <= 0.0:
            return effect.position

        progress = max(0.0, min(1.0, effect.elapsed_seconds / effect.travel_duration_seconds))
        radians = math.radians(effect.angle_degrees)
        offset_x = math.cos(radians) * effect.travel_distance * progress
        offset_y = math.sin(radians) * effect.travel_distance * progress
        return (effect.position[0] + offset_x, effect.position[1] + offset_y)

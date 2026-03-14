from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

import pygame

from game.core.blessings import (
    BLESSING_VFX_DAMAGE_AURA,
    BLESSING_VFX_ENEMY_CLEAR,
    BLESSING_VFX_FULL_HEAL,
)
from game.core.enemies import ENEMY_VFX_FLOATING_EYE_PURPLE
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
    frame_sequence: tuple[tuple[int, int], ...]
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
}

# Frame coordinates use a 16x16 grid, with (0, 0) at the top-left tile.
EFFECT_CATALOG: dict[str, EffectDefinition] = {
    BLESSING_VFX_FULL_HEAL: EffectDefinition(
        effect_id=BLESSING_VFX_FULL_HEAL,
        sheet_key="green_sheet",
        frame_sequence=((14, 3), (15, 3), (16, 3), (17, 3)),
        fps=4.0 / _BLESSING_VFX_TARGET_DURATION_SECONDS,
        scale_multiple=3,
        loop=False,
    ),
    BLESSING_VFX_ENEMY_CLEAR: EffectDefinition(
        effect_id=BLESSING_VFX_ENEMY_CLEAR,
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
            frame = sheet.frames.get(frame_coord)
            if frame is None:
                self._warn_once_missing_frame(effect_id, frame_coord)
                self._clip_cache[effect_id] = None
                return None
            clip_frames.append(pixelart_upscale_surface(frame, max(1, definition.scale_multiple)))

        if not clip_frames:
            self._clip_cache[effect_id] = None
            return None

        clip = EffectClip(frames=tuple(clip_frames), fps=definition.fps, loop=definition.loop)
        self._clip_cache[effect_id] = clip
        return clip

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
            instance = ActiveWorldEffect(
                instance_id=self._next_instance_id,
                effect_id=effect_id,
                position=position,
                frames=clip.frames,
                fps=clip.fps,
                loop=clip.loop,
            )
            self._active_effects[instance.instance_id] = instance
            self._next_instance_id += 1

    def update_and_draw(self, screen: pygame.Surface, camera: Camera, render_dt: float) -> None:
        expired_ids: list[int] = []
        for instance_id, effect in self._active_effects.items():
            if not effect.frames:
                expired_ids.append(instance_id)
                continue

            frame = effect.frames[effect.frame_index]
            center = camera.world_to_screen(effect.position)
            rect = frame.get_rect(center=center)
            screen.blit(frame, rect)

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

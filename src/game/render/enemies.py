from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pygame

from game.core.enemy_catalog import get_enemy_profiles
from game.render.characters import ANIM_IDLE, AnimationClip
from game.render.spritesheet import load_spritesheet_frames, pixelart_upscale_surface

DEFAULT_ENEMY_FRAME_COUNT = 4
DEFAULT_ENEMY_FPS = 8.0
DEFAULT_ENEMY_PIXEL_SCALE = 3


@dataclass(frozen=True, slots=True)
class EnemySpriteDefinition:
    enemy_id: str
    display_name: str
    sheet_path: Path
    frame_count: int = DEFAULT_ENEMY_FRAME_COUNT
    fps: float = DEFAULT_ENEMY_FPS
    pixel_scale: int = DEFAULT_ENEMY_PIXEL_SCALE


@dataclass(frozen=True, slots=True)
class LoadedEnemyAssets:
    definition: EnemySpriteDefinition
    animations: dict[str, AnimationClip]


class EnemySpriteLibrary:
    def __init__(self, definitions: dict[str, EnemySpriteDefinition] | None = None) -> None:
        self.definitions = definitions or get_enemy_sprite_definitions()
        self.assets: dict[str, LoadedEnemyAssets] = {}
        self._ordered_enemy_ids: list[str] = []
        self._preview_cache: dict[tuple[str, int], pygame.Surface | None] = {}

        for enemy_id, definition in self.definitions.items():
            loaded = self._load_enemy_assets(definition)
            self.assets[enemy_id] = loaded
            if loaded.animations.get(ANIM_IDLE) is not None:
                self._ordered_enemy_ids.append(enemy_id)

    def get_animation_clip(
        self, enemy_id: str, animation_name: str = ANIM_IDLE
    ) -> AnimationClip | None:
        assets = self.assets.get(enemy_id)
        if assets is None:
            return None
        clip = assets.animations.get(animation_name)
        if clip is not None:
            return clip
        return assets.animations.get(ANIM_IDLE)

    def enemy_id_for_entity(self, entity_id: int) -> str | None:
        if not self._ordered_enemy_ids:
            return None
        return self._ordered_enemy_ids[entity_id % len(self._ordered_enemy_ids)]

    def get_idle_clip_for_entity(self, entity_id: int) -> AnimationClip | None:
        enemy_id = self.enemy_id_for_entity(entity_id)
        if enemy_id is None:
            return None
        return self.get_animation_clip(enemy_id, ANIM_IDLE)

    def get_idle_clip(
        self,
        *,
        profile_id: str | None = None,
        entity_id: int = -1,
    ) -> AnimationClip | None:
        if profile_id:
            clip = self.get_animation_clip(profile_id, ANIM_IDLE)
            if clip is not None:
                return clip
        if entity_id >= 0:
            return self.get_idle_clip_for_entity(entity_id)
        return None

    @property
    def loaded_enemy_count(self) -> int:
        return len(self._ordered_enemy_ids)

    def get_preview_sprite(self, enemy_id: str, *, max_size: int) -> pygame.Surface | None:
        cache_key = (enemy_id, max(1, int(max_size)))
        if cache_key in self._preview_cache:
            return self._preview_cache[cache_key]

        definition = self.definitions.get(enemy_id)
        if definition is None:
            self._preview_cache[cache_key] = None
            return None

        base_frames = load_spritesheet_frames(
            definition.sheet_path,
            definition.frame_count,
            pixel_scale=1,
        )
        if not base_frames:
            self._preview_cache[cache_key] = None
            return None

        base_frame = base_frames[0]
        base_max_dim = max(1, max(base_frame.get_width(), base_frame.get_height()))
        scale_multiple = max(1, int(max_size) // base_max_dim)
        preview_frame = pixelart_upscale_surface(base_frame, scale_multiple)
        self._preview_cache[cache_key] = preview_frame
        return preview_frame

    def _load_enemy_assets(self, definition: EnemySpriteDefinition) -> LoadedEnemyAssets:
        idle_frames = load_spritesheet_frames(
            definition.sheet_path,
            definition.frame_count,
            pixel_scale=definition.pixel_scale,
        )

        animations: dict[str, AnimationClip] = {}
        if idle_frames:
            animations[ANIM_IDLE] = AnimationClip(
                frames=idle_frames,
                fps=definition.fps,
                loop=True,
            )
        else:
            print(
                "[Enemies] Failed to load idle animation for "
                f"{definition.enemy_id}; circle fallback rendering will be used."
            )

        return LoadedEnemyAssets(
            definition=definition,
            animations=animations,
        )


def get_enemy_sprite_definitions() -> dict[str, EnemySpriteDefinition]:
    assets_root = Path(__file__).resolve().parents[3] / "assets" / "enemies"
    definitions: dict[str, EnemySpriteDefinition] = {}
    for profile in get_enemy_profiles().values():
        asset_name = profile.sprite_asset_name or f"{profile.display_name.replace(' ', '')}.png"
        definitions[profile.profile_id] = EnemySpriteDefinition(
            enemy_id=profile.profile_id,
            display_name=profile.display_name,
            sheet_path=assets_root / asset_name,
            pixel_scale=profile.sprite_pixel_scale or DEFAULT_ENEMY_PIXEL_SCALE,
        )
    return definitions

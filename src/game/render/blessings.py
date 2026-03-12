from __future__ import annotations

from pathlib import Path

import pygame

from game.core.blessings import BlessingDefinition, get_blessing, list_blessings
from game.render.spritesheet import load_image, pixelart_upscale_surface

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_BLESSING_ICON_SCALE = 2


class BlessingSpriteLibrary:
    def __init__(
        self,
        definitions: list[BlessingDefinition] | None = None,
        *,
        world_icon_scale: int = DEFAULT_BLESSING_ICON_SCALE,
    ) -> None:
        base_definitions = definitions or list_blessings()
        self.definitions = {definition.blessing_id: definition for definition in base_definitions}
        self.world_icon_scale = max(1, int(world_icon_scale))
        self._base_icons: dict[str, pygame.Surface | None] = {}
        self._scaled_cache: dict[tuple[str, int], pygame.Surface | None] = {}

        for blessing_id, definition in self.definitions.items():
            icon_path = PROJECT_ROOT / definition.icon_path
            self._base_icons[blessing_id] = load_image(icon_path)

    def get_icon(
        self, blessing_id: str, scale_multiple: int | None = None
    ) -> pygame.Surface | None:
        definition = self.definitions.get(blessing_id) or get_blessing(blessing_id)
        if definition is None:
            return None

        safe_scale = (
            self.world_icon_scale if scale_multiple is None else max(1, int(scale_multiple))
        )
        cache_key = (definition.blessing_id, safe_scale)
        if cache_key in self._scaled_cache:
            return self._scaled_cache[cache_key]

        base = self._base_icons.get(definition.blessing_id)
        if base is None:
            self._scaled_cache[cache_key] = None
            return None

        if safe_scale == 1:
            self._scaled_cache[cache_key] = base
            return base

        scaled = pixelart_upscale_surface(base, safe_scale)
        self._scaled_cache[cache_key] = scaled
        return scaled

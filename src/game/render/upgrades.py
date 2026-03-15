from __future__ import annotations

from pathlib import Path

import pygame

from game.core.upgrades import UpgradeDefinition, get_upgrade, list_upgrades
from game.render.spritesheet import load_image, pixelart_upscale_surface

PROJECT_ROOT = Path(__file__).resolve().parents[3]


class UpgradeSpriteLibrary:
    def __init__(self, definitions: list[UpgradeDefinition] | None = None) -> None:
        base_definitions = definitions or list_upgrades()
        self.definitions = {definition.upgrade_id: definition for definition in base_definitions}
        self._base_icons: dict[str, pygame.Surface | None] = {}
        self._scaled_cache: dict[tuple[str, int, int], pygame.Surface | None] = {}

        for upgrade_id, definition in self.definitions.items():
            self._base_icons[upgrade_id] = load_image(PROJECT_ROOT / definition.icon_path)

    def get_icon(self, upgrade_id: str, max_size: tuple[int, int]) -> pygame.Surface | None:
        definition = self.definitions.get(upgrade_id) or get_upgrade(upgrade_id)
        if definition is None:
            return None

        safe_size = (max(1, int(max_size[0])), max(1, int(max_size[1])))
        cache_key = (definition.upgrade_id, safe_size[0], safe_size[1])
        if cache_key in self._scaled_cache:
            return self._scaled_cache[cache_key]

        base = self._base_icons.get(definition.upgrade_id)
        if base is None:
            self._scaled_cache[cache_key] = None
            return None

        width, height = base.get_size()
        if width <= 0 or height <= 0:
            self._scaled_cache[cache_key] = None
            return None

        scale = min(safe_size[0] / width, safe_size[1] / height)
        target_size = (
            max(1, int(round(width * scale))),
            max(1, int(round(height * scale))),
        )
        if target_size == base.get_size():
            self._scaled_cache[cache_key] = base
            return base

        if scale >= 1.0:
            scale_multiple = max(1, int(scale))
            scaled = pixelart_upscale_surface(base, scale_multiple)
        else:
            scaled = pygame.transform.scale(base, target_size)
        self._scaled_cache[cache_key] = scaled
        return scaled

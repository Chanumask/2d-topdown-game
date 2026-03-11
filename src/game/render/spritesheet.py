from __future__ import annotations

from pathlib import Path

import pygame


def load_spritesheet_frames(path: Path, frame_count: int) -> list[pygame.Surface] | None:
    if frame_count <= 0:
        return None
    if not path.exists():
        print(f"[Spritesheet] Missing file: {path}")
        return None

    try:
        sheet = pygame.image.load(str(path))
        if pygame.display.get_surface() is not None:
            sheet = sheet.convert_alpha()
    except Exception as error:
        print(f"[Spritesheet] Failed to load {path}: {error}")
        return None

    sheet_width, sheet_height = sheet.get_size()
    frame_width = sheet_width // frame_count
    if frame_width <= 0:
        print(f"[Spritesheet] Invalid frame width in {path}")
        return None

    frames: list[pygame.Surface] = []
    for index in range(frame_count):
        frame_rect = pygame.Rect(index * frame_width, 0, frame_width, sheet_height)
        frame = sheet.subsurface(frame_rect).copy()
        frames.append(frame)

    return frames


def load_image(path: Path) -> pygame.Surface | None:
    if not path.exists():
        print(f"[Assets] Missing image: {path}")
        return None

    try:
        image = pygame.image.load(str(path))
        if pygame.display.get_surface() is not None:
            image = image.convert_alpha()
        return image
    except Exception as error:
        print(f"[Assets] Failed to load image {path}: {error}")
        return None

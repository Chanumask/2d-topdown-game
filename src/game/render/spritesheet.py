from __future__ import annotations

from pathlib import Path

import pygame


def load_spritesheet_frames(
    path: Path,
    frame_count: int,
    *,
    frame_width: int | None = None,
    frame_height: int | None = None,
    scale: float = 1.0,
    smooth: bool = False,
    pixel_scale: int | None = None,
) -> list[pygame.Surface] | None:
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
    resolved_frame_width = (
        int(frame_width) if frame_width is not None else sheet_width // frame_count
    )
    resolved_frame_height = int(frame_height) if frame_height is not None else sheet_height
    if resolved_frame_width <= 0 or resolved_frame_height <= 0:
        print(f"[Spritesheet] Invalid frame width in {path}")
        return None
    if resolved_frame_width * frame_count > sheet_width or resolved_frame_height > sheet_height:
        print(f"[Spritesheet] Frame geometry exceeds sheet bounds in {path}")
        return None

    frames: list[pygame.Surface] = []
    for index in range(frame_count):
        frame_rect = pygame.Rect(
            index * resolved_frame_width,
            0,
            resolved_frame_width,
            resolved_frame_height,
        )
        frame = sheet.subsurface(frame_rect).copy()
        if pixel_scale is not None:
            frame = pixelart_upscale_surface(frame, pixel_scale)
        elif scale != 1.0:
            frame = scale_surface(frame, scale=scale, smooth=smooth)
        frames.append(frame)

    return frames


def scale_surface(
    surface: pygame.Surface,
    *,
    scale: float,
    smooth: bool,
) -> pygame.Surface:
    width, height = surface.get_size()
    scaled_size = (max(1, int(round(width * scale))), max(1, int(round(height * scale))))
    if smooth:
        return pygame.transform.smoothscale(surface, scaled_size)
    return pygame.transform.scale(surface, scaled_size)


def pixelart_upscale_surface(surface: pygame.Surface, scale_multiple: int) -> pygame.Surface:
    if scale_multiple < 1:
        raise ValueError("scale_multiple must be >= 1")
    if scale_multiple == 1:
        return surface

    width, height = surface.get_size()
    return pygame.transform.scale(
        surface,
        (width * scale_multiple, height * scale_multiple),
    )


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


def load_pixelart_image(path: Path, scale_multiple: int = 1) -> pygame.Surface | None:
    image = load_image(path)
    if image is None:
        return None
    return pixelart_upscale_surface(image, scale_multiple)

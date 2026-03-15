from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pygame

DEFAULT_FONT_RELATIVE_PATH = Path("assets/fonts/game_font.ttf")


@dataclass(frozen=True, slots=True)
class UIFonts:
    title: pygame.font.Font
    heading: pygame.font.Font
    body: pygame.font.Font
    small: pygame.font.Font
    hud: pygame.font.Font
    using_custom_font: bool
    source_path: str | None
    reference_sizes: tuple[int, int, int, int, int]


def load_ui_fonts(font_path: Path | None = None) -> UIFonts:
    resolved_font_path = _resolve_custom_font(font_path)
    using_custom_font = resolved_font_path is not None

    if not using_custom_font:
        print(
            "[Fonts] Could not load assets/fonts/game_font.ttf. "
            "Falling back to default pygame font."
        )

    return UIFonts(
        title=_create_font(resolved_font_path, 56),
        heading=_create_font(resolved_font_path, 42),
        body=_create_font(resolved_font_path, 30),
        small=_create_font(resolved_font_path, 24),
        hud=_create_font(resolved_font_path, 22),
        using_custom_font=using_custom_font,
        source_path=str(resolved_font_path) if resolved_font_path is not None else None,
        reference_sizes=(56, 42, 30, 24, 22),
    )


def scale_ui_fonts(
    base_fonts: UIFonts,
    *,
    scale: float,
    title_scale: float | None = None,
    heading_scale: float | None = None,
    hud_scale: float | None = None,
) -> UIFonts:
    source_path = Path(base_fonts.source_path) if base_fonts.source_path is not None else None
    title_base, heading_base, body_base, small_base, hud_base = base_fonts.reference_sizes
    body_factor = max(0.62, min(1.0, float(scale)))
    title_factor = (
        max(0.60, min(1.0, float(title_scale)))
        if title_scale is not None
        else body_factor
    )
    heading_factor = (
        max(0.60, min(1.0, float(heading_scale)))
        if heading_scale is not None
        else body_factor
    )
    hud_factor = (
        max(0.62, min(1.0, float(hud_scale)))
        if hud_scale is not None
        else body_factor
    )

    return UIFonts(
        title=_create_font(source_path, max(20, int(round(title_base * title_factor)))),
        heading=_create_font(source_path, max(18, int(round(heading_base * heading_factor)))),
        body=_create_font(source_path, max(15, int(round(body_base * body_factor)))),
        small=_create_font(source_path, max(13, int(round(small_base * body_factor)))),
        hud=_create_font(source_path, max(13, int(round(hud_base * hud_factor)))),
        using_custom_font=base_fonts.using_custom_font,
        source_path=base_fonts.source_path,
        reference_sizes=base_fonts.reference_sizes,
    )


def _create_font(path: Path | None, size: int) -> pygame.font.Font:
    if path is None:
        return pygame.font.Font(None, size)
    return pygame.font.Font(str(path), size)


def _resolve_custom_font(font_path: Path | None) -> Path | None:
    candidates: list[Path]
    if font_path is not None:
        candidates = [font_path]
    else:
        repo_root = Path(__file__).resolve().parents[3]
        candidates = [
            repo_root / DEFAULT_FONT_RELATIVE_PATH,
            Path.cwd() / DEFAULT_FONT_RELATIVE_PATH,
        ]

    for candidate in candidates:
        if not candidate.exists():
            continue
        try:
            pygame.font.Font(str(candidate), 16)
            return candidate
        except Exception as error:
            print(f"[Fonts] Failed to load custom font at {candidate}: {error}")

    return None

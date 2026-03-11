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

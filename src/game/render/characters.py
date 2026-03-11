from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pygame

from game.render.spritesheet import load_image, load_spritesheet_frames

ANIM_IDLE = "idle"
ANIM_WALK = "walk"
ANIM_THROW = "throw"
ANIM_DEATH = "death"

DEFAULT_CHARACTER_ID = "dude_monster"
DEFAULT_PLAYER_SPRITE_SCALE = 2.0


@dataclass(frozen=True, slots=True)
class AnimationSheetDefinition:
    sheet_path: Path
    frame_count: int
    fps: float
    loop: bool = True


@dataclass(frozen=True, slots=True)
class CharacterDefinition:
    character_id: str
    display_name: str
    portrait_path: Path
    animations: dict[str, AnimationSheetDefinition]
    sprite_scale: float = DEFAULT_PLAYER_SPRITE_SCALE


@dataclass(frozen=True, slots=True)
class AnimationClip:
    frames: list[pygame.Surface]
    fps: float
    loop: bool

    @property
    def duration_seconds(self) -> float:
        if self.fps <= 0.0:
            return 0.0
        return len(self.frames) / self.fps


@dataclass(slots=True)
class LoadedCharacterAssets:
    definition: CharacterDefinition
    portrait: pygame.Surface | None
    animations: dict[str, AnimationClip]


class CharacterSpriteLibrary:
    def __init__(self, definitions: dict[str, CharacterDefinition] | None = None) -> None:
        self.definitions = definitions or get_character_definitions()
        self.default_character_id = _resolve_default_character_id(self.definitions)
        self.assets: dict[str, LoadedCharacterAssets] = {}

        for character_id, definition in self.definitions.items():
            self.assets[character_id] = self._load_character_assets(definition)

    def get_character(self, character_id: str) -> LoadedCharacterAssets | None:
        return self.assets.get(character_id) or self.assets.get(self.default_character_id)

    def get_animation_clip(self, character_id: str, animation_name: str) -> AnimationClip | None:
        character_assets = self.get_character(character_id)
        if character_assets is None:
            return None

        clip = character_assets.animations.get(animation_name)
        if clip is not None:
            return clip
        return character_assets.animations.get(ANIM_IDLE)

    def _load_character_assets(self, definition: CharacterDefinition) -> LoadedCharacterAssets:
        animations: dict[str, AnimationClip] = {}
        portrait = load_image(definition.portrait_path)

        for animation_name, animation_def in definition.animations.items():
            frames = load_spritesheet_frames(animation_def.sheet_path, animation_def.frame_count)
            if not frames:
                continue

            scaled_frames = [_scale_frame(frame, definition.sprite_scale) for frame in frames]
            animations[animation_name] = AnimationClip(
                frames=scaled_frames,
                fps=animation_def.fps,
                loop=animation_def.loop,
            )

        if not animations:
            print(
                "[Characters] No animations loaded for "
                f"{definition.character_id}. Player fallback rendering will be used."
            )

        return LoadedCharacterAssets(
            definition=definition,
            portrait=portrait,
            animations=animations,
        )


def get_character_definitions() -> dict[str, CharacterDefinition]:
    assets_root = Path(__file__).resolve().parents[3] / "assets" / "characters"

    return {
        "dude_monster": CharacterDefinition(
            character_id="dude_monster",
            display_name="Dude Monster",
            portrait_path=assets_root / "dude_monster" / "Dude_Monster.png",
            animations={
                ANIM_IDLE: AnimationSheetDefinition(
                    sheet_path=assets_root / "dude_monster" / "Dude_Monster_Idle_4.png",
                    frame_count=4,
                    fps=6.0,
                    loop=True,
                ),
                ANIM_WALK: AnimationSheetDefinition(
                    sheet_path=assets_root / "dude_monster" / "Dude_Monster_Walk_6.png",
                    frame_count=6,
                    fps=10.0,
                    loop=True,
                ),
                ANIM_THROW: AnimationSheetDefinition(
                    sheet_path=assets_root / "dude_monster" / "Dude_Monster_Throw_4.png",
                    frame_count=4,
                    fps=14.0,
                    loop=False,
                ),
                ANIM_DEATH: AnimationSheetDefinition(
                    sheet_path=assets_root / "dude_monster" / "Dude_Monster_Death_8.png",
                    frame_count=8,
                    fps=10.0,
                    loop=False,
                ),
            },
        ),
        "owlet_monster": CharacterDefinition(
            character_id="owlet_monster",
            display_name="Owlet Monster",
            portrait_path=assets_root / "owlet_monster" / "Owlet_Monster.png",
            animations={
                ANIM_IDLE: AnimationSheetDefinition(
                    sheet_path=assets_root / "owlet_monster" / "Owlet_Monster_Idle_4.png",
                    frame_count=4,
                    fps=6.0,
                    loop=True,
                ),
                ANIM_WALK: AnimationSheetDefinition(
                    sheet_path=assets_root / "owlet_monster" / "Owlet_Monster_Walk_6.png",
                    frame_count=6,
                    fps=10.0,
                    loop=True,
                ),
                ANIM_THROW: AnimationSheetDefinition(
                    sheet_path=assets_root / "owlet_monster" / "Owlet_Monster_Throw_4.png",
                    frame_count=4,
                    fps=14.0,
                    loop=False,
                ),
                ANIM_DEATH: AnimationSheetDefinition(
                    sheet_path=assets_root / "owlet_monster" / "Owlet_Monster_Death_8.png",
                    frame_count=8,
                    fps=10.0,
                    loop=False,
                ),
            },
        ),
        "pink_monster": CharacterDefinition(
            character_id="pink_monster",
            display_name="Pink Monster",
            portrait_path=assets_root / "pink_monster" / "Pink_Monster.png",
            animations={
                ANIM_IDLE: AnimationSheetDefinition(
                    sheet_path=assets_root / "pink_monster" / "Pink_Monster_Idle_4.png",
                    frame_count=4,
                    fps=6.0,
                    loop=True,
                ),
                ANIM_WALK: AnimationSheetDefinition(
                    sheet_path=assets_root / "pink_monster" / "Pink_Monster_Walk_6.png",
                    frame_count=6,
                    fps=10.0,
                    loop=True,
                ),
                ANIM_THROW: AnimationSheetDefinition(
                    sheet_path=assets_root / "pink_monster" / "Pink_Monster_Throw_4.png",
                    frame_count=4,
                    fps=14.0,
                    loop=False,
                ),
                ANIM_DEATH: AnimationSheetDefinition(
                    sheet_path=assets_root / "pink_monster" / "Pink_Monster_Death_8.png",
                    frame_count=8,
                    fps=10.0,
                    loop=False,
                ),
            },
        ),
    }


def _scale_frame(frame: pygame.Surface, scale: float) -> pygame.Surface:
    if scale == 1.0:
        return frame

    width, height = frame.get_size()
    scaled_size = (max(1, int(round(width * scale))), max(1, int(round(height * scale))))
    return pygame.transform.smoothscale(frame, scaled_size)


def _resolve_default_character_id(definitions: dict[str, CharacterDefinition]) -> str:
    if DEFAULT_CHARACTER_ID in definitions:
        return DEFAULT_CHARACTER_ID
    if definitions:
        return next(iter(definitions))
    return DEFAULT_CHARACTER_ID

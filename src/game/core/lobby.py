from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import TypeVar

from game.render.characters import get_character_definitions
from game.render.map_loader import DEFAULT_MAPS_ROOT

T = TypeVar("T")

MAP_NAME_OVERRIDES = {
    "ashland_map": "Ashland",
}


@dataclass(frozen=True, slots=True)
class CharacterOption:
    character_id: str
    display_name: str


@dataclass(frozen=True, slots=True)
class MapOption:
    map_id: str
    display_name: str


def list_character_options() -> list[CharacterOption]:
    definitions = get_character_definitions()
    options = [
        CharacterOption(character_id=character_id, display_name=definition.display_name)
        for character_id, definition in definitions.items()
    ]
    return sorted(options, key=lambda option: option.display_name.lower())


def list_map_options(maps_root: Path = DEFAULT_MAPS_ROOT) -> list[MapOption]:
    if not maps_root.exists():
        return []

    options: list[MapOption] = []
    for map_dir in sorted(path for path in maps_root.iterdir() if path.is_dir()):
        layer_files = sorted(map_dir.glob("layer*.py"))
        if not layer_files:
            continue
        map_id = map_dir.name
        display_name = MAP_NAME_OVERRIDES.get(map_id, map_id.replace("_", " ").title())
        options.append(MapOption(map_id=map_id, display_name=display_name))

    return options


def resolve_selected_id(
    options: list[T],
    selected_id: str,
    *,
    id_getter: Callable[[T], str],
) -> str:
    if not options:
        return ""

    valid_ids = {id_getter(option) for option in options}
    if selected_id in valid_ids:
        return selected_id
    return id_getter(options[0])


def cycle_selected_id(
    options: list[T],
    selected_id: str,
    *,
    id_getter: Callable[[T], str],
    step: int,
) -> str:
    if not options:
        return ""
    if len(options) == 1:
        return id_getter(options[0])

    ids = [id_getter(option) for option in options]
    if selected_id not in ids:
        return ids[0]
    index = ids.index(selected_id)
    return ids[(index + step) % len(ids)]

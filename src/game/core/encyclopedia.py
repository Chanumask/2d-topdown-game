from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EncyclopediaEntry:
    entry_id: str
    term: str
    explanation: str
    sort_order: int = 0


ENCYCLOPEDIA_ENTRIES: tuple[EncyclopediaEntry, ...] = (
    EncyclopediaEntry(
        entry_id="active_ability",
        term="Active Ability",
        explanation=(
            "A pre-run equipped player ability that you trigger manually. "
            "It has its own Cooldown and one chosen Variant."
        ),
    ),
    EncyclopediaEntry(
        entry_id="area_of_effect",
        term="Area of Effect",
        explanation=(
            "An effect that applies inside a circular area instead of hitting "
            "just one target."
        ),
    ),
    EncyclopediaEntry(
        entry_id="blessing",
        term="Blessing",
        explanation=(
            "A special drop that can appear instead of a coin when an enemy dies "
            "(2% chance by default). Picking it up triggers an Instant effect or "
            "adds a Run Boon."
        ),
    ),
    EncyclopediaEntry(
        entry_id="blocking_tile",
        term="Blocking Tile",
        explanation=(
            "A tile marked as blocked in the map data. Players and most ground "
            "enemies cannot move through it."
        ),
    ),
    EncyclopediaEntry(
        entry_id="coin",
        term="Coin",
        explanation=(
            "A pickup dropped by enemies. Collecting it increases the current run "
            "coin total, which is added to your Profile after the Run ends."
        ),
    ),
    EncyclopediaEntry(
        entry_id="coin_drop",
        term="Coin Drop",
        explanation=(
            "The number of coins an enemy creates when it dies, unless that death "
            "rolls a Blessing instead."
        ),
    ),
    EncyclopediaEntry(
        entry_id="cooldown",
        term="Cooldown",
        explanation=(
            "The minimum time that must pass before the same action can be used "
            "again."
        ),
    ),
    EncyclopediaEntry(
        entry_id="damage",
        term="Damage",
        explanation="The amount of Health removed by an attack or harmful effect.",
    ),
    EncyclopediaEntry(
        entry_id="difficulty",
        term="Difficulty",
        explanation=(
            "A run scaling value that starts at 1.0 and rises by 1.0 every 60 "
            "seconds. It unlocks enemies with higher minimum values, shortens "
            "spawn intervals, and adds enemy health and speed."
        ),
    ),
    EncyclopediaEntry(
        entry_id="elite",
        term="Elite",
        explanation=(
            "A stronger enemy tier with larger visuals, higher coin rewards, and "
            "more dangerous stats or abilities."
        ),
    ),
    EncyclopediaEntry(
        entry_id="enemy",
        term="Enemy",
        explanation=(
            "A hostile unit spawned during a Run. Enemies can move, deal Touch "
            "Damage, and some use abilities or Projectiles."
        ),
    ),
    EncyclopediaEntry(
        entry_id="enemy_stats",
        term="Enemy Stats",
        explanation=(
            "The main numbers that define an enemy: maximum Health, speed, Touch "
            "Damage, coin drop value, and collision size."
        ),
    ),
    EncyclopediaEntry(
        entry_id="flying",
        term="Flying",
        explanation=(
            "An enemy trait for units that are not constrained by ground-only "
            "movement rules."
        ),
    ),
    EncyclopediaEntry(
        entry_id="heal",
        term="Heal",
        explanation="Restore lost Health, but never above maximum Health.",
    ),
    EncyclopediaEntry(
        entry_id="health",
        term="Health",
        explanation="How much Damage a unit can take before it dies.",
    ),
    EncyclopediaEntry(
        entry_id="instant",
        term="Instant",
        explanation=(
            "A Blessing category whose effect happens immediately when the "
            "Blessing is collected."
        ),
    ),
    EncyclopediaEntry(
        entry_id="invulnerability",
        term="Invulnerability",
        explanation="A temporary state where incoming Damage is reduced to 0.",
    ),
    EncyclopediaEntry(
        entry_id="layer",
        term="Layer",
        explanation=(
            "One grid inside a Map. Layers are stacked to build the final terrain, "
            "visual objects, and blocking data."
        ),
    ),
    EncyclopediaEntry(
        entry_id="magnet",
        term="Magnet",
        explanation=(
            "A persistent Upgrade that increases Pickup Radius for coins and "
            "Blessings."
        ),
    ),
    EncyclopediaEntry(
        entry_id="map",
        term="Map",
        explanation=(
            "The fixed play area used for a Run. A map contains one or more Layers "
            "plus blocking data."
        ),
    ),
    EncyclopediaEntry(
        entry_id="pickup_radius",
        term="Pickup Radius",
        explanation=(
            "The distance from the player at which coins and Blessings are "
            "collected automatically."
        ),
    ),
    EncyclopediaEntry(
        entry_id="profile",
        term="Profile",
        explanation=(
            "Your saved persistent data, including currency, Upgrades, settings, "
            "and discovered entries."
        ),
    ),
    EncyclopediaEntry(
        entry_id="projectile",
        term="Projectile",
        explanation=(
            "A moving attack entity with speed, Damage, size, and an expiration "
            "time. Rocks and enemy shots both use Projectiles."
        ),
    ),
    EncyclopediaEntry(
        entry_id="run",
        term="Run",
        explanation=(
            "One game attempt, from entering a Map until game over. Coins earned "
            "during the run are added to your Profile afterward."
        ),
    ),
    EncyclopediaEntry(
        entry_id="run_boon",
        term="Run Boon",
        explanation=(
            "A Blessing category for passive effects that last until the current "
            "Run ends and stack when collected again."
        ),
    ),
    EncyclopediaEntry(
        entry_id="shop",
        term="Shop",
        explanation=(
            "The menu where you spend Profile currency on persistent Upgrades "
            "between runs."
        ),
    ),
    EncyclopediaEntry(
        entry_id="spawn_rate",
        term="Spawn Rate",
        explanation=(
            "How often new enemies appear. In this game, the time between spawns "
            "gets shorter as the Run continues."
        ),
    ),
    EncyclopediaEntry(
        entry_id="tileset",
        term="Tileset",
        explanation="The source image file a Layer uses to draw its map tiles.",
    ),
    EncyclopediaEntry(
        entry_id="touch_damage",
        term="Touch Damage",
        explanation="Damage dealt when an enemy physically collides with the player.",
    ),
    EncyclopediaEntry(
        entry_id="upgrade",
        term="Upgrade",
        explanation=(
            "A persistent bonus bought in the Shop and stored in your Profile. "
            "Its effects are applied when a Run starts."
        ),
    ),
    EncyclopediaEntry(
        entry_id="variant",
        term="Variant",
        explanation=(
            "One of three predefined versions of an Active Ability. A Variant "
            "changes values like damage, duration, range, healing, or cooldown."
        ),
    ),
)


def list_encyclopedia_entries() -> list[EncyclopediaEntry]:
    return sorted(
        ENCYCLOPEDIA_ENTRIES,
        key=lambda entry: (entry.term.lower(), entry.entry_id),
    )

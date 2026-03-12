from __future__ import annotations

import random
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BlessingDefinition:
    blessing_id: str
    display_name: str
    description: str
    icon_path: str
    animated_effect_id: str | None = None
    has_behavior_vfx: bool = False


BLESSING_COIN_VACUUM = "coin_vacuum"
BLESSING_FULL_HEAL = "full_heal"
BLESSING_ENEMY_CLEAR = "enemy_clear"
BLESSING_DAMAGE_AURA = "damage_aura"
BLESSING_VFX_FULL_HEAL = "blessing_full_heal_green"
BLESSING_VFX_ENEMY_CLEAR = "blessing_enemy_clear_red"
BLESSING_VFX_DAMAGE_AURA = "blessing_damage_aura_blue"


BLESSING_CATALOG: dict[str, BlessingDefinition] = {
    BLESSING_COIN_VACUUM: BlessingDefinition(
        blessing_id=BLESSING_COIN_VACUUM,
        display_name="Coin Vacuum",
        description="Collect all coins currently on the map instantly.",
        icon_path="assets/effects/blessings/coin_vacuum.png",
        has_behavior_vfx=True,
    ),
    BLESSING_FULL_HEAL: BlessingDefinition(
        blessing_id=BLESSING_FULL_HEAL,
        display_name="Full Heal",
        description="Restore all players to maximum health.",
        icon_path="assets/effects/blessings/full_heal.png",
        animated_effect_id=BLESSING_VFX_FULL_HEAL,
    ),
    BLESSING_ENEMY_CLEAR: BlessingDefinition(
        blessing_id=BLESSING_ENEMY_CLEAR,
        display_name="Enemy Clear",
        description="Remove all alive enemies and trigger their normal drops.",
        icon_path="assets/effects/blessings/enemy_clear.png",
        animated_effect_id=BLESSING_VFX_ENEMY_CLEAR,
    ),
    BLESSING_DAMAGE_AURA: BlessingDefinition(
        blessing_id=BLESSING_DAMAGE_AURA,
        display_name="Damage Aura",
        description="Emit a damaging aura around the player for 30 seconds.",
        icon_path="assets/effects/blessings/damage_aura.png",
        animated_effect_id=BLESSING_VFX_DAMAGE_AURA,
    ),
}


def list_blessings() -> list[BlessingDefinition]:
    return list(BLESSING_CATALOG.values())


def get_blessing(blessing_id: str) -> BlessingDefinition | None:
    return BLESSING_CATALOG.get(blessing_id)


def random_blessing_id(rng: random.Random) -> str | None:
    if not BLESSING_CATALOG:
        return None
    return rng.choice(list(BLESSING_CATALOG))

from __future__ import annotations

import random
from dataclasses import dataclass
from enum import StrEnum


class BlessingCategory(StrEnum):
    INSTANT = "instant"
    RUN_BOON = "run_boon"


def blessing_category_label(category: BlessingCategory) -> str:
    if category is BlessingCategory.RUN_BOON:
        return "Run Boon"
    return "Instant"


@dataclass(frozen=True, slots=True)
class BlessingDefinition:
    blessing_id: str
    display_name: str
    description: str
    icon_path: str
    category: BlessingCategory = BlessingCategory.INSTANT
    animated_effect_id: str | None = None
    has_behavior_vfx: bool = False
    coin_heal_on_pickup: int = 0


BLESSING_COIN_VACUUM = "coin_vacuum"
BLESSING_SACRED_RENEWAL = "sacred_renewal"
BLESSING_DIVINE_PURGE = "divine_purge"
BLESSING_DAMAGE_AURA = "damage_aura"
BLESSING_HEALING_COIN = "healing_coin"
BLESSING_VFX_SACRED_RENEWAL = "blessing_sacred_renewal_green"
BLESSING_VFX_DIVINE_PURGE = "blessing_divine_purge_red"
BLESSING_VFX_DAMAGE_AURA = "blessing_damage_aura_blue"


BLESSING_CATALOG: dict[str, BlessingDefinition] = {
    BLESSING_COIN_VACUUM: BlessingDefinition(
        blessing_id=BLESSING_COIN_VACUUM,
        display_name="Coin Vacuum",
        description="Collect all coins currently on the map instantly.",
        icon_path="assets/blessings/coin_vacuum.png",
        category=BlessingCategory.INSTANT,
        has_behavior_vfx=True,
    ),
    BLESSING_SACRED_RENEWAL: BlessingDefinition(
        blessing_id=BLESSING_SACRED_RENEWAL,
        display_name="Sacred Renewal",
        description="Restore all players to maximum health.",
        icon_path="assets/blessings/sacred_renewal.png",
        category=BlessingCategory.INSTANT,
        animated_effect_id=BLESSING_VFX_SACRED_RENEWAL,
    ),
    BLESSING_DIVINE_PURGE: BlessingDefinition(
        blessing_id=BLESSING_DIVINE_PURGE,
        display_name="Divine Purge",
        description="Remove all alive enemies and trigger their normal drops.",
        icon_path="assets/blessings/divine_purge.png",
        category=BlessingCategory.INSTANT,
        animated_effect_id=BLESSING_VFX_DIVINE_PURGE,
    ),
    BLESSING_DAMAGE_AURA: BlessingDefinition(
        blessing_id=BLESSING_DAMAGE_AURA,
        display_name="Damage Aura",
        description="Emit a damaging aura around the player for 30 seconds.",
        icon_path="assets/blessings/damage_aura.png",
        category=BlessingCategory.INSTANT,
        animated_effect_id=BLESSING_VFX_DAMAGE_AURA,
    ),
    BLESSING_HEALING_COIN: BlessingDefinition(
        blessing_id=BLESSING_HEALING_COIN,
        display_name="Healing Coin",
        description="Heal 1 HP whenever you collect a coin this run. Stacks.",
        icon_path="assets/blessings/healing_coin.png",
        category=BlessingCategory.RUN_BOON,
        coin_heal_on_pickup=1,
    ),
}


def list_blessings() -> list[BlessingDefinition]:
    category_order = {
        BlessingCategory.INSTANT: 0,
        BlessingCategory.RUN_BOON: 1,
    }
    return sorted(
        BLESSING_CATALOG.values(),
        key=lambda blessing: (
            category_order.get(blessing.category, 99),
            blessing.display_name.lower(),
            blessing.blessing_id,
        ),
    )


def get_blessing(blessing_id: str) -> BlessingDefinition | None:
    return BLESSING_CATALOG.get(blessing_id)


def random_blessing_id(rng: random.Random) -> str | None:
    if not BLESSING_CATALOG:
        return None
    return rng.choice(list(BLESSING_CATALOG))

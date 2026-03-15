from game.core.enemies import (
    ENEMY_ABILITY_DELAYED_EXPLOSION_ON_TOUCH,
    ENEMY_VFX_FLOATING_EYE_PURPLE,
    EnemyAbilityDefinition,
    EnemyProfile,
    EnemyStats,
    EnemyTier,
)

CRIMSON_IMP = EnemyProfile(
    profile_id="crimson_imp",
    display_name="Crimson Imp",
    tier=EnemyTier.NORMAL,
    stats=EnemyStats(
        max_health=30,
        speed=72.0,
        touch_damage=10,
        coin_drop_value=1,
        radius=12.0,
    ),
    abilities=(),
    passive_influences=(),
    hooks=(),
    tags=("ground", "melee"),
    spawn_weight=1.0,
)

FLOATING_EYE_SELF_DESTRUCT = EnemyAbilityDefinition(
    ability_id=ENEMY_ABILITY_DELAYED_EXPLOSION_ON_TOUCH,
    display_name="Volatile Charge",
    description="Arms on player contact or lethal damage and explodes after a delay.",
    trigger_on_player_touch=True,
    arming_delay_seconds=1,
    explosion_damage=50,
    explosion_radius=48.0,
    loop_effect_id=ENEMY_VFX_FLOATING_EYE_PURPLE,
)

FLOATING_EYE = EnemyProfile(
    profile_id="floating_eye",
    display_name="Floating Eye",
    tier=EnemyTier.NORMAL,
    stats=EnemyStats(
        max_health=22,
        speed=84.0,
        touch_damage=10,
        coin_drop_value=1,
        radius=12.0,
    ),
    abilities=(FLOATING_EYE_SELF_DESTRUCT,),
    passive_influences=(),
    hooks=(),
    tags=("flying",),
    spawn_weight=0.2,
)

CRIMSON_IMP_PROFILE_ID = CRIMSON_IMP.profile_id

ENEMY_PROFILES: dict[str, EnemyProfile] = {
    CRIMSON_IMP.profile_id: CRIMSON_IMP,
    FLOATING_EYE.profile_id: FLOATING_EYE,
}


def list_enemy_profiles() -> list[EnemyProfile]:
    return sorted(ENEMY_PROFILES.values(), key=lambda profile: profile.display_name.lower())


def get_enemy_profiles() -> dict[str, EnemyProfile]:
    return ENEMY_PROFILES.copy()


def get_enemy_profile(profile_id: str) -> EnemyProfile | None:
    return ENEMY_PROFILES.get(profile_id)


def get_fallback_enemy_radius() -> float:
    return float(CRIMSON_IMP.stats.radius)

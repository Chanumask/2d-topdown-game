from game.core.enemies import EnemyProfile, EnemyStats, EnemyTier

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

CRIMSON_IMP_PROFILE_ID = CRIMSON_IMP.profile_id

ENEMY_PROFILES: dict[str, EnemyProfile] = {
    CRIMSON_IMP.profile_id: CRIMSON_IMP,
}


def get_enemy_profiles() -> dict[str, EnemyProfile]:
    return ENEMY_PROFILES.copy()


def get_enemy_profile(profile_id: str) -> EnemyProfile | None:
    return ENEMY_PROFILES.get(profile_id)


def get_fallback_enemy_radius() -> float:
    return float(CRIMSON_IMP.stats.radius)

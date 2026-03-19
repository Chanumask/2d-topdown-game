from game.audio.audio_assets import SFX_ENEMY_ELITE_SPAWN
from game.core.enemies import (
    ENEMY_ABILITY_DELAYED_EXPLOSION_ON_TOUCH,
    ENEMY_ABILITY_RANGED_SHOT,
    ENEMY_VFX_ELITE_BURST_PROJECTILE_PURPLE,
    ENEMY_VFX_FLOATING_EYE_PURPLE,
    ENEMY_VFX_WARPED_SKULL_PROJECTILE_PURPLE,
    EnemyAbilityDefinition,
    EnemyInfluenceDefinition,
    EnemyProfile,
    EnemyStatModifier,
    EnemyStats,
    EnemyTier,
)

ELITE_MIN_DIFFICULTY_FACTOR = 2.0

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
    sprite_asset_name="CrimsonImp.png",
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
    sprite_asset_name="FloatingEye.png",
)

WARPED_SKULL_RANGED_SHOT = EnemyAbilityDefinition(
    ability_id=ENEMY_ABILITY_RANGED_SHOT,
    display_name="Warp Bolt",
    description="Fires a straight projectile toward players within range.",
    attack_interval_seconds=4.0,
    attack_range=350.0,
    projectile_speed=200.0,
    projectile_damage=25,
    projectile_ttl_seconds=2.5,
    projectile_radius=4.0,
    projectile_effect_id=ENEMY_VFX_WARPED_SKULL_PROJECTILE_PURPLE,
)

POINTED_DEMONSPAWN_BURST_SHOT = EnemyAbilityDefinition(
    ability_id=ENEMY_ABILITY_RANGED_SHOT,
    display_name="Void Barrage",
    description="Fires an 8-way burst of purple projectiles.",
    attack_interval_seconds=WARPED_SKULL_RANGED_SHOT.attack_interval_seconds,
    attack_range=WARPED_SKULL_RANGED_SHOT.attack_range,
    projectile_speed=WARPED_SKULL_RANGED_SHOT.projectile_speed,
    projectile_damage=WARPED_SKULL_RANGED_SHOT.projectile_damage,
    projectile_ttl_seconds=WARPED_SKULL_RANGED_SHOT.projectile_ttl_seconds,
    projectile_radius=WARPED_SKULL_RANGED_SHOT.projectile_radius,
    projectile_effect_id=ENEMY_VFX_ELITE_BURST_PROJECTILE_PURPLE,
    projectile_burst_angles_degrees=(0.0, 45.0, 90.0, 135.0, 180.0, 225.0, 270.0, 315.0),
)

NEFARIOUS_SCAMP_SPEED_AURA = EnemyInfluenceDefinition(
    influence_id="nefarious_scamp_speed_aura",
    radius=160.0,
    stat_modifier=EnemyStatModifier(speed_multiplier=1.25),
)

WARPED_SKULL = EnemyProfile(
    profile_id="warped_skull",
    display_name="Warped Skull",
    tier=EnemyTier.NORMAL,
    stats=EnemyStats(
        max_health=15,
        speed=66.0,
        touch_damage=10,
        coin_drop_value=1,
        radius=11.0,
    ),
    abilities=(WARPED_SKULL_RANGED_SHOT,),
    passive_influences=(),
    hooks=(),
    tags=("flying", "ranged"),
    spawn_weight=0.1,
    sprite_asset_name="WarpedSkull.png",
)

CLAWED_ABOMINATION = EnemyProfile(
    profile_id="clawed_abomination",
    display_name="Clawed Abomination",
    tier=EnemyTier.ELITE,
    stats=EnemyStats(
        max_health=400,
        speed=50.0,
        touch_damage=35,
        coin_drop_value=20,
        radius=24.0,
    ),
    abilities=(),
    passive_influences=(),
    hooks=(),
    tags=("ground", "melee", "elite"),
    spawn_weight=0.03,
    min_difficulty_factor=ELITE_MIN_DIFFICULTY_FACTOR,
    sprite_asset_name="ClawedAbomination.png",
    sprite_pixel_scale=6,
    spawn_sfx_key=SFX_ENEMY_ELITE_SPAWN,
)

POINTED_DEMONSPAWN = EnemyProfile(
    profile_id="pointed_demonspawn",
    display_name="Pointed Demonspawn",
    tier=EnemyTier.ELITE,
    stats=EnemyStats(
        max_health=300,
        speed=50.0,
        touch_damage=35,
        coin_drop_value=20,
        radius=24.0,
    ),
    abilities=(POINTED_DEMONSPAWN_BURST_SHOT,),
    passive_influences=(),
    hooks=(),
    tags=("ground", "ranged", "elite"),
    spawn_weight=0.03,
    min_difficulty_factor=ELITE_MIN_DIFFICULTY_FACTOR,
    sprite_asset_name="PointedDemonspawn.png",
    sprite_pixel_scale=6,
    spawn_sfx_key=SFX_ENEMY_ELITE_SPAWN,
)

NEFARIOUS_SCAMP = EnemyProfile(
    profile_id="nefarious_scamp",
    display_name="Nefarious Scamp",
    tier=EnemyTier.ELITE,
    stats=EnemyStats(
        max_health=150,
        speed=80.0,
        touch_damage=20,
        coin_drop_value=20,
        radius=24.0,
    ),
    abilities=(),
    passive_influences=(NEFARIOUS_SCAMP_SPEED_AURA,),
    hooks=(),
    tags=("flying", "support", "elite"),
    spawn_weight=0.02,
    min_difficulty_factor=4.0,
    sprite_asset_name="NefariousScamp.png",
    sprite_pixel_scale=4,
    spawn_sfx_key=SFX_ENEMY_ELITE_SPAWN,
)

CRIMSON_IMP_PROFILE_ID = CRIMSON_IMP.profile_id

ENEMY_PROFILES: dict[str, EnemyProfile] = {
    CRIMSON_IMP.profile_id: CRIMSON_IMP,
    FLOATING_EYE.profile_id: FLOATING_EYE,
    WARPED_SKULL.profile_id: WARPED_SKULL,
    CLAWED_ABOMINATION.profile_id: CLAWED_ABOMINATION,
    POINTED_DEMONSPAWN.profile_id: POINTED_DEMONSPAWN,
    NEFARIOUS_SCAMP.profile_id: NEFARIOUS_SCAMP,
}


def list_enemy_profiles() -> list[EnemyProfile]:
    tier_order = {
        EnemyTier.NORMAL: 0,
        EnemyTier.ELITE: 1,
        EnemyTier.BOSS: 2,
    }
    return sorted(
        ENEMY_PROFILES.values(),
        key=lambda profile: (
            tier_order.get(profile.tier, 99),
            profile.display_name.lower(),
            profile.profile_id,
        ),
    )


def get_enemy_profiles() -> dict[str, EnemyProfile]:
    return ENEMY_PROFILES.copy()


def get_enemy_profile(profile_id: str) -> EnemyProfile | None:
    return ENEMY_PROFILES.get(profile_id)


def get_fallback_enemy_radius() -> float:
    return float(CRIMSON_IMP.stats.radius)

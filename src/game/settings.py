from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class GameSettings:
    title: str = "Runner2D Survival Prototype"
    screen_width: int = 960
    screen_height: int = 540
    world_width: float = 960.0
    world_height: float = 540.0
    simulation_hz: int = 60
    max_render_fps: int = 120
    max_catchup_steps: int = 5
    default_player_character_id: str = "dude_monster"

    player_radius: float = 14.0
    player_speed: float = 250.0
    player_max_health: int = 100
    player_touch_iframe_seconds: float = 0.4
    throw_cooldown_seconds: float = 0.2

    enemy_radius: float = 12.0
    enemy_base_speed: float = 72.0
    enemy_base_health: int = 30
    enemy_touch_damage: int = 10

    projectile_radius: float = 4.0
    projectile_speed: float = 460.0
    projectile_damage: int = 15
    projectile_ttl_seconds: float = 1.3

    coin_radius: float = 6.0
    coin_value: int = 1

    spawn_base_interval_seconds: float = 1.8
    spawn_min_interval_seconds: float = 0.45
    spawn_acceleration_per_second: float = 0.015

    background_color: tuple[int, int, int] = (18, 22, 26)
    grid_color: tuple[int, int, int] = (30, 36, 42)
    player_color: tuple[int, int, int] = (80, 170, 255)
    player_aim_color: tuple[int, int, int] = (245, 240, 126)
    enemy_color: tuple[int, int, int] = (245, 104, 104)
    projectile_color: tuple[int, int, int] = (255, 187, 85)
    coin_color: tuple[int, int, int] = (255, 223, 88)
    hud_color: tuple[int, int, int] = (236, 236, 236)

    grid_step: int = 48
    camera_dead_zone_width_ratio: float = 0.5
    camera_dead_zone_height_ratio: float = 0.5


SETTINGS = GameSettings()

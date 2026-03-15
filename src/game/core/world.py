from __future__ import annotations

import math
import random
from dataclasses import dataclass, field

from game.core.blessings import BLESSING_DAMAGE_AURA, random_blessing_id
from game.core.enemies import (
    ENEMY_ABILITY_DELAYED_EXPLOSION_ON_TOUCH,
    ENEMY_ABILITY_RANGED_SHOT,
    EnemyAbilityDefinition,
    EnemySpawnRequest,
)
from game.core.enemy_catalog import get_enemy_profile
from game.core.run_result import RunResult
from game.core.session_state import MatchPhase, SessionState
from game.core.snapshot import WorldSnapshot
from game.core.upgrades import RunModifiers
from game.entities import Blessing, Coin, Enemy, Player, Projectile, Vec2
from game.input.actions import PlayerActions
from game.input.session_actions import SessionActions
from game.settings import GameSettings
from game.systems import (
    BlessingSystem,
    CombatSystem,
    EnemyDirector,
    EnemyNavigationSystem,
    EnemySpawner,
)
from game.systems.collision import circles_overlap, nearest_player


@dataclass(slots=True)
class DamageAuraState:
    remaining_seconds: float
    tick_cooldown_seconds: float = 0.0


@dataclass(slots=True)
class World:
    settings: GameSettings
    world_width: float
    world_height: float
    blocking_grid: tuple[tuple[bool, ...], ...] | None = None
    blocking_tile_size: float = 32.0
    run_modifiers: RunModifiers = field(default_factory=RunModifiers)
    players: dict[str, Player] = field(default_factory=dict)
    enemies: dict[int, Enemy] = field(default_factory=dict)
    projectiles: dict[int, Projectile] = field(default_factory=dict)
    coins: dict[int, Coin] = field(default_factory=dict)
    blessings: dict[int, Blessing] = field(default_factory=dict)
    active_damage_auras: dict[str, DamageAuraState] = field(default_factory=dict)
    coin_vacuum_target_player_id: str | None = None
    coin_vacuum_coin_ids: set[int] = field(default_factory=set)
    tick: int = 0
    simulation_time: float = 0.0
    total_coins_collected: int = 0
    enemies_killed_total: int = 0
    enemies_killed_by_player: dict[str, int] = field(default_factory=dict)
    final_run_result: RunResult | None = None
    session: SessionState = field(default_factory=SessionState)
    spawner: EnemySpawner = field(init=False)
    combat: CombatSystem = field(init=False)
    enemy_director: EnemyDirector = field(init=False)
    navigation: EnemyNavigationSystem = field(init=False)
    blessing_system: BlessingSystem = field(init=False)
    _rng: random.Random = field(init=False, repr=False)
    _next_entity_id: int = field(init=False, repr=False)
    _next_vfx_event_id: int = field(init=False, repr=False)
    _pending_actions: dict[str, PlayerActions] = field(init=False, repr=False)
    _pending_session_actions: dict[str, SessionActions] = field(init=False, repr=False)
    _pending_vfx_events: list[dict[str, object]] = field(init=False, repr=False)
    _pending_profile_progress_events: list[dict[str, str]] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self._rng = random.Random()
        self._next_entity_id = 1
        self._next_vfx_event_id = 1
        self._pending_actions = {}
        self._pending_session_actions = {}
        self._pending_vfx_events = []
        self._pending_profile_progress_events = []

        self.spawner = EnemySpawner(
            rng=self._rng,
            base_interval_seconds=self.settings.spawn_base_interval_seconds,
            min_interval_seconds=self.settings.spawn_min_interval_seconds,
            acceleration_per_second=self.settings.spawn_acceleration_per_second,
        )
        self.enemy_director = EnemyDirector(rng=self._rng)
        self.blessing_system = BlessingSystem()
        self.navigation = EnemyNavigationSystem(
            repath_interval_seconds=self.settings.enemy_nav_repath_interval_seconds,
            max_path_requests_per_tick=self.settings.enemy_nav_max_path_requests_per_tick,
            max_search_nodes=self.settings.enemy_nav_max_search_nodes,
            stuck_seconds=self.settings.enemy_nav_stuck_seconds,
            min_progress_per_second=self.settings.enemy_nav_min_progress_per_second,
        )
        self.combat = CombatSystem(
            projectile_speed=max(1.0, self.settings.projectile_speed),
            projectile_damage=max(
                1,
                self.settings.projectile_damage + self.run_modifiers.projectile_damage_bonus,
            ),
            projectile_ttl_seconds=self.settings.projectile_ttl_seconds,
            projectile_radius=self.settings.projectile_radius,
        )

    def add_player(self, player_id: str, character_id: str | None = None) -> None:
        if player_id in self.players:
            return

        spawn = Vec2(self.world_width * 0.5, self.world_height * 0.5)
        spawn = self._nearest_walkable_position(spawn, self.settings.player_radius)
        resolved_character_id = character_id or self.settings.default_player_character_id
        base_health = self.settings.player_max_health + self.run_modifiers.player_max_health_bonus
        base_speed = self.settings.player_speed + self.run_modifiers.player_speed_bonus
        throw_cooldown = max(
            0.05,
            self.settings.throw_cooldown_seconds - self.run_modifiers.throw_cooldown_reduction,
        )
        pickup_radius = max(
            self.settings.player_radius,
            self.settings.player_radius + self.run_modifiers.coin_pickup_radius_bonus,
        )

        self.players[player_id] = Player(
            entity_id=self._allocate_entity_id(),
            player_id=player_id,
            character_id=resolved_character_id,
            position=spawn,
            radius=self.settings.player_radius,
            speed=base_speed,
            max_health=base_health,
            health=base_health,
            coin_pickup_radius=pickup_radius,
            aim_position=spawn.copy(),
            throw_cooldown_seconds=throw_cooldown,
            damage_iframe_seconds=self.settings.player_touch_iframe_seconds,
        )
        self.enemies_killed_by_player.setdefault(player_id, 0)

    def ensure_min_bounds(self, min_width: float, min_height: float) -> None:
        updated_width = max(self.world_width, float(min_width))
        updated_height = max(self.world_height, float(min_height))
        if updated_width == self.world_width and updated_height == self.world_height:
            return

        self.world_width = updated_width
        self.world_height = updated_height
        self._clamp_entities_to_world_bounds()

    def apply_actions(self, player_id: str, actions: PlayerActions) -> None:
        self._pending_actions[player_id] = actions

    def apply_action_payload(self, player_id: str, payload: dict[str, object]) -> None:
        self.apply_actions(player_id, PlayerActions.from_dict(payload))

    def apply_session_actions(self, player_id: str, actions: SessionActions) -> None:
        self._pending_session_actions[player_id] = actions

    def apply_session_payload(self, player_id: str, payload: dict[str, object]) -> None:
        self.apply_session_actions(player_id, SessionActions.from_dict(payload))

    def update(self, dt: float) -> None:
        self.tick += 1
        self._pending_vfx_events.clear()
        self._apply_session_actions()

        if self.session.phase is MatchPhase.GAME_OVER:
            self._pending_actions.clear()
            if self.final_run_result is None:
                self.final_run_result = self.build_run_result()
            return

        if self.session.phase is MatchPhase.PAUSED:
            self._pending_actions.clear()
            self._maybe_start_resume_countdown()
            return

        if self.session.phase is MatchPhase.RESUME_COUNTDOWN:
            self._pending_actions.clear()
            self.session.countdown_remaining = max(0.0, self.session.countdown_remaining - dt)
            if self.session.countdown_remaining <= 0.0:
                self.session.resume_running()
            return

        # RUNNING and PAUSE_COUNTDOWN both keep gameplay simulation active.
        self.simulation_time += dt
        self._apply_player_actions()
        for player in self.players.values():
            previous_position = player.position.copy()
            player.update(dt, self.world_width, self.world_height)
            self._resolve_blocking_for_entity(player, previous_position)

        self.enemy_director.update(self, dt)
        self.spawner.update(self, dt)
        self._update_enemy_ai(dt)

        self.combat.update_projectiles(self, dt)
        self.combat.resolve(self)
        self._update_enemy_abilities(dt)
        self._update_coin_vacuum(dt)
        self._update_damage_auras(dt)

        self._collect_coins()
        self._collect_blessings()
        self._cleanup_dead_entities()
        self._update_game_over_state()

        if self.session.phase is MatchPhase.PAUSE_COUNTDOWN:
            self.session.countdown_remaining = max(0.0, self.session.countdown_remaining - dt)
            if self.session.countdown_remaining <= 0.0:
                self.session.start_paused()

    @property
    def difficulty_factor(self) -> float:
        return 1.0 + (self.simulation_time / 60.0)

    @property
    def current_spawn_interval(self) -> float:
        return self.spawner.current_interval(
            self.simulation_time,
            interval_multiplier=self.enemy_director.current_spawn_interval_multiplier(self),
        )

    def snapshot(self) -> WorldSnapshot:
        players = [self.players[player_id].to_dict() for player_id in sorted(self.players)]
        enemies = [self.enemies[enemy_id].to_dict() for enemy_id in sorted(self.enemies)]
        projectiles = [
            self.projectiles[projectile_id].to_dict() for projectile_id in sorted(self.projectiles)
        ]
        coins = [self.coins[coin_id].to_dict() for coin_id in sorted(self.coins)]
        blessings = [
            self.blessings[blessing_id].to_dict() for blessing_id in sorted(self.blessings)
        ]
        active_blessings = [
            {
                "player_id": player_id,
                "blessing_id": BLESSING_DAMAGE_AURA,
                "remaining_seconds": aura.remaining_seconds,
                "radius": float(self.settings.damage_aura_radius),
            }
            for player_id, aura in sorted(self.active_damage_auras.items())
            if aura.remaining_seconds > 0.0
        ]
        vfx_events = list(self._pending_vfx_events)

        score = {
            "total_run_coins": self.total_coins_collected,
            "run_coins_by_player": {
                player_id: self.players[player_id].coins for player_id in sorted(self.players)
            },
            "enemies_killed_total": self.enemies_killed_total,
            "enemies_killed_by_player": {
                player_id: self.enemies_killed_by_player.get(player_id, 0)
                for player_id in sorted(self.players)
            },
        }
        difficulty = {
            "factor": self.difficulty_factor,
            "spawn_interval_seconds": self.current_spawn_interval,
        }

        player_ids = set(self.players)
        session_payload = self.session.to_dict(player_ids)

        return WorldSnapshot(
            tick=self.tick,
            simulation_time=self.simulation_time,
            run_state=self.session.phase.value,
            world={"width": self.world_width, "height": self.world_height},
            session=session_payload,
            players=players,
            enemies=enemies,
            projectiles=projectiles,
            coins=coins,
            blessings=blessings,
            active_blessings=active_blessings,
            vfx_events=vfx_events,
            score=score,
            difficulty=difficulty,
        )

    def to_dict(self) -> dict[str, object]:
        return self.snapshot().to_dict()

    def build_run_result(self) -> RunResult:
        players = sorted(self.players)
        return RunResult(
            survival_time_seconds=self.simulation_time,
            total_run_coins=self.total_coins_collected,
            coins_by_player={player_id: self.players[player_id].coins for player_id in players},
            enemies_killed_total=self.enemies_killed_total,
            enemies_killed_by_player={
                player_id: self.enemies_killed_by_player.get(player_id, 0) for player_id in players
            },
            players=players,
            tick=self.tick,
            simulation_time=self.simulation_time,
        )

    def get_run_result(self) -> RunResult | None:
        if self.final_run_result is None and self.session.phase is MatchPhase.GAME_OVER:
            self.final_run_result = self.build_run_result()
        return self.final_run_result

    def spawn_enemy(self, position: Vec2, profile_id: str | None = None) -> None:
        spawn_request: EnemySpawnRequest = self.enemy_director.build_spawn_request(
            self,
            profile_id=profile_id,
        )
        spawn_position = self._nearest_walkable_position(position, spawn_request.stats.radius)
        enemy = Enemy(
            entity_id=self._allocate_entity_id(),
            position=spawn_position,
            radius=spawn_request.stats.radius,
            profile_id=spawn_request.profile_id,
            tier=spawn_request.tier.value,
            tags=spawn_request.tags,
            base_radius=spawn_request.stats.radius,
            base_speed=spawn_request.stats.speed,
            base_max_health=spawn_request.stats.max_health,
            base_touch_damage=spawn_request.stats.touch_damage,
            base_coin_drop_value=spawn_request.stats.coin_drop_value,
            speed=spawn_request.stats.speed,
            max_health=spawn_request.stats.max_health,
            health=spawn_request.stats.max_health,
            touch_damage=spawn_request.stats.touch_damage,
            coin_drop_value=spawn_request.stats.coin_drop_value,
        )
        self.enemies[enemy.entity_id] = enemy
        self._queue_profile_progress_event(kind="enemy", entry_id=spawn_request.profile_id)
        self.enemy_director.on_enemy_spawn(self, enemy)

    def spawn_projectile(
        self,
        position: Vec2,
        velocity: Vec2,
        damage: int,
        ttl_seconds: float,
        radius: float,
        owner_player_id: str = "",
        source_faction: str = "player",
        projectile_effect_id: str | None = None,
    ) -> None:
        projectile = Projectile(
            entity_id=self._allocate_entity_id(),
            position=position,
            radius=radius,
            owner_player_id=owner_player_id,
            source_faction=source_faction,
            projectile_effect_id=projectile_effect_id,
            velocity=velocity,
            damage=damage,
            ttl_seconds=ttl_seconds,
        )
        self.projectiles[projectile.entity_id] = projectile

    def spawn_coin(self, position: Vec2, value: int) -> None:
        coin = Coin(
            entity_id=self._allocate_entity_id(),
            position=position,
            radius=self.settings.coin_radius,
            value=value,
        )
        self.coins[coin.entity_id] = coin

    def spawn_blessing(self, position: Vec2, blessing_id: str) -> None:
        blessing = Blessing(
            entity_id=self._allocate_entity_id(),
            position=position,
            radius=self.settings.blessing_radius,
            blessing_id=blessing_id,
        )
        self.blessings[blessing.entity_id] = blessing

    def emit_world_vfx(self, effect_id: str, position: Vec2) -> None:
        if not effect_id:
            return

        event_payload = {
            "event_id": self._next_vfx_event_id,
            "effect_id": effect_id,
            "position": position.to_dict(),
        }
        self._next_vfx_event_id += 1
        self._pending_vfx_events.append(event_payload)

    def consume_profile_progress_events(self) -> list[dict[str, str]]:
        events = list(self._pending_profile_progress_events)
        self._pending_profile_progress_events.clear()
        return events

    def activate_coin_vacuum(self, collector_player_id: str) -> None:
        collector = self.players.get(collector_player_id)
        if collector is None or not collector.alive:
            return

        self.coin_vacuum_target_player_id = collector_player_id
        self.coin_vacuum_coin_ids = {coin_id for coin_id, coin in self.coins.items() if coin.alive}

    def activate_damage_aura(self, collector_player_id: str) -> None:
        collector = self.players.get(collector_player_id)
        if collector is None or not collector.alive:
            return

        self.active_damage_auras[collector_player_id] = DamageAuraState(
            remaining_seconds=float(self.settings.damage_aura_duration_seconds),
            tick_cooldown_seconds=max(0.05, float(self.settings.damage_aura_tick_interval_seconds)),
        )

    def defeat_enemy(self, enemy: Enemy, killer_player_id: str | None) -> None:
        self.register_enemy_kill(killer_player_id)
        self._drop_enemy_reward(position=enemy.position.copy(), coin_value=enemy.coin_drop_value)
        self.enemy_director.on_enemy_death(self, enemy)
        enemy.clear_ability_state()
        enemy.health = 0
        enemy.alive = False

    def register_enemy_kill(self, killer_player_id: str | None) -> None:
        self.enemies_killed_total += 1
        if killer_player_id is None:
            return

        self.enemies_killed_by_player.setdefault(killer_player_id, 0)
        self.enemies_killed_by_player[killer_player_id] += 1

    def _drop_enemy_reward(self, position: Vec2, coin_value: int) -> None:
        if self._maybe_spawn_blessing_drop(position):
            return
        self.spawn_coin(position=position, value=coin_value)

    def _maybe_spawn_blessing_drop(self, position: Vec2) -> bool:
        drop_rate = max(0.0, min(1.0, float(self.settings.blessing_drop_rate)))
        if self._rng.random() >= drop_rate:
            return False

        blessing_id = random_blessing_id(self._rng)
        if blessing_id is None:
            return False

        self.spawn_blessing(position=position, blessing_id=blessing_id)
        return True

    def _apply_player_actions(self) -> None:
        for player_id, player in self.players.items():
            if not player.alive:
                continue

            actions = self._pending_actions.get(player_id, PlayerActions())
            player.set_movement(actions.move_x, actions.move_y)

            if actions.aim_position is not None:
                player.aim_position = Vec2(*actions.aim_position)

            if actions.throw:
                self.combat.try_throw_projectile(self, player)

        self._pending_actions.clear()

    def _apply_session_actions(self) -> None:
        for player_id, session_actions in self._pending_session_actions.items():
            if session_actions.request_pause:
                self.session.request_pause(player_id)

            if session_actions.ready_up:
                self.session.mark_ready(player_id)

        self._pending_session_actions.clear()

    def _maybe_start_resume_countdown(self) -> None:
        player_ids = set(self.players)
        if self.session.phase is not MatchPhase.PAUSED:
            return

        if self.session.all_players_ready(player_ids):
            self.session.start_resume_countdown()

    def _update_enemy_ai(self, dt: float) -> None:
        self.navigation.begin_tick()
        alive_enemy_ids: set[int] = set()
        for enemy in self.enemies.values():
            if not enemy.alive:
                continue
            alive_enemy_ids.add(enemy.entity_id)
            enemy.attack_cooldown_seconds = max(0.0, enemy.attack_cooldown_seconds - dt)

            if enemy.active_ability_id is not None:
                enemy.velocity = Vec2(0.0, 0.0)
                continue

            target_player = nearest_player(enemy.position, self.players)
            if target_player is None:
                enemy.velocity = Vec2(0.0, 0.0)
                continue

            if self._apply_ranged_attack_behavior(enemy, target_player):
                previous_position = enemy.position.copy()
                enemy.update(dt, self.world_width, self.world_height)
                self._resolve_blocking_for_entity(enemy, previous_position)
                continue

            enemy.velocity = self.navigation.choose_velocity(
                enemy=enemy,
                target_position=target_player.position,
                dt=dt,
                blocking_grid=self.blocking_grid,
                tile_size=self.blocking_tile_size,
            )

            previous_position = enemy.position.copy()
            enemy.update(dt, self.world_width, self.world_height)
            self._resolve_blocking_for_entity(enemy, previous_position)
        self.navigation.prune(alive_enemy_ids)

    def _apply_ranged_attack_behavior(self, enemy: Enemy, target_player: Player) -> bool:
        ability = self._get_ranged_shot_ability(enemy)
        if ability is None:
            return False

        attack_range = max(1.0, float(ability.attack_range))
        delta = target_player.position - enemy.position
        in_range = delta.length_squared() <= attack_range * attack_range
        if not in_range:
            return False

        enemy.velocity = Vec2(0.0, 0.0)
        if enemy.attack_cooldown_seconds > 0.0:
            return True

        if delta.length_squared() <= 0.0:
            return True

        direction = delta.normalized()
        projectile_speed = max(1.0, float(ability.projectile_speed))
        projectile_damage = max(1, int(ability.projectile_damage))
        projectile_ttl = max(0.05, float(ability.projectile_ttl_seconds))
        projectile_radius = max(1.0, float(ability.projectile_radius))
        self.spawn_projectile(
            position=enemy.position.copy(),
            velocity=direction * projectile_speed,
            owner_player_id="",
            damage=projectile_damage,
            ttl_seconds=projectile_ttl,
            radius=projectile_radius,
            source_faction="enemy",
            projectile_effect_id=ability.projectile_effect_id,
        )
        enemy.attack_cooldown_seconds = max(0.05, float(ability.attack_interval_seconds))
        return True

    def handle_enemy_player_contact(self, enemy: Enemy, player: Player) -> bool:
        delayed_explosion = self._get_delayed_explosion_ability(enemy)
        if delayed_explosion is None:
            return False

        self._arm_enemy_delayed_explosion(enemy, delayed_explosion)
        return False

    def resolve_enemy_damage_defeat(self, enemy: Enemy, killer_player_id: str | None) -> None:
        delayed_explosion = self._get_delayed_explosion_ability(enemy)
        if delayed_explosion is not None:
            self._arm_enemy_delayed_explosion(enemy, delayed_explosion)
            return
        self.defeat_enemy(enemy, killer_player_id=killer_player_id)

    def _collect_coins(self) -> None:
        for coin in self.coins.values():
            if not coin.alive:
                continue

            for player in self.players.values():
                if not player.alive:
                    continue
                if not circles_overlap(
                    player.position,
                    player.coin_pickup_radius,
                    coin.position,
                    coin.radius,
                ):
                    continue

                self._collect_coin_for_player(coin, player)
                break

    def _collect_coin_for_player(self, coin: Coin, collector: Player) -> None:
        collector.coins += coin.value
        self.total_coins_collected += coin.value
        coin.alive = False
        self.coin_vacuum_coin_ids.discard(coin.entity_id)

    def _update_coin_vacuum(self, dt: float) -> None:
        if not self.coin_vacuum_coin_ids:
            self.coin_vacuum_target_player_id = None
            return

        if self.coin_vacuum_target_player_id is None:
            self.coin_vacuum_coin_ids.clear()
            return

        collector = self.players.get(self.coin_vacuum_target_player_id)
        if collector is None or not collector.alive:
            self.coin_vacuum_coin_ids.clear()
            self.coin_vacuum_target_player_id = None
            return

        pull_speed = max(1.0, float(self.settings.coin_vacuum_pull_speed))
        for coin_id in list(self.coin_vacuum_coin_ids):
            coin = self.coins.get(coin_id)
            if coin is None or not coin.alive:
                self.coin_vacuum_coin_ids.discard(coin_id)
                continue

            direction = collector.position - coin.position
            distance = direction.length()
            collect_distance = max(1.0, collector.coin_pickup_radius + coin.radius)
            if distance <= collect_distance:
                self._collect_coin_for_player(coin, collector)
                continue

            move_distance = pull_speed * dt
            if move_distance >= distance:
                coin.position = collector.position.copy()
            else:
                coin.position = coin.position + direction.normalized() * move_distance

    def _update_damage_auras(self, dt: float) -> None:
        if not self.active_damage_auras:
            return

        expired_player_ids: list[str] = []
        tick_interval = max(0.05, float(self.settings.damage_aura_tick_interval_seconds))
        for player_id, aura in self.active_damage_auras.items():
            player = self.players.get(player_id)
            if player is None or not player.alive:
                expired_player_ids.append(player_id)
                continue

            aura.remaining_seconds = max(0.0, aura.remaining_seconds - dt)
            if aura.remaining_seconds <= 0.0:
                expired_player_ids.append(player_id)
                continue

            aura.tick_cooldown_seconds = max(0.0, aura.tick_cooldown_seconds - dt)
            if aura.tick_cooldown_seconds > 0.0:
                continue

            self._apply_damage_aura_tick(player_id, player)
            aura.tick_cooldown_seconds = tick_interval

        for player_id in expired_player_ids:
            self.active_damage_auras.pop(player_id, None)

    def _apply_damage_aura_tick(self, player_id: str, player: Player) -> None:
        damage = max(1, int(self.settings.damage_aura_damage_per_tick))
        aura_radius = max(1.0, float(self.settings.damage_aura_radius))
        for enemy in list(self.enemies.values()):
            if not enemy.alive:
                continue
            if not circles_overlap(player.position, aura_radius, enemy.position, enemy.radius):
                continue

            enemy.take_damage(damage)
            if enemy.alive:
                continue
            self.resolve_enemy_damage_defeat(enemy, killer_player_id=player_id)

    def _update_enemy_abilities(self, dt: float) -> None:
        active_enemy_ids = [
            enemy.entity_id
            for enemy in self.enemies.values()
            if enemy.alive and enemy.active_ability_id is not None
        ]
        for enemy_id in active_enemy_ids:
            enemy = self.enemies.get(enemy_id)
            if enemy is None or not enemy.alive or enemy.active_ability_id is None:
                continue

            enemy.ability_timer_seconds = max(0.0, enemy.ability_timer_seconds - dt)
            if enemy.active_ability_id == ENEMY_ABILITY_DELAYED_EXPLOSION_ON_TOUCH:
                if enemy.ability_timer_seconds > 0.0:
                    continue
                self._explode_enemy(enemy)

    def _explode_enemy(self, source_enemy: Enemy) -> None:
        ability = self._get_delayed_explosion_ability(source_enemy)
        if ability is None:
            return

        explosion_radius = max(1.0, float(ability.explosion_radius))
        explosion_damage = max(1, int(ability.explosion_damage))
        explosion_center = source_enemy.position.copy()

        for player in self.players.values():
            if not player.alive:
                continue
            if not circles_overlap(
                explosion_center,
                explosion_radius,
                player.position,
                player.radius,
            ):
                continue
            player.take_damage(explosion_damage)

        for enemy in list(self.enemies.values()):
            if not enemy.alive or enemy.entity_id == source_enemy.entity_id:
                continue
            if not circles_overlap(
                explosion_center,
                explosion_radius,
                enemy.position,
                enemy.radius,
            ):
                continue
            enemy.take_damage(explosion_damage)
            if enemy.alive:
                continue
            self.resolve_enemy_damage_defeat(enemy, killer_player_id=None)

        self.defeat_enemy(source_enemy, killer_player_id=None)

    def _get_delayed_explosion_ability(self, enemy: Enemy) -> EnemyAbilityDefinition | None:
        profile = get_enemy_profile(enemy.profile_id)
        if profile is None:
            return None
        for ability in profile.abilities:
            if ability.ability_id == ENEMY_ABILITY_DELAYED_EXPLOSION_ON_TOUCH:
                return ability
        return None

    def _get_ranged_shot_ability(self, enemy: Enemy) -> EnemyAbilityDefinition | None:
        profile = get_enemy_profile(enemy.profile_id)
        if profile is None:
            return None
        for ability in profile.abilities:
            if ability.ability_id == ENEMY_ABILITY_RANGED_SHOT:
                return ability
        return None

    def _arm_enemy_delayed_explosion(
        self,
        enemy: Enemy,
        ability: EnemyAbilityDefinition,
    ) -> None:
        remaining_seconds = max(
            float(ability.arming_delay_seconds),
            float(enemy.ability_timer_seconds),
        )
        enemy.alive = True
        enemy.health = max(1, enemy.health)
        enemy.arm_ability(
            ability.ability_id,
            timer_seconds=remaining_seconds,
            vfx_effect_id=ability.loop_effect_id,
        )

    def _collect_blessings(self) -> None:
        for blessing in list(self.blessings.values()):
            if not blessing.alive:
                continue

            for player in self.players.values():
                if not player.alive:
                    continue
                if not circles_overlap(
                    player.position,
                    player.coin_pickup_radius,
                    blessing.position,
                    blessing.radius,
                ):
                    continue

                self.blessing_system.apply_blessing(
                    self,
                    collector_player_id=player.player_id,
                    blessing_id=blessing.blessing_id,
                )
                self._queue_profile_progress_event(
                    kind="blessing",
                    entry_id=blessing.blessing_id,
                )
                blessing.alive = False
                break

    def _cleanup_dead_entities(self) -> None:
        self.enemies = {enemy_id: enemy for enemy_id, enemy in self.enemies.items() if enemy.alive}
        self.projectiles = {
            projectile_id: projectile
            for projectile_id, projectile in self.projectiles.items()
            if projectile.alive
        }
        self.coins = {coin_id: coin for coin_id, coin in self.coins.items() if coin.alive}
        self.coin_vacuum_coin_ids.intersection_update(self.coins)
        if not self.coin_vacuum_coin_ids:
            self.coin_vacuum_target_player_id = None
        self.active_damage_auras = {
            player_id: aura
            for player_id, aura in self.active_damage_auras.items()
            if aura.remaining_seconds > 0.0 and self.players.get(player_id) is not None
        }
        self.blessings = {
            blessing_id: blessing
            for blessing_id, blessing in self.blessings.items()
            if blessing.alive
        }

    def _update_game_over_state(self) -> None:
        if not self.players:
            return

        has_alive_player = any(player.alive for player in self.players.values())
        if not has_alive_player:
            self.session.set_game_over()
            if self.final_run_result is None:
                self.final_run_result = self.build_run_result()

    def _clamp_entities_to_world_bounds(self) -> None:
        for player in self.players.values():
            player.position.x = max(
                player.radius,
                min(player.position.x, self.world_width - player.radius),
            )
            player.position.y = max(
                player.radius,
                min(player.position.y, self.world_height - player.radius),
            )

        for enemy in self.enemies.values():
            enemy.position.x = max(
                enemy.radius,
                min(enemy.position.x, self.world_width - enemy.radius),
            )
            enemy.position.y = max(
                enemy.radius,
                min(enemy.position.y, self.world_height - enemy.radius),
            )

        for projectile in self.projectiles.values():
            projectile.position.x = max(
                projectile.radius,
                min(projectile.position.x, self.world_width - projectile.radius),
            )
            projectile.position.y = max(
                projectile.radius,
                min(projectile.position.y, self.world_height - projectile.radius),
            )

        for coin in self.coins.values():
            coin.position.x = max(
                coin.radius,
                min(coin.position.x, self.world_width - coin.radius),
            )
            coin.position.y = max(
                coin.radius,
                min(coin.position.y, self.world_height - coin.radius),
            )

        for blessing in self.blessings.values():
            blessing.position.x = max(
                blessing.radius,
                min(blessing.position.x, self.world_width - blessing.radius),
            )
            blessing.position.y = max(
                blessing.radius,
                min(blessing.position.y, self.world_height - blessing.radius),
            )

    def _allocate_entity_id(self) -> int:
        entity_id = self._next_entity_id
        self._next_entity_id += 1
        return entity_id

    def _queue_profile_progress_event(self, *, kind: str, entry_id: str) -> None:
        normalized_id = str(entry_id).strip()
        if not normalized_id:
            return
        self._pending_profile_progress_events.append(
            {
                "kind": kind,
                "id": normalized_id,
            }
        )

    def _resolve_blocking_for_entity(self, entity: Player | Enemy, previous_position: Vec2) -> None:
        if not self._has_blocking_grid() or not entity.alive:
            return

        if not self._position_intersects_blocking(entity.position, entity.radius):
            return

        attempted_x = entity.position.x
        attempted_y = entity.position.y

        x_candidate = Vec2(attempted_x, previous_position.y)
        y_candidate = Vec2(previous_position.x, attempted_y)
        x_blocked = self._position_intersects_blocking(x_candidate, entity.radius)
        y_blocked = self._position_intersects_blocking(y_candidate, entity.radius)

        if not x_blocked:
            entity.position.x = x_candidate.x
            entity.position.y = x_candidate.y
            return
        if not y_blocked:
            entity.position.x = y_candidate.x
            entity.position.y = y_candidate.y
            return

        entity.position.x = previous_position.x
        entity.position.y = previous_position.y

    def _has_blocking_grid(self) -> bool:
        return bool(self.blocking_grid) and self.blocking_tile_size > 0.0

    def _position_intersects_blocking(self, position: Vec2, radius: float) -> bool:
        if not self._has_blocking_grid():
            return False

        grid = self.blocking_grid
        if grid is None:
            return False

        tile_size = self.blocking_tile_size
        min_col = math.floor((position.x - radius) / tile_size)
        max_col = math.floor((position.x + radius) / tile_size)
        min_row = math.floor((position.y - radius) / tile_size)
        max_row = math.floor((position.y + radius) / tile_size)

        grid_height = len(grid)
        if grid_height == 0:
            return False
        grid_width = len(grid[0])
        if grid_width == 0:
            return False

        if max_col < 0 or max_row < 0 or min_col >= grid_width or min_row >= grid_height:
            return False

        clamped_min_col = max(0, min_col)
        clamped_max_col = min(grid_width - 1, max_col)
        clamped_min_row = max(0, min_row)
        clamped_max_row = min(grid_height - 1, max_row)

        for row in range(clamped_min_row, clamped_max_row + 1):
            for col in range(clamped_min_col, clamped_max_col + 1):
                if grid[row][col]:
                    return True
        return False

    def _nearest_walkable_position(self, preferred: Vec2, radius: float) -> Vec2:
        if not self._has_blocking_grid():
            return preferred.copy()

        if not self._position_intersects_blocking(preferred, radius):
            return preferred.copy()

        grid = self.blocking_grid
        if grid is None or not grid or not grid[0]:
            return preferred.copy()

        tile_size = self.blocking_tile_size
        grid_height = len(grid)
        grid_width = len(grid[0])
        origin_col = math.floor(preferred.x / tile_size)
        origin_row = math.floor(preferred.y / tile_size)
        max_distance = max(grid_width, grid_height)

        for distance in range(1, max_distance + 1):
            min_row = max(0, origin_row - distance)
            max_row = min(grid_height - 1, origin_row + distance)
            min_col = max(0, origin_col - distance)
            max_col = min(grid_width - 1, origin_col + distance)

            for row in range(min_row, max_row + 1):
                for col in range(min_col, max_col + 1):
                    if row not in (min_row, max_row) and col not in (min_col, max_col):
                        continue
                    if grid[row][col]:
                        continue

                    candidate = Vec2(
                        x=min(
                            max((col + 0.5) * tile_size, radius),
                            self.world_width - radius,
                        ),
                        y=min(
                            max((row + 0.5) * tile_size, radius),
                            self.world_height - radius,
                        ),
                    )
                    if not self._position_intersects_blocking(candidate, radius):
                        return candidate

        return preferred.copy()

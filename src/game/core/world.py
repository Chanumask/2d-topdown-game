from __future__ import annotations

import random
from dataclasses import dataclass, field

from game.core.run_result import RunResult
from game.core.session_state import MatchPhase, SessionState
from game.core.snapshot import WorldSnapshot
from game.core.upgrades import RunModifiers
from game.entities import Coin, Enemy, Player, Projectile, Vec2
from game.input.actions import PlayerActions
from game.input.session_actions import SessionActions
from game.settings import GameSettings
from game.systems import CombatSystem, EnemySpawner
from game.systems.collision import circles_overlap, nearest_player


@dataclass(slots=True)
class World:
    settings: GameSettings
    world_width: float
    world_height: float
    run_modifiers: RunModifiers = field(default_factory=RunModifiers)
    players: dict[str, Player] = field(default_factory=dict)
    enemies: dict[int, Enemy] = field(default_factory=dict)
    projectiles: dict[int, Projectile] = field(default_factory=dict)
    coins: dict[int, Coin] = field(default_factory=dict)
    tick: int = 0
    simulation_time: float = 0.0
    total_coins_collected: int = 0
    enemies_killed_total: int = 0
    enemies_killed_by_player: dict[str, int] = field(default_factory=dict)
    final_run_result: RunResult | None = None
    session: SessionState = field(default_factory=SessionState)
    spawner: EnemySpawner = field(init=False)
    combat: CombatSystem = field(init=False)
    _rng: random.Random = field(init=False, repr=False)
    _next_entity_id: int = field(init=False, repr=False)
    _pending_actions: dict[str, PlayerActions] = field(init=False, repr=False)
    _pending_session_actions: dict[str, SessionActions] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self._rng = random.Random()
        self._next_entity_id = 1
        self._pending_actions = {}
        self._pending_session_actions = {}

        self.spawner = EnemySpawner(
            rng=self._rng,
            base_interval_seconds=self.settings.spawn_base_interval_seconds,
            min_interval_seconds=self.settings.spawn_min_interval_seconds,
            acceleration_per_second=self.settings.spawn_acceleration_per_second,
        )
        self.combat = CombatSystem(
            projectile_speed=max(
                1.0,
                self.settings.projectile_speed + self.run_modifiers.projectile_speed_bonus,
            ),
            projectile_damage=self.settings.projectile_damage,
            projectile_ttl_seconds=self.settings.projectile_ttl_seconds,
            projectile_radius=self.settings.projectile_radius,
        )

    def add_player(self, player_id: str, character_id: str | None = None) -> None:
        if player_id in self.players:
            return

        spawn = Vec2(self.world_width * 0.5, self.world_height * 0.5)
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
            player.update(dt, self.world_width, self.world_height)

        self.spawner.update(self, dt)
        self._update_enemy_ai(dt)

        self.combat.update_projectiles(self, dt)
        self.combat.resolve(self)

        self._collect_coins()
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
        return self.spawner.current_interval(self.simulation_time)

    def snapshot(self) -> WorldSnapshot:
        players = [self.players[player_id].to_dict() for player_id in sorted(self.players)]
        enemies = [self.enemies[enemy_id].to_dict() for enemy_id in sorted(self.enemies)]
        projectiles = [
            self.projectiles[projectile_id].to_dict() for projectile_id in sorted(self.projectiles)
        ]
        coins = [self.coins[coin_id].to_dict() for coin_id in sorted(self.coins)]

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

    def spawn_enemy(self, position: Vec2, health: int, speed: float, touch_damage: int) -> None:
        enemy = Enemy(
            entity_id=self._allocate_entity_id(),
            position=position,
            radius=self.settings.enemy_radius,
            speed=speed,
            max_health=health,
            health=health,
            touch_damage=touch_damage,
            coin_drop_value=self.settings.coin_value,
        )
        self.enemies[enemy.entity_id] = enemy

    def spawn_projectile(
        self,
        position: Vec2,
        velocity: Vec2,
        owner_player_id: str,
        damage: int,
        ttl_seconds: float,
        radius: float,
    ) -> None:
        projectile = Projectile(
            entity_id=self._allocate_entity_id(),
            position=position,
            radius=radius,
            owner_player_id=owner_player_id,
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

    def register_enemy_kill(self, killer_player_id: str | None) -> None:
        self.enemies_killed_total += 1
        if killer_player_id is None:
            return

        self.enemies_killed_by_player.setdefault(killer_player_id, 0)
        self.enemies_killed_by_player[killer_player_id] += 1

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
        for enemy in self.enemies.values():
            if not enemy.alive:
                continue

            target_player = nearest_player(enemy.position, self.players)
            if target_player is None:
                enemy.velocity = Vec2(0.0, 0.0)
            else:
                enemy.chase(target_player.position)

            enemy.update(dt, self.world_width, self.world_height)

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

                player.coins += coin.value
                self.total_coins_collected += coin.value
                coin.alive = False
                break

    def _cleanup_dead_entities(self) -> None:
        self.enemies = {enemy_id: enemy for enemy_id, enemy in self.enemies.items() if enemy.alive}
        self.projectiles = {
            projectile_id: projectile
            for projectile_id, projectile in self.projectiles.items()
            if projectile.alive
        }
        self.coins = {coin_id: coin for coin_id, coin in self.coins.items() if coin.alive}

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

    def _allocate_entity_id(self) -> int:
        entity_id = self._next_entity_id
        self._next_entity_id += 1
        return entity_id

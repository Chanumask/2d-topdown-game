from game.core.profile import PlayerProfile, UserSettings
from game.core.run_result import RunResult
from game.core.snapshot import WorldSnapshot
from game.core.world import World
from game.entities import Coin, Enemy, Player, Projectile
from game.input.actions import PlayerActions
from game.input.session_actions import SessionActions


def serialize_player_actions(actions: PlayerActions) -> dict[str, object]:
    return actions.to_dict()


def deserialize_player_actions(payload: dict[str, object]) -> PlayerActions:
    return PlayerActions.from_dict(payload)


def serialize_session_actions(actions: SessionActions) -> dict[str, object]:
    return actions.to_dict()


def deserialize_session_actions(payload: dict[str, object]) -> SessionActions:
    return SessionActions.from_dict(payload)


def serialize_player(player: Player) -> dict[str, object]:
    return player.to_dict()


def deserialize_player(payload: dict[str, object]) -> Player:
    return Player.from_dict(payload)


def serialize_enemy(enemy: Enemy) -> dict[str, object]:
    return enemy.to_dict()


def deserialize_enemy(payload: dict[str, object]) -> Enemy:
    return Enemy.from_dict(payload)


def serialize_projectile(projectile: Projectile) -> dict[str, object]:
    return projectile.to_dict()


def deserialize_projectile(payload: dict[str, object]) -> Projectile:
    return Projectile.from_dict(payload)


def serialize_coin(coin: Coin) -> dict[str, object]:
    return coin.to_dict()


def deserialize_coin(payload: dict[str, object]) -> Coin:
    return Coin.from_dict(payload)


def serialize_world_snapshot(snapshot: WorldSnapshot) -> dict[str, object]:
    return snapshot.to_dict()


def deserialize_world_snapshot(payload: dict[str, object]) -> WorldSnapshot:
    return WorldSnapshot.from_dict(payload)


def serialize_run_result(run_result: RunResult) -> dict[str, object]:
    return run_result.to_dict()


def deserialize_run_result(payload: dict[str, object]) -> RunResult:
    return RunResult.from_dict(payload)


def serialize_world(world: World) -> dict[str, object]:
    return world.to_dict()


def serialize_profile(profile: PlayerProfile) -> dict[str, object]:
    return profile.to_dict()


def deserialize_profile(payload: dict[str, object]) -> PlayerProfile:
    return PlayerProfile.from_dict(payload)


def serialize_user_settings(settings: UserSettings) -> dict[str, object]:
    return settings.to_dict()


def deserialize_user_settings(payload: dict[str, object]) -> UserSettings:
    return UserSettings.from_dict(payload)

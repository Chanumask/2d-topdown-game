# Runner2D Survival Prototype

Top-down 2D survival prototype using `pygame-ce`, managed with `uv`, and linted/formatted by `ruff`.

This version is structured for future online multiplayer by separating:

- Input layer (`game/input`)
- Simulation/session layer (`game/core`, `game/entities`, `game/systems`)
- Rendering layer (`game/render`)
- Serialization layer (`game/serialization`)
- UI/app state layer (`game/ui`, `game/core/app_state.py`)

## Setup

```bash
uv venv .venv
uv sync --dev
```

## Run

```bash
uv run runner2d
```

Canonical run path: `uv run runner2d`

## Controls

- Main menu / shop / settings / pause menu:
  - `Up/Down`: select option
  - `Left/Right`: adjust setting values
  - `Enter` / `Space`: confirm
  - `Esc` / `Backspace`: back
  - Mouse move: hover/select items
  - Left click: activate selected item/button
- During run:
  - `WASD`: move
  - Mouse: aim
  - Left click: shoot
  - `P` or `Esc`: request shared pause countdown

## Lint and Format

```bash
uv run ruff check .
uv run ruff format .
```

## Profile Save Data

- Save file: `save/profile.json`
- Encoding/format: UTF-8 JSON with indentation
- Schema wrapper:
  - `schema_version`
  - `profile`

Profile persistence is app-level (`game/core/profile_store.py`) and stores profile/meta progression
outside run simulation.

## Implemented Gameplay

- App boots into main menu (`Start Run`, `Shop`, `Settings`, `Quit`)
- Main menu, pause menu, settings menu, and shop are keyboard + mouse interactable
- WASD movement
- Mouse aiming
- Projectile shooting
- Enemy spawning with increasing spawn rate
- Enemy chasing nearest player
- Enemy damage on player collision
- Enemy death from projectiles
- Coin drop and collection
- Difficulty growth over time
- Explicit session state (`running`, `pause_countdown`, `paused`, `resume_countdown`, `game_over`)
- Shared pause flow with 3-second pause and resume countdowns
- Per-player ready-up tracking in paused state
- Shop upgrade purchases with persistent levels and costs
- Profile/meta progression persistence in `save/profile.json`
- Shared settings model reused from main menu and pause menu
- Fullscreen toggle applies immediately and persists in profile save data
- Fixed-timestep simulation with decoupled rendering
- Serializable world snapshots for future network transport
- Authoritative run result pipeline for game-over/results + banking

## Known Limitation

- Fullscreen gameplay currently changes viewport size, but world/map rendering scale behavior
  is not fully adapted for large fullscreen resolutions yet. This is intentionally deferred for
  the planned camera/map rendering rework.

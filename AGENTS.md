Project overview

This repository contains a top-down 2D survival game built in Python with pygame-ce.

The game includes:
	•	fixed-map runs
	•	layered tile maps created with a map editor
	•	persistent meta progression
	•	shop upgrades
	•	menu / settings / pause flows
	•	audio systems
	•	blocking terrain and pathing constraints

The architecture is being prepared for future online multiplayer.

Do not optimize for rapid hacks.
Optimize for clean extension and system stability.

⸻

Core technical stack

Language
• Python

Framework
• pygame-ce

Dependency/environment management
• uv

Lint/format
• ruff

Environment rules

• Use the local project environment only
• Never install dependencies system-wide
• Prefer commands such as:

uv run runner2d
uv run ruff check .
uv run ruff format .

⸻

Non-negotiable architecture boundaries

Input / simulation / rendering separation

Keep input, simulation, and rendering as separate layers.

Simulation:
• must not read pygame keyboard/mouse APIs directly

Input layer:
• converts raw input → abstract actions

Rendering:
• reads simulation/app state
• draws visuals only

Rendering must not mutate gameplay state.

⸻

Persistence boundary

World/simulation code must not perform file I/O.

Persistent data is handled externally.

Use profile_store.py for save/load.

Do not add ad-hoc persistence logic inside:
	•	UI systems
	•	gameplay systems
	•	entities
	•	world logic

⸻

Progression boundary

End-of-run progression must flow through authoritative RunResult.

UI must not invent run results.

Meta progression must use:

profile.bank_run_result(…)

Shop purchases must happen in profile/domain logic, not simulation.

⸻

Upgrade boundary

Upgrade ownership lives in PlayerProfile.

Upgrade definitions live in a catalog/domain layer.

Upgrade effects are applied at run bootstrap only.

Simulation receives:

• prepared modifiers
• initial parameters

Simulation must not inspect shop UI state or save files.

⸻

Session / pause boundary

Pause state is shared session state, not local UI state.

Pause system rules:

• pause requester must be tracked
• ready-up must be tracked per player ID
• pause countdown / resume countdown must remain multiplayer-safe

Do not add local pause hacks that bypass session state.

⸻

Multiplayer-conformity rules

A feature is multiplayer-conform if most of the following are true:

• it does not assume exactly one player
• player state uses player IDs
• state can be represented as shared authoritative state
• state can be serialized without pygame objects
• state does not depend on hidden UI-only data
• system could later be owned by a server

When implementing a system ask:

• Is this app, profile, session, or run simulation state?
• Would this still work if a future server owned the world/session?
• Am I mixing UI concerns with authoritative state?

⸻

State separation rules

Keep these layers clearly separated.

App state

Examples:

• current screen/menu
• screen navigation
• local display mode
• UI hover/focus state

Profile state

Examples:

• meta currency
• purchased upgrades
• persistent settings
• lifetime statistics

Session state

Examples:

• running / pause_countdown / paused / resume_countdown / game_over
• pause requester
• players ready to resume
• countdown timers

Run simulation state

Examples:

• players in the run
• enemies
• projectiles
• pickups
• simulation time/ticks
• spawner logic
• combat state

Never blur these layers without a clear architectural reason.

⸻

Map system rules

Maps are data-driven layered maps created using the map-builder tool.

Each map consists of multiple layer files.

Example:

assets/maps/<map_id>/
layer1.py
layer2.py
layer3.py

Each layer contains:

LAYER_NAME
LAYER_ORDER
TILESET_PATH
TILE_SIZE
MAP_WIDTH
MAP_HEIGHT
UNIT_COORD_GRID
BLOCKING_GRID

Layer rendering rules

Layers render bottom → top using LAYER_ORDER.

Typical order:

1 base terrain (A5)
2 liquids / hazards (A1)
3 props / trees / structures (B)

Cells in UNIT_COORD_GRID may be:

None

which means transparent tile.

Renderer must skip drawing None cells.

⸻

Blocking tiles

Maps include a per-layer grid:

BLOCKING_GRID

This is a boolean grid aligned with UNIT_COORD_GRID.

A tile is blocking if ANY layer marks it blocking.

Movement rules:

final_blocking = OR(all_layer_blocking_cells)

Blocking affects:

• player movement
• enemy movement
• pathfinding

Rendering must not infer blocking from visuals.

Blocking is explicit data only.

⸻

Map builder integration

Maps are created using the map-builder repository.

The editor exports layer files containing:

UNIT_COORD_GRID
BLOCKING_GRID

Empty cells are stored as:

None

The main game must:

• load layer files safely
• not execute arbitrary code
• validate grid sizes
• validate tile coordinates

Use safe parsing (AST + literal_eval).

⸻

Audio system rules

Audio is centralized.

Structure:

src/game/audio/
audio_assets.py
audio_manager.py

Responsibilities:

audio_assets.py
• registry of logical sounds/music
• defines expected filenames

audio_manager.py
• loads sounds
• manages playback
• applies volume settings
• handles missing assets safely

⸻

Audio asset structure

assets/audio/music/
assets/audio/sfx/ui/
assets/audio/sfx/player/
assets/audio/sfx/enemies/
assets/audio/sfx/world/

Example SFX:

ui/button_hover
ui/button_confirm
ui/pause_timer_tick
player/rock_throw
world/coin_pickup
enemies/enemy_hit
enemies/enemy_death

Audio registry supports multiple file extensions automatically.

Preferred priority:

1 .wav
2 .mp3
3 .ogg

Missing files must never crash the game.

⸻

UI rules

Main menu:

• must support keyboard navigation
• should support mouse hover and click

Pause menu:

• must support mouse hover and click
• keyboard navigation must still work

UI readability rules:

• do not overlap text
• long descriptions go into dedicated panels
• prefer readable layouts over dense layouts

Fullscreen is local client behavior only.

UI must not affect simulation logic.

⸻

Menu behavior expectations

Boot → main menu.

Main menu:

• player-facing options only

Shop:

• uses persistent profile currency

Settings:

• shared across entry points

Pause menu:

• reflects shared session state

Results screens:

• read authoritative run results

⸻

Rendering rules

Renderer should remain snapshot driven.

Renderer responsibilities:

• draw map layers
• draw entities
• draw effects
• draw UI

Renderer must not contain gameplay authority.

Keep draw order explicit.

⸻

Persistence rules

Save format:

JSON

Rules:

• human readable
• schema versioned
• backwards compatible when possible

Missing fields should load with safe defaults.

Never persist:

• world objects
• session state
• pygame objects

⸻

Data/model rules

Prefer data-driven catalogs.

Examples:

• upgrades
• enemies
• maps
• audio assets

Prefer:

• dataclasses
• explicit models
• serializable structures

Avoid:

large nested dict soup.

Provide to_dict() / from_dict() when models cross boundaries.

⸻

File/module placement guidance

Use existing structure:

core/ — app/session/profile coordination
entities/ — gameplay entities
systems/ — gameplay systems
input/ — input → actions
render/ — rendering/camera/display logic
ui/ — menus and UI widgets
audio/ — audio systems
serialization/ — serialization helpers

Do not place new systems in random modules.

⸻

Coding style preferences

• keep modules focused
• avoid giant god-classes
• prefer composition
• avoid premature frameworks
• avoid introducing ECS unless explicitly requested

Prefer clear names over clever names.

Add comments only where they improve understanding.

⸻

Change discipline

When making changes:

• preserve architecture boundaries
• avoid unnecessary rewrites
• avoid breaking save compatibility
• avoid duplicating existing logic

When adding features consider:

• serialization impact
• persistence impact
• multiplayer compatibility
• UI readability
• correct state ownership

⸻

Tooling expectations

Use uv and ruff.

Standard commands:

uv run runner2d
uv run ruff check .
uv run ruff format .

Never rely on system Python or packages.

⸻

What to avoid

Do not:

• install dependencies system-wide
• read pygame input inside simulation
• perform file I/O inside world/entities/systems
• let UI invent authoritative results
• hardcode single-player assumptions
• leave debug text visible in UI
• solve layout issues by drawing text on top of text
• bypass session state for pause/resume

⸻

Preferred workflow for larger changes

1 define/extend domain model
2 wire correct state ownership (app/profile/session/run)
3 integrate simulation boundary if needed
4 update UI/rendering
5 run lint/checks
6 validate the affected flow

⸻

Current high-level priorities

When in doubt:

• maintain multiplayer-ready architecture
• keep persistent progression clean
• keep menus/settings/shop readable
• keep systems data-driven
• build features without collapsing architectural boundaries
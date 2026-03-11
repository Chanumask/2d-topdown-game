Project overview
	•	This repository contains a top-down 2D survival game built in Python with pygame-ce.
	•	The game has:
	•	fixed-map runs
	•	persistent meta progression
	•	shop upgrades
	•	menu/settings/pause flows
	•	The architecture is being prepared for future online multiplayer.
	•	Do not optimize for rapid hacks. Optimize for clean extension.

Core technical stack
	•	Language: Python
	•	Framework: pygame-ce
	•	Dependency/environment management: uv
	•	Lint/format: ruff
	•	Use the local project environment only.
	•	Never install dependencies system-wide.

Non-negotiable architecture boundaries

Input / simulation / rendering separation
	•	Keep input, simulation, and rendering as separate layers.
	•	Simulation must not directly read pygame keyboard or mouse APIs.
	•	Input layers convert raw input into abstract actions.
	•	Rendering reads simulation/app state and draws it.
	•	Rendering must not secretly mutate gameplay state.

Persistence boundary
	•	World/simulation code must not perform file I/O.
	•	Persistent profile data is handled outside simulation.
	•	Use profile_store.py for profile save/load responsibilities.
	•	Do not add ad-hoc save/load logic in UI or gameplay systems.

Progression boundary
	•	End-of-run progression must flow through authoritative RunResult.
	•	UI must not invent run results.
	•	Banking meta progression must use profile.bank_run_result(...).
	•	Shop purchases happen in profile/app/domain logic, not in simulation.

Upgrade boundary
	•	Upgrade ownership lives in PlayerProfile.
	•	Upgrade definitions/rules live in the upgrade catalog/domain layer.
	•	Upgrade effects are applied at run bootstrap only.
	•	Simulation should receive prepared run modifiers/initial parameters.
	•	Simulation must not inspect shop UI state or save files.

Session / pause boundary
	•	Pause state is shared session/match state, not local-only UI state.
	•	Ready-up state must be tracked per player ID.
	•	Countdown-driven pause/resume logic must remain multiplayer-safe.
	•	Do not implement local-only pause hacks that bypass session state.

Multiplayer-conformity rules

A feature is multiplayer-conform only if most or all of the following are true:
	•	It does not assume exactly one player unless explicitly temporary.
	•	Player-specific state uses player IDs.
	•	It can be represented as shared authoritative state if needed.
	•	It can be serialized without pygame objects.
	•	It does not depend on hidden local UI-only state.
	•	It could later be owned by a server without rewriting the entire system.

When adding new systems, ask:
	•	Is this app-level state, profile-level state, session-level state, or run simulation state?
	•	Would this still make sense if a future server owned the world/session?
	•	Am I accidentally putting local UI concerns into authoritative state, or authoritative state into local UI?

State separation rules

Keep these concerns distinct:

App state

Examples:
	•	current screen/menu
	•	screen navigation
	•	local display mode
	•	local UI focus/hover state

Profile state

Examples:
	•	meta currency
	•	purchased upgrades
	•	persistent settings
	•	lifetime stats

Session state

Examples:
	•	running / pause_countdown / paused / resume_countdown / game_over
	•	pause requester
	•	players ready to resume
	•	countdown timers

Run simulation state

Examples:
	•	players in the current run
	•	enemies
	•	projectiles
	•	pickups
	•	simulation tick/time
	•	combat/spawner state

Do not blur these layers without a clear reason.

UI rules
	•	Main menu must support keyboard navigation.
	•	Main menu should support mouse hover and click.
	•	Pause menu should support mouse hover and click.
	•	Keyboard navigation should continue to work even when mouse support exists.
	•	Do not leave development/debug text visible in player-facing UI.
	•	Long descriptions and upgrade details should be shown in dedicated info panels, not overlapping list text.
	•	Favor readability over squeezing more text into small areas.
	•	If a details panel exists, reserve space for it instead of letting text collide.
	•	Fullscreen is local client/app behavior only.
	•	UI layout must not affect simulation logic.

Menu behavior expectations
	•	Boot goes to main menu, not directly into gameplay.
	•	Main menu should only show player-facing options/content.
	•	Shop uses persistent profile/meta currency, not live run-world state.
	•	Settings should be shared consistently across entry points.
	•	Pause menu should reflect shared session state.
	•	Game over/results screens should read authoritative result data, not world internals directly.

Rendering rules
	•	Keep renderer snapshot-driven where possible.
	•	Do not put gameplay authority into renderer code.
	•	Avoid arbitrary UI hacks when a small layout/helper abstraction would solve the problem cleanly.
	•	If overlay panels are used, ensure draw order/readability is explicit.

Persistence rules
	•	Save format should be JSON and human-readable.
	•	Use schema versioning for persistent profile data.
	•	Missing/older fields should load safely with reasonable defaults when possible.
	•	Keep save compatibility in mind when extending profile fields.
	•	Do not persist transient run/world/session objects in the profile save.

Data/model rules
	•	Prefer data-driven catalogs for things like upgrades, enemy definitions, and maps.
	•	Prefer explicit models/dataclasses/plain serializable structures over loose dict soup.
	•	Keep serialization free of pygame objects.
	•	Add to_dict() / from_dict() or equivalent where models are intended to cross boundaries.

File/module placement guidance

Use the existing structure and keep responsibilities aligned.
	•	core/ for app/session/profile/domain coordination
	•	entities/ for gameplay entities
	•	systems/ for gameplay systems
	•	input/ for raw input -> action translation
	•	render/ for drawing/camera/display-facing logic
	•	ui/ for menu/screen widgets and layouts
	•	serialization/ for cross-boundary serialization helpers

Do not place new systems in random modules just because it is faster.

Coding style preferences
	•	Keep modules focused and reasonably small.
	•	Prefer composition and helper functions over giant god-classes.
	•	Avoid premature frameworks or overengineering.
	•	Avoid introducing ECS frameworks unless explicitly requested.
	•	Centralize rule/config/catalog logic instead of scattering constants.
	•	Add comments only where they improve understanding.
	•	Prefer clear names over clever names.

Change discipline

When making a change:
	•	preserve existing architecture boundaries
	•	avoid unnecessary rewrites
	•	avoid breaking save compatibility without a migration/fallback plan
	•	avoid duplicating logic that already has a clear owner
	•	verify affected flows end-to-end when practical

When adding a new feature, also think about:
	•	serialization impact
	•	persistence impact
	•	multiplayer-conformity impact
	•	UI readability impact
	•	whether the feature belongs at app/profile/session/run level

Tooling expectations
	•	Use uv for dependency and run commands.
	•	Use ruff for linting/formatting.
	•	Prefer local project commands such as:
	•	uv run runner2d
	•	uv run ruff check .
	•	uv run ruff format .
	•	Do not rely on system Python/package state.

What to avoid
	•	Do not add system-wide installs.
	•	Do not put pygame input polling into world/simulation logic.
	•	Do not put file persistence into world/entities/systems.
	•	Do not let UI directly own authoritative gameplay results.
	•	Do not hardcode single-player assumptions into new systems unless clearly marked temporary.
	•	Do not leave placeholder/debug copy in visible UI.
	•	Do not solve layout problems by drawing text on top of other text.
	•	Do not bypass shared session state for pause/resume behavior.

Preferred workflow for significant changes

For larger features, aim to keep this pattern:
	1.	define or extend data/domain model
	2.	wire app/profile/session ownership correctly
	3.	integrate simulation boundary if needed
	4.	update UI/rendering
	5.	run lint/checks
	6.	run a small sanity validation of the affected flow

Current high-level priorities

When in doubt, preserve and extend these directions:
	•	maintain multiplayer-ready architecture
	•	keep persistent progression clean and durable
	•	keep menus/settings/shop/pause readable and consistent
	•	make systems data-driven and serializable
	•	build content/features without collapsing architectural boundaries
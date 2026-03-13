from __future__ import annotations

import heapq
from dataclasses import dataclass, field

from game.entities import Enemy, Vec2

GridCell = tuple[int, int]


@dataclass(slots=True)
class EnemyNavigationState:
    path_cells: list[GridCell] = field(default_factory=list)
    target_cell: GridCell | None = None
    repath_cooldown_seconds: float = 0.0
    using_pathfinding: bool = False
    stuck_time_seconds: float = 0.0
    last_position: Vec2 | None = None
    last_dt: float = 0.0
    last_attempt_speed: float = 0.0
    last_attempt_was_direct: bool = False


class EnemyNavigationSystem:
    def __init__(
        self,
        *,
        repath_interval_seconds: float,
        max_path_requests_per_tick: int,
        max_search_nodes: int,
        stuck_seconds: float,
        min_progress_per_second: float,
    ) -> None:
        self.repath_interval_seconds = max(0.05, float(repath_interval_seconds))
        self.max_path_requests_per_tick = max(1, int(max_path_requests_per_tick))
        self.max_search_nodes = max(64, int(max_search_nodes))
        self.stuck_seconds = max(0.1, float(stuck_seconds))
        self.min_progress_per_second = max(0.1, float(min_progress_per_second))
        self._path_requests_remaining = self.max_path_requests_per_tick
        self._states: dict[int, EnemyNavigationState] = {}

    def begin_tick(self) -> None:
        self._path_requests_remaining = self.max_path_requests_per_tick

    def prune(self, alive_enemy_ids: set[int]) -> None:
        self._states = {
            enemy_id: state
            for enemy_id, state in self._states.items()
            if enemy_id in alive_enemy_ids
        }

    def choose_velocity(
        self,
        *,
        enemy: Enemy,
        target_position: Vec2 | None,
        dt: float,
        blocking_grid: tuple[tuple[bool, ...], ...] | None,
        tile_size: float,
    ) -> Vec2:
        if target_position is None:
            return Vec2(0.0, 0.0)

        if blocking_grid is None or not blocking_grid or not blocking_grid[0] or tile_size <= 0.0:
            return self._direct_chase(enemy.position, target_position, enemy.speed)

        state = self._states.setdefault(enemy.entity_id, EnemyNavigationState())
        self._update_stuck_state(state, current_position=enemy.position, dt=dt)
        state.repath_cooldown_seconds = max(0.0, state.repath_cooldown_seconds - dt)

        start_cell = self._world_to_cell(enemy.position, tile_size)
        goal_cell = self._world_to_cell(target_position, tile_size)
        start_cell = (
            self._nearest_walkable_cell(start_cell, blocking_grid, max_radius=3) or start_cell
        )
        goal_cell = self._nearest_walkable_cell(goal_cell, blocking_grid, max_radius=4) or goal_cell

        direct_velocity = self._direct_chase(enemy.position, target_position, enemy.speed)
        direct_speed = direct_velocity.length()
        direct_step_blocked = self._would_step_into_blocking(
            position=enemy.position,
            radius=enemy.radius,
            velocity=direct_velocity,
            dt=dt,
            grid=blocking_grid,
            tile_size=tile_size,
        )
        direct_line_clear = self._line_of_travel_clear(start_cell, goal_cell, blocking_grid)

        if state.using_pathfinding and direct_line_clear and not direct_step_blocked:
            self._clear_path_state(state)

        if not state.using_pathfinding:
            if (
                state.stuck_time_seconds >= self.stuck_seconds
                or direct_step_blocked
                or not direct_line_clear
            ):
                state.using_pathfinding = True
                state.repath_cooldown_seconds = 0.0
            else:
                self._record_attempt(
                    state,
                    position=enemy.position,
                    dt=dt,
                    speed=direct_speed,
                    was_direct=True,
                )
                return direct_velocity

        path_velocity = self._choose_path_velocity(
            state,
            enemy=enemy,
            start_cell=start_cell,
            goal_cell=goal_cell,
            blocking_grid=blocking_grid,
            tile_size=tile_size,
            dt=dt,
        )
        if path_velocity.length_squared() == 0.0:
            path_velocity = direct_velocity

        self._record_attempt(
            state,
            position=enemy.position,
            dt=dt,
            speed=path_velocity.length(),
            was_direct=False,
        )
        return path_velocity

    def _choose_path_velocity(
        self,
        state: EnemyNavigationState,
        *,
        enemy: Enemy,
        start_cell: GridCell,
        goal_cell: GridCell,
        blocking_grid: tuple[tuple[bool, ...], ...],
        tile_size: float,
        dt: float,
    ) -> Vec2:
        del dt

        should_repath = (
            state.target_cell != goal_cell
            or not state.path_cells
            or state.repath_cooldown_seconds <= 0.0
        )
        if should_repath:
            state.path_cells = []
            self._recompute_path(
                state,
                start_cell=start_cell,
                goal_cell=goal_cell,
                grid=blocking_grid,
            )
            state.target_cell = goal_cell
            state.repath_cooldown_seconds = self.repath_interval_seconds

        while state.path_cells and state.path_cells[0] == start_cell:
            state.path_cells.pop(0)

        next_cell = state.path_cells[0] if state.path_cells else goal_cell
        waypoint = self._cell_to_world_center(next_cell, tile_size)
        to_waypoint = waypoint - enemy.position
        if to_waypoint.length_squared() <= max(4.0, (tile_size * 0.18) ** 2):
            if state.path_cells:
                state.path_cells.pop(0)
            next_cell = state.path_cells[0] if state.path_cells else goal_cell
            waypoint = self._cell_to_world_center(next_cell, tile_size)
            to_waypoint = waypoint - enemy.position

        if to_waypoint.length_squared() == 0.0:
            return Vec2(0.0, 0.0)
        return to_waypoint.normalized() * enemy.speed

    def _update_stuck_state(
        self, state: EnemyNavigationState, *, current_position: Vec2, dt: float
    ) -> None:
        if (
            state.last_position is None
            or not state.last_attempt_was_direct
            or state.last_attempt_speed <= 0.0
            or state.last_dt <= 0.0
        ):
            state.stuck_time_seconds = 0.0
            return

        moved_distance = (current_position - state.last_position).length()
        min_progress = self.min_progress_per_second * state.last_dt
        if moved_distance <= min_progress:
            state.stuck_time_seconds += dt
        else:
            state.stuck_time_seconds = 0.0

    @staticmethod
    def _record_attempt(
        state: EnemyNavigationState,
        *,
        position: Vec2,
        dt: float,
        speed: float,
        was_direct: bool,
    ) -> None:
        state.last_position = position.copy()
        state.last_dt = max(0.0, dt)
        state.last_attempt_speed = max(0.0, speed)
        state.last_attempt_was_direct = was_direct

    @staticmethod
    def _clear_path_state(state: EnemyNavigationState) -> None:
        state.using_pathfinding = False
        state.path_cells.clear()
        state.target_cell = None
        state.repath_cooldown_seconds = 0.0

    def _recompute_path(
        self,
        state: EnemyNavigationState,
        *,
        start_cell: GridCell,
        goal_cell: GridCell,
        grid: tuple[tuple[bool, ...], ...],
    ) -> None:
        if self._path_requests_remaining <= 0:
            return
        self._path_requests_remaining -= 1

        path = self._a_star(start_cell, goal_cell, grid)
        if path:
            state.path_cells = path
        else:
            state.path_cells = []

    def _a_star(
        self,
        start: GridCell,
        goal: GridCell,
        grid: tuple[tuple[bool, ...], ...],
    ) -> list[GridCell]:
        if start == goal:
            return []

        if not self._is_walkable(start, grid) or not self._is_walkable(goal, grid):
            return []

        open_heap: list[tuple[int, int, GridCell]] = []
        heapq.heappush(open_heap, (0, 0, start))
        came_from: dict[GridCell, GridCell] = {}
        g_cost: dict[GridCell, int] = {start: 0}
        visited: set[GridCell] = set()
        tie_breaker = 1
        explored_nodes = 0

        while open_heap and explored_nodes < self.max_search_nodes:
            _, _, current = heapq.heappop(open_heap)
            if current in visited:
                continue
            visited.add(current)
            explored_nodes += 1

            if current == goal:
                return self._reconstruct_path(came_from, start, goal)

            for neighbor in self._neighbors_4(current):
                if not self._is_walkable(neighbor, grid) or neighbor in visited:
                    continue
                tentative = g_cost[current] + 1
                if tentative >= g_cost.get(neighbor, 1_000_000):
                    continue

                came_from[neighbor] = current
                g_cost[neighbor] = tentative
                heuristic = abs(goal[0] - neighbor[0]) + abs(goal[1] - neighbor[1])
                priority = tentative + heuristic
                heapq.heappush(open_heap, (priority, tie_breaker, neighbor))
                tie_breaker += 1

        return []

    @staticmethod
    def _reconstruct_path(
        came_from: dict[GridCell, GridCell],
        start: GridCell,
        goal: GridCell,
    ) -> list[GridCell]:
        current = goal
        path: list[GridCell] = [goal]
        while current in came_from:
            current = came_from[current]
            path.append(current)
            if current == start:
                break
        path.reverse()
        if path and path[0] == start:
            path = path[1:]
        return path

    @staticmethod
    def _neighbors_4(cell: GridCell) -> tuple[GridCell, GridCell, GridCell, GridCell]:
        col, row = cell
        return (
            (col + 1, row),
            (col - 1, row),
            (col, row + 1),
            (col, row - 1),
        )

    @staticmethod
    def _is_walkable(cell: GridCell, grid: tuple[tuple[bool, ...], ...]) -> bool:
        col, row = cell
        if row < 0 or col < 0:
            return False
        if row >= len(grid) or col >= len(grid[0]):
            return False
        return not grid[row][col]

    def _nearest_walkable_cell(
        self,
        origin: GridCell,
        grid: tuple[tuple[bool, ...], ...],
        *,
        max_radius: int,
    ) -> GridCell | None:
        if self._is_walkable(origin, grid):
            return origin

        origin_col, origin_row = origin
        for radius in range(1, max_radius + 1):
            min_col = origin_col - radius
            max_col = origin_col + radius
            min_row = origin_row - radius
            max_row = origin_row + radius

            for row in range(min_row, max_row + 1):
                for col in range(min_col, max_col + 1):
                    if row not in (min_row, max_row) and col not in (min_col, max_col):
                        continue
                    candidate = (col, row)
                    if self._is_walkable(candidate, grid):
                        return candidate
        return None

    def _would_step_into_blocking(
        self,
        *,
        position: Vec2,
        radius: float,
        velocity: Vec2,
        dt: float,
        grid: tuple[tuple[bool, ...], ...],
        tile_size: float,
    ) -> bool:
        if velocity.length_squared() == 0.0:
            return False
        next_position = position + (velocity * max(0.0, dt))
        return self._position_intersects_blocking(
            next_position,
            radius=radius,
            grid=grid,
            tile_size=tile_size,
        )

    def _position_intersects_blocking(
        self,
        position: Vec2,
        *,
        radius: float,
        grid: tuple[tuple[bool, ...], ...],
        tile_size: float,
    ) -> bool:
        min_col = int((position.x - radius) // tile_size)
        max_col = int((position.x + radius) // tile_size)
        min_row = int((position.y - radius) // tile_size)
        max_row = int((position.y + radius) // tile_size)

        grid_height = len(grid)
        grid_width = len(grid[0]) if grid_height > 0 else 0
        if grid_width == 0:
            return False

        if max_col < 0 or max_row < 0 or min_col >= grid_width or min_row >= grid_height:
            return False

        for row in range(max(0, min_row), min(grid_height - 1, max_row) + 1):
            for col in range(max(0, min_col), min(grid_width - 1, max_col) + 1):
                if grid[row][col]:
                    return True
        return False

    def _line_of_travel_clear(
        self,
        start: GridCell,
        goal: GridCell,
        grid: tuple[tuple[bool, ...], ...],
    ) -> bool:
        if start == goal:
            return True

        dx = goal[0] - start[0]
        dy = goal[1] - start[1]
        steps = max(abs(dx), abs(dy))
        if steps <= 0:
            return True

        for i in range(steps + 1):
            t = i / steps
            sample = (
                int(round(start[0] + dx * t)),
                int(round(start[1] + dy * t)),
            )
            if not self._is_walkable(sample, grid):
                return False
        return True

    @staticmethod
    def _direct_chase(current: Vec2, target: Vec2, speed: float) -> Vec2:
        delta = target - current
        if delta.length_squared() == 0.0:
            return Vec2(0.0, 0.0)
        return delta.normalized() * speed

    @staticmethod
    def _world_to_cell(position: Vec2, tile_size: float) -> GridCell:
        return (int(position.x // tile_size), int(position.y // tile_size))

    @staticmethod
    def _cell_to_world_center(cell: GridCell, tile_size: float) -> Vec2:
        col, row = cell
        return Vec2((col + 0.5) * tile_size, (row + 0.5) * tile_size)

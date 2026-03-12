from __future__ import annotations

from game.render.maps.types import CoordPatch, StructurePlacement, TilePlacement, TilesetCoord


def repeat_structure_placements(
    unit_placements: tuple[StructurePlacement, ...],
    *,
    unit_cols: int,
    unit_rows: int,
    repeat_cols: int,
    repeat_rows: int,
) -> tuple[StructurePlacement, ...]:
    placements: list[StructurePlacement] = []
    for tile_row in range(repeat_rows):
        for tile_col in range(repeat_cols):
            col_offset = tile_col * unit_cols
            row_offset = tile_row * unit_rows
            for placement in unit_placements:
                placements.append(
                    StructurePlacement(
                        structure_id=placement.structure_id,
                        anchor_col=placement.anchor_col + col_offset,
                        anchor_row=placement.anchor_row + row_offset,
                    )
                )
    return tuple(placements)


def repeat_tile_placements(
    unit_placements: tuple[TilePlacement, ...],
    *,
    unit_cols: int,
    unit_rows: int,
    repeat_cols: int,
    repeat_rows: int,
) -> tuple[TilePlacement, ...]:
    placements: list[TilePlacement] = []
    for tile_row in range(repeat_rows):
        for tile_col in range(repeat_cols):
            col_offset = tile_col * unit_cols
            row_offset = tile_row * unit_rows
            for placement in unit_placements:
                placements.append(
                    TilePlacement(
                        tile_id=placement.tile_id,
                        col=placement.col + col_offset,
                        row=placement.row + row_offset,
                    )
                )
    return tuple(placements)


def repeat_coord_grid(
    unit_grid: tuple[tuple[TilesetCoord, ...], ...],
    *,
    repeat_cols: int,
    repeat_rows: int,
) -> tuple[tuple[TilesetCoord, ...], ...]:
    repeated_rows: list[tuple[TilesetCoord, ...]] = []
    for _ in range(repeat_rows):
        for row in unit_grid:
            repeated_rows.append(tuple(coord for _ in range(repeat_cols) for coord in row))
    return tuple(repeated_rows)


def build_coord_patch_from_rect(
    patch_id: str,
    *,
    col_start: int,
    row_start: int,
    col_end: int,
    row_end: int,
) -> CoordPatch:
    if col_end < col_start or row_end < row_start:
        raise ValueError(f"Invalid patch bounds for {patch_id}.")

    rows: list[tuple[TilesetCoord, ...]] = []
    for row in range(row_start, row_end + 1):
        row_coords: list[TilesetCoord] = []
        for col in range(col_start, col_end + 1):
            row_coords.append((col, row))
        rows.append(tuple(row_coords))

    return CoordPatch(
        patch_id=patch_id,
        width=col_end - col_start + 1,
        height=row_end - row_start + 1,
        coords=tuple(rows),
    )


def stamp_coord_patch(
    layer: list[list[TilesetCoord]],
    patch: CoordPatch,
    anchor_col: int,
    anchor_row: int,
) -> None:
    if not layer:
        return

    rows = len(layer)
    cols = len(layer[0])
    if (
        anchor_col < 0
        or anchor_row < 0
        or anchor_col + patch.width > cols
        or anchor_row + patch.height > rows
    ):
        return

    for row_offset in range(patch.height):
        for col_offset in range(patch.width):
            layer[anchor_row + row_offset][anchor_col + col_offset] = patch.coords[row_offset][
                col_offset
            ]


def compute_internal_vertical_seam_cols(
    *,
    unit_cols: int,
    repeat_cols: int,
    seam_patch_width: int,
) -> tuple[int, ...]:
    return tuple(
        seam_index * unit_cols - (seam_patch_width // 2) for seam_index in range(1, repeat_cols)
    )


def build_continuous_vertical_starts(*, total_rows: int, patch_height: int) -> tuple[int, ...]:
    if patch_height <= 0:
        return ()

    max_start = max(0, total_rows - patch_height)
    starts: list[int] = []
    for raw_start in range(0, total_rows, patch_height):
        clamped = min(raw_start, max_start)
        if starts and starts[-1] == clamped:
            continue
        starts.append(clamped)
    if not starts:
        starts.append(0)
    return tuple(starts)


def stamp_coord_patch_along_internal_vertical_seams(
    *,
    layer: list[list[TilesetCoord]],
    seam_patch: CoordPatch,
    unit_cols: int,
    repeat_cols: int,
) -> None:
    seam_cols = compute_internal_vertical_seam_cols(
        unit_cols=unit_cols,
        repeat_cols=repeat_cols,
        seam_patch_width=seam_patch.width,
    )
    seam_rows = build_continuous_vertical_starts(
        total_rows=len(layer),
        patch_height=seam_patch.height,
    )

    for seam_col in seam_cols:
        for seam_row in seam_rows:
            stamp_coord_patch(layer, seam_patch, seam_col, seam_row)

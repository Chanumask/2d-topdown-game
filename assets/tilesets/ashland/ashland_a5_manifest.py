"""Ashland A5 tileset manifest.
16 columns x 32 rows. Rows 30-31 are empty in the source sheet.
Semantic labels are deterministic and intended as a clean first manifest for the tile renderer.
Refine individual tiles later without changing stable ids.

Current runtime note:
- Fixed-map rendering is the only active map path.
- The renderer currently uses this manifest only for tile-id -> sheet-coordinate lookup.
- Additional semantic/adjacency metadata below is retained as inactive data for future map layers.
"""

TILESET_NAME = "tf_A5_ashlands_2"
TILE_SIZE = 16
USED_ROWS = 30
EMPTY_ROWS = [30, 31]

ASHLAND_A5_MANIFEST = {
  "0,0": {
    "id": "ash_a5_r00_c00",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      0,
      0
    ],
    "group": "ground_round",
    "semantic": "rounded ash ground / soft-edged floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "round",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "1,0": {
    "id": "ash_a5_r00_c01",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      1,
      0
    ],
    "group": "ground_round",
    "semantic": "rounded ash ground / soft-edged floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "round",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "2,0": {
    "id": "ash_a5_r00_c02",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      2,
      0
    ],
    "group": "ground_round",
    "semantic": "rounded ash ground / soft-edged floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "round",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "3,0": {
    "id": "ash_a5_r00_c03",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      3,
      0
    ],
    "group": "ground_round",
    "semantic": "rounded ash ground / soft-edged floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "round",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "4,0": {
    "id": "ash_a5_r00_c04",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      4,
      0
    ],
    "group": "ground_round",
    "semantic": "rounded ash ground / soft-edged floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "round",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "5,0": {
    "id": "ash_a5_r00_c05",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      5,
      0
    ],
    "group": "ground_round",
    "semantic": "rounded ash ground / soft-edged floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "round",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "6,0": {
    "id": "ash_a5_r00_c06",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      6,
      0
    ],
    "group": "ground_round",
    "semantic": "rounded ash ground / soft-edged floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "round",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "7,0": {
    "id": "ash_a5_r00_c07",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      7,
      0
    ],
    "group": "ground_round",
    "semantic": "rounded ash ground / soft-edged floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "round",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "8,0": {
    "id": "ash_a5_r00_c08",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      8,
      0
    ],
    "group": "ground_round",
    "semantic": "rounded ash ground / soft-edged floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "round",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "9,0": {
    "id": "ash_a5_r00_c09",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      9,
      0
    ],
    "group": "ground_round",
    "semantic": "rounded ash ground / soft-edged floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "round",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "10,0": {
    "id": "ash_a5_r00_c10",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      10,
      0
    ],
    "group": "ground_round",
    "semantic": "rounded ash ground / soft-edged floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "round",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "11,0": {
    "id": "ash_a5_r00_c11",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      11,
      0
    ],
    "group": "ground_round",
    "semantic": "rounded ash ground / soft-edged floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "round",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "12,0": {
    "id": "ash_a5_r00_c12",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      12,
      0
    ],
    "group": "ground_round",
    "semantic": "rounded ash ground / soft-edged floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "round",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "13,0": {
    "id": "ash_a5_r00_c13",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      13,
      0
    ],
    "group": "ground_round",
    "semantic": "rounded ash ground / soft-edged floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "round",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "14,0": {
    "id": "ash_a5_r00_c14",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      14,
      0
    ],
    "group": "ground_round",
    "semantic": "rounded ash ground / soft-edged floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "round",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "15,0": {
    "id": "ash_a5_r00_c15",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      15,
      0
    ],
    "group": "ground_round",
    "semantic": "rounded ash ground / soft-edged floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "round",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "0,1": {
    "id": "ash_a5_r01_c00",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      0,
      1
    ],
    "group": "ground_round",
    "semantic": "rounded ash ground / soft-edged floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "round",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "1,1": {
    "id": "ash_a5_r01_c01",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      1,
      1
    ],
    "group": "ground_round",
    "semantic": "rounded ash ground / soft-edged floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "round",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "2,1": {
    "id": "ash_a5_r01_c02",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      2,
      1
    ],
    "group": "ground_round",
    "semantic": "rounded ash ground / soft-edged floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "round",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "3,1": {
    "id": "ash_a5_r01_c03",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      3,
      1
    ],
    "group": "ground_round",
    "semantic": "rounded ash ground / soft-edged floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "round",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "4,1": {
    "id": "ash_a5_r01_c04",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      4,
      1
    ],
    "group": "ground_round",
    "semantic": "rounded ash ground / soft-edged floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "round",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "5,1": {
    "id": "ash_a5_r01_c05",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      5,
      1
    ],
    "group": "ground_round",
    "semantic": "rounded ash ground / soft-edged floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "round",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "6,1": {
    "id": "ash_a5_r01_c06",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      6,
      1
    ],
    "group": "ground_round",
    "semantic": "rounded ash ground / soft-edged floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "round",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "7,1": {
    "id": "ash_a5_r01_c07",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      7,
      1
    ],
    "group": "ground_round",
    "semantic": "rounded ash ground / soft-edged floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "round",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "8,1": {
    "id": "ash_a5_r01_c08",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      8,
      1
    ],
    "group": "ground_round",
    "semantic": "rounded ash ground / soft-edged floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "round",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "9,1": {
    "id": "ash_a5_r01_c09",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      9,
      1
    ],
    "group": "ground_round",
    "semantic": "rounded ash ground / soft-edged floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "round",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "10,1": {
    "id": "ash_a5_r01_c10",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      10,
      1
    ],
    "group": "ground_round",
    "semantic": "rounded ash ground / soft-edged floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "round",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "11,1": {
    "id": "ash_a5_r01_c11",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      11,
      1
    ],
    "group": "ground_round",
    "semantic": "rounded ash ground / soft-edged floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "round",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "12,1": {
    "id": "ash_a5_r01_c12",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      12,
      1
    ],
    "group": "ground_round",
    "semantic": "rounded ash ground / soft-edged floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "round",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "13,1": {
    "id": "ash_a5_r01_c13",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      13,
      1
    ],
    "group": "ground_round",
    "semantic": "rounded ash ground / soft-edged floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "round",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "14,1": {
    "id": "ash_a5_r01_c14",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      14,
      1
    ],
    "group": "ground_round",
    "semantic": "rounded ash ground / soft-edged floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "round",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "15,1": {
    "id": "ash_a5_r01_c15",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      15,
      1
    ],
    "group": "ground_round",
    "semantic": "rounded ash ground / soft-edged floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "round",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "0,2": {
    "id": "ash_a5_r02_c00",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      0,
      2
    ],
    "group": "ground_square",
    "semantic": "square ash ground / packed floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "square",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "1,2": {
    "id": "ash_a5_r02_c01",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      1,
      2
    ],
    "group": "ground_square",
    "semantic": "square ash ground / packed floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "square",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "2,2": {
    "id": "ash_a5_r02_c02",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      2,
      2
    ],
    "group": "ground_square",
    "semantic": "square ash ground / packed floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "square",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "3,2": {
    "id": "ash_a5_r02_c03",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      3,
      2
    ],
    "group": "ground_square",
    "semantic": "square ash ground / packed floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "square",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "4,2": {
    "id": "ash_a5_r02_c04",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      4,
      2
    ],
    "group": "ground_square",
    "semantic": "square ash ground / packed floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "square",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "5,2": {
    "id": "ash_a5_r02_c05",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      5,
      2
    ],
    "group": "ground_square",
    "semantic": "square ash ground / packed floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "square",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "6,2": {
    "id": "ash_a5_r02_c06",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      6,
      2
    ],
    "group": "ground_square",
    "semantic": "square ash ground / packed floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "square",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "7,2": {
    "id": "ash_a5_r02_c07",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      7,
      2
    ],
    "group": "ground_square",
    "semantic": "square ash ground / packed floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "square",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "8,2": {
    "id": "ash_a5_r02_c08",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      8,
      2
    ],
    "group": "ground_square",
    "semantic": "square ash ground / packed floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "square",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "9,2": {
    "id": "ash_a5_r02_c09",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      9,
      2
    ],
    "group": "ground_square",
    "semantic": "square ash ground / packed floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "square",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "10,2": {
    "id": "ash_a5_r02_c10",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      10,
      2
    ],
    "group": "ground_square",
    "semantic": "square ash ground / packed floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "square",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "11,2": {
    "id": "ash_a5_r02_c11",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      11,
      2
    ],
    "group": "ground_square",
    "semantic": "square ash ground / packed floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "square",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "12,2": {
    "id": "ash_a5_r02_c12",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      12,
      2
    ],
    "group": "ground_square",
    "semantic": "square ash ground / packed floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "square",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "13,2": {
    "id": "ash_a5_r02_c13",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      13,
      2
    ],
    "group": "ground_square",
    "semantic": "square ash ground / packed floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "square",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "14,2": {
    "id": "ash_a5_r02_c14",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      14,
      2
    ],
    "group": "ground_square",
    "semantic": "square ash ground / packed floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "square",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "15,2": {
    "id": "ash_a5_r02_c15",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      15,
      2
    ],
    "group": "ground_square",
    "semantic": "square ash ground / packed floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "square",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "0,3": {
    "id": "ash_a5_r03_c00",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      0,
      3
    ],
    "group": "ground_square",
    "semantic": "square ash ground / packed floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "square",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "1,3": {
    "id": "ash_a5_r03_c01",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      1,
      3
    ],
    "group": "ground_square",
    "semantic": "square ash ground / packed floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "square",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "2,3": {
    "id": "ash_a5_r03_c02",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      2,
      3
    ],
    "group": "ground_square",
    "semantic": "square ash ground / packed floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "square",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "3,3": {
    "id": "ash_a5_r03_c03",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      3,
      3
    ],
    "group": "ground_square",
    "semantic": "square ash ground / packed floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "square",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "4,3": {
    "id": "ash_a5_r03_c04",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      4,
      3
    ],
    "group": "ground_square",
    "semantic": "square ash ground / packed floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "square",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "5,3": {
    "id": "ash_a5_r03_c05",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      5,
      3
    ],
    "group": "ground_square",
    "semantic": "square ash ground / packed floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "square",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "6,3": {
    "id": "ash_a5_r03_c06",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      6,
      3
    ],
    "group": "ground_square",
    "semantic": "square ash ground / packed floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "square",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "7,3": {
    "id": "ash_a5_r03_c07",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      7,
      3
    ],
    "group": "ground_square",
    "semantic": "square ash ground / packed floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "square",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "8,3": {
    "id": "ash_a5_r03_c08",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      8,
      3
    ],
    "group": "ground_square",
    "semantic": "square ash ground / packed floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "square",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "9,3": {
    "id": "ash_a5_r03_c09",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      9,
      3
    ],
    "group": "ground_square",
    "semantic": "square ash ground / packed floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "square",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "10,3": {
    "id": "ash_a5_r03_c10",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      10,
      3
    ],
    "group": "ground_square",
    "semantic": "square ash ground / packed floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "square",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "11,3": {
    "id": "ash_a5_r03_c11",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      11,
      3
    ],
    "group": "ground_square",
    "semantic": "square ash ground / packed floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "square",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "12,3": {
    "id": "ash_a5_r03_c12",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      12,
      3
    ],
    "group": "ground_square",
    "semantic": "square ash ground / packed floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "square",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "13,3": {
    "id": "ash_a5_r03_c13",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      13,
      3
    ],
    "group": "ground_square",
    "semantic": "square ash ground / packed floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "square",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "14,3": {
    "id": "ash_a5_r03_c14",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      14,
      3
    ],
    "group": "ground_square",
    "semantic": "square ash ground / packed floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "square",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "15,3": {
    "id": "ash_a5_r03_c15",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      15,
      3
    ],
    "group": "ground_square",
    "semantic": "square ash ground / packed floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "square",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "0,4": {
    "id": "ash_a5_r04_c00",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      0,
      4
    ],
    "group": "ground_dark",
    "semantic": "dark ash ground / scorched floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "dark",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "1,4": {
    "id": "ash_a5_r04_c01",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      1,
      4
    ],
    "group": "ground_dark",
    "semantic": "dark ash ground / scorched floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "dark",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "2,4": {
    "id": "ash_a5_r04_c02",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      2,
      4
    ],
    "group": "ground_dark",
    "semantic": "dark ash ground / scorched floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "dark",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "3,4": {
    "id": "ash_a5_r04_c03",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      3,
      4
    ],
    "group": "ground_dark",
    "semantic": "dark ash ground / scorched floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "dark",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "4,4": {
    "id": "ash_a5_r04_c04",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      4,
      4
    ],
    "group": "ground_dark",
    "semantic": "dark ash ground / scorched floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "dark",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "5,4": {
    "id": "ash_a5_r04_c05",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      5,
      4
    ],
    "group": "ground_dark",
    "semantic": "dark ash ground / scorched floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "dark",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "6,4": {
    "id": "ash_a5_r04_c06",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      6,
      4
    ],
    "group": "ground_dark",
    "semantic": "dark ash ground / scorched floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "dark",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "7,4": {
    "id": "ash_a5_r04_c07",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      7,
      4
    ],
    "group": "ground_dark",
    "semantic": "dark ash ground / scorched floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "dark",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "8,4": {
    "id": "ash_a5_r04_c08",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      8,
      4
    ],
    "group": "ground_dark",
    "semantic": "dark ash ground / scorched floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "dark",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "9,4": {
    "id": "ash_a5_r04_c09",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      9,
      4
    ],
    "group": "ground_dark",
    "semantic": "dark ash ground / scorched floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "dark",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "10,4": {
    "id": "ash_a5_r04_c10",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      10,
      4
    ],
    "group": "ground_dark",
    "semantic": "dark ash ground / scorched floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "dark",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "11,4": {
    "id": "ash_a5_r04_c11",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      11,
      4
    ],
    "group": "ground_dark",
    "semantic": "dark ash ground / scorched floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "dark",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "12,4": {
    "id": "ash_a5_r04_c12",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      12,
      4
    ],
    "group": "ground_dark",
    "semantic": "dark ash ground / scorched floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "dark",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "13,4": {
    "id": "ash_a5_r04_c13",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      13,
      4
    ],
    "group": "ground_dark",
    "semantic": "dark ash ground / scorched floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "dark",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "14,4": {
    "id": "ash_a5_r04_c14",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      14,
      4
    ],
    "group": "ground_dark",
    "semantic": "dark ash ground / scorched floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "dark",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "15,4": {
    "id": "ash_a5_r04_c15",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      15,
      4
    ],
    "group": "ground_dark",
    "semantic": "dark ash ground / scorched floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "dark",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "0,5": {
    "id": "ash_a5_r05_c00",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      0,
      5
    ],
    "group": "ground_dark",
    "semantic": "dark ash ground / scorched floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "dark",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "1,5": {
    "id": "ash_a5_r05_c01",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      1,
      5
    ],
    "group": "ground_dark",
    "semantic": "dark ash ground / scorched floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "dark",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "2,5": {
    "id": "ash_a5_r05_c02",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      2,
      5
    ],
    "group": "ground_dark",
    "semantic": "dark ash ground / scorched floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "dark",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "3,5": {
    "id": "ash_a5_r05_c03",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      3,
      5
    ],
    "group": "ground_dark",
    "semantic": "dark ash ground / scorched floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "dark",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "4,5": {
    "id": "ash_a5_r05_c04",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      4,
      5
    ],
    "group": "ground_dark",
    "semantic": "dark ash ground / scorched floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "dark",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "5,5": {
    "id": "ash_a5_r05_c05",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      5,
      5
    ],
    "group": "ground_dark",
    "semantic": "dark ash ground / scorched floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "dark",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "6,5": {
    "id": "ash_a5_r05_c06",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      6,
      5
    ],
    "group": "ground_dark",
    "semantic": "dark ash ground / scorched floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "dark",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "7,5": {
    "id": "ash_a5_r05_c07",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      7,
      5
    ],
    "group": "ground_dark",
    "semantic": "dark ash ground / scorched floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "dark",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "8,5": {
    "id": "ash_a5_r05_c08",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      8,
      5
    ],
    "group": "ground_dark",
    "semantic": "dark ash ground / scorched floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "dark",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "9,5": {
    "id": "ash_a5_r05_c09",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      9,
      5
    ],
    "group": "ground_dark",
    "semantic": "dark ash ground / scorched floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "dark",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "10,5": {
    "id": "ash_a5_r05_c10",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      10,
      5
    ],
    "group": "ground_dark",
    "semantic": "dark ash ground / scorched floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "dark",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "11,5": {
    "id": "ash_a5_r05_c11",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      11,
      5
    ],
    "group": "ground_dark",
    "semantic": "dark ash ground / scorched floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "dark",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "12,5": {
    "id": "ash_a5_r05_c12",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      12,
      5
    ],
    "group": "ground_dark",
    "semantic": "dark ash ground / scorched floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "dark",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "13,5": {
    "id": "ash_a5_r05_c13",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      13,
      5
    ],
    "group": "ground_dark",
    "semantic": "dark ash ground / scorched floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "dark",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "14,5": {
    "id": "ash_a5_r05_c14",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      14,
      5
    ],
    "group": "ground_dark",
    "semantic": "dark ash ground / scorched floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "dark",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "15,5": {
    "id": "ash_a5_r05_c15",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      15,
      5
    ],
    "group": "ground_dark",
    "semantic": "dark ash ground / scorched floor variant",
    "walkable_default": True,
    "tags": [
      "ground",
      "dark",
      "ash"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "0,6": {
    "id": "ash_a5_r06_c00",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      0,
      6
    ],
    "group": "lava_small",
    "semantic": "small lava vent / molten accent tile",
    "walkable_default": False,
    "tags": [
      "lava",
      "hazard",
      "accent"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "1,6": {
    "id": "ash_a5_r06_c01",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      1,
      6
    ],
    "group": "lava_small",
    "semantic": "small lava vent / molten accent tile",
    "walkable_default": False,
    "tags": [
      "lava",
      "hazard",
      "accent"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "2,6": {
    "id": "ash_a5_r06_c02",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      2,
      6
    ],
    "group": "lava_small",
    "semantic": "small lava vent / molten accent tile",
    "walkable_default": False,
    "tags": [
      "lava",
      "hazard",
      "accent"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "3,6": {
    "id": "ash_a5_r06_c03",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      3,
      6
    ],
    "group": "lava_small",
    "semantic": "small lava vent / molten accent tile",
    "walkable_default": False,
    "tags": [
      "lava",
      "hazard",
      "accent"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "4,6": {
    "id": "ash_a5_r06_c04",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      4,
      6
    ],
    "group": "lava_small",
    "semantic": "small lava vent / molten accent tile",
    "walkable_default": False,
    "tags": [
      "lava",
      "hazard",
      "accent"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "5,6": {
    "id": "ash_a5_r06_c05",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      5,
      6
    ],
    "group": "lava_small",
    "semantic": "small lava vent / molten accent tile",
    "walkable_default": False,
    "tags": [
      "lava",
      "hazard",
      "accent"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "6,6": {
    "id": "ash_a5_r06_c06",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      6,
      6
    ],
    "group": "lava_small",
    "semantic": "small lava vent / molten accent tile",
    "walkable_default": False,
    "tags": [
      "lava",
      "hazard",
      "accent"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "7,6": {
    "id": "ash_a5_r06_c07",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      7,
      6
    ],
    "group": "lava_small",
    "semantic": "small lava vent / molten accent tile",
    "walkable_default": False,
    "tags": [
      "lava",
      "hazard",
      "accent"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "8,6": {
    "id": "ash_a5_r06_c08",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      8,
      6
    ],
    "group": "lava_small",
    "semantic": "small lava vent / molten accent tile",
    "walkable_default": False,
    "tags": [
      "lava",
      "hazard",
      "accent"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "9,6": {
    "id": "ash_a5_r06_c09",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      9,
      6
    ],
    "group": "lava_small",
    "semantic": "small lava vent / molten accent tile",
    "walkable_default": False,
    "tags": [
      "lava",
      "hazard",
      "accent"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "10,6": {
    "id": "ash_a5_r06_c10",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      10,
      6
    ],
    "group": "lava_small",
    "semantic": "small lava vent / molten accent tile",
    "walkable_default": False,
    "tags": [
      "lava",
      "hazard",
      "accent"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "11,6": {
    "id": "ash_a5_r06_c11",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      11,
      6
    ],
    "group": "lava_small",
    "semantic": "small lava vent / molten accent tile",
    "walkable_default": False,
    "tags": [
      "lava",
      "hazard",
      "accent"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "12,6": {
    "id": "ash_a5_r06_c12",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      12,
      6
    ],
    "group": "lava_small",
    "semantic": "small lava vent / molten accent tile",
    "walkable_default": False,
    "tags": [
      "lava",
      "hazard",
      "accent"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "13,6": {
    "id": "ash_a5_r06_c13",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      13,
      6
    ],
    "group": "lava_small",
    "semantic": "small lava vent / molten accent tile",
    "walkable_default": False,
    "tags": [
      "lava",
      "hazard",
      "accent"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "14,6": {
    "id": "ash_a5_r06_c14",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      14,
      6
    ],
    "group": "lava_small",
    "semantic": "small lava vent / molten accent tile",
    "walkable_default": False,
    "tags": [
      "lava",
      "hazard",
      "accent"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "15,6": {
    "id": "ash_a5_r06_c15",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      15,
      6
    ],
    "group": "lava_small",
    "semantic": "small lava vent / molten accent tile",
    "walkable_default": False,
    "tags": [
      "lava",
      "hazard",
      "accent"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "0,7": {
    "id": "ash_a5_r07_c00",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      0,
      7
    ],
    "group": "lava_small",
    "semantic": "small lava vent / molten accent tile",
    "walkable_default": False,
    "tags": [
      "lava",
      "hazard",
      "accent"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "1,7": {
    "id": "ash_a5_r07_c01",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      1,
      7
    ],
    "group": "lava_small",
    "semantic": "small lava vent / molten accent tile",
    "walkable_default": False,
    "tags": [
      "lava",
      "hazard",
      "accent"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "2,7": {
    "id": "ash_a5_r07_c02",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      2,
      7
    ],
    "group": "lava_small",
    "semantic": "small lava vent / molten accent tile",
    "walkable_default": False,
    "tags": [
      "lava",
      "hazard",
      "accent"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "3,7": {
    "id": "ash_a5_r07_c03",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      3,
      7
    ],
    "group": "lava_small",
    "semantic": "small lava vent / molten accent tile",
    "walkable_default": False,
    "tags": [
      "lava",
      "hazard",
      "accent"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "4,7": {
    "id": "ash_a5_r07_c04",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      4,
      7
    ],
    "group": "lava_small",
    "semantic": "small lava vent / molten accent tile",
    "walkable_default": False,
    "tags": [
      "lava",
      "hazard",
      "accent"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "5,7": {
    "id": "ash_a5_r07_c05",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      5,
      7
    ],
    "group": "lava_small",
    "semantic": "small lava vent / molten accent tile",
    "walkable_default": False,
    "tags": [
      "lava",
      "hazard",
      "accent"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "6,7": {
    "id": "ash_a5_r07_c06",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      6,
      7
    ],
    "group": "lava_small",
    "semantic": "small lava vent / molten accent tile",
    "walkable_default": False,
    "tags": [
      "lava",
      "hazard",
      "accent"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "7,7": {
    "id": "ash_a5_r07_c07",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      7,
      7
    ],
    "group": "lava_small",
    "semantic": "small lava vent / molten accent tile",
    "walkable_default": False,
    "tags": [
      "lava",
      "hazard",
      "accent"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "8,7": {
    "id": "ash_a5_r07_c08",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      8,
      7
    ],
    "group": "lava_small",
    "semantic": "small lava vent / molten accent tile",
    "walkable_default": False,
    "tags": [
      "lava",
      "hazard",
      "accent"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "9,7": {
    "id": "ash_a5_r07_c09",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      9,
      7
    ],
    "group": "lava_small",
    "semantic": "small lava vent / molten accent tile",
    "walkable_default": False,
    "tags": [
      "lava",
      "hazard",
      "accent"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "10,7": {
    "id": "ash_a5_r07_c10",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      10,
      7
    ],
    "group": "lava_small",
    "semantic": "small lava vent / molten accent tile",
    "walkable_default": False,
    "tags": [
      "lava",
      "hazard",
      "accent"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "11,7": {
    "id": "ash_a5_r07_c11",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      11,
      7
    ],
    "group": "lava_small",
    "semantic": "small lava vent / molten accent tile",
    "walkable_default": False,
    "tags": [
      "lava",
      "hazard",
      "accent"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "12,7": {
    "id": "ash_a5_r07_c12",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      12,
      7
    ],
    "group": "lava_small",
    "semantic": "small lava vent / molten accent tile",
    "walkable_default": False,
    "tags": [
      "lava",
      "hazard",
      "accent"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "13,7": {
    "id": "ash_a5_r07_c13",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      13,
      7
    ],
    "group": "lava_small",
    "semantic": "small lava vent / molten accent tile",
    "walkable_default": False,
    "tags": [
      "lava",
      "hazard",
      "accent"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "14,7": {
    "id": "ash_a5_r07_c14",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      14,
      7
    ],
    "group": "lava_small",
    "semantic": "small lava vent / molten accent tile",
    "walkable_default": False,
    "tags": [
      "lava",
      "hazard",
      "accent"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "15,7": {
    "id": "ash_a5_r07_c15",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      15,
      7
    ],
    "group": "lava_small",
    "semantic": "small lava vent / molten accent tile",
    "walkable_default": False,
    "tags": [
      "lava",
      "hazard",
      "accent"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "0,8": {
    "id": "ash_a5_r08_c00",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      0,
      8
    ],
    "group": "lava_full",
    "semantic": "full lava pool / molten floor tile",
    "walkable_default": False,
    "tags": [
      "lava",
      "hazard",
      "pool"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "1,8": {
    "id": "ash_a5_r08_c01",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      1,
      8
    ],
    "group": "lava_full",
    "semantic": "full lava pool / molten floor tile",
    "walkable_default": False,
    "tags": [
      "lava",
      "hazard",
      "pool"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "2,8": {
    "id": "ash_a5_r08_c02",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      2,
      8
    ],
    "group": "lava_full",
    "semantic": "full lava pool / molten floor tile",
    "walkable_default": False,
    "tags": [
      "lava",
      "hazard",
      "pool"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "3,8": {
    "id": "ash_a5_r08_c03",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      3,
      8
    ],
    "group": "lava_full",
    "semantic": "full lava pool / molten floor tile",
    "walkable_default": False,
    "tags": [
      "lava",
      "hazard",
      "pool"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "4,8": {
    "id": "ash_a5_r08_c04",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      4,
      8
    ],
    "group": "lava_full",
    "semantic": "full lava pool / molten floor tile",
    "walkable_default": False,
    "tags": [
      "lava",
      "hazard",
      "pool"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "5,8": {
    "id": "ash_a5_r08_c05",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      5,
      8
    ],
    "group": "lava_full",
    "semantic": "full lava pool / molten floor tile",
    "walkable_default": False,
    "tags": [
      "lava",
      "hazard",
      "pool"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "6,8": {
    "id": "ash_a5_r08_c06",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      6,
      8
    ],
    "group": "lava_full",
    "semantic": "full lava pool / molten floor tile",
    "walkable_default": False,
    "tags": [
      "lava",
      "hazard",
      "pool"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "7,8": {
    "id": "ash_a5_r08_c07",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      7,
      8
    ],
    "group": "lava_full",
    "semantic": "full lava pool / molten floor tile",
    "walkable_default": False,
    "tags": [
      "lava",
      "hazard",
      "pool"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "8,8": {
    "id": "ash_a5_r08_c08",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      8,
      8
    ],
    "group": "lava_full",
    "semantic": "full lava pool / molten floor tile",
    "walkable_default": False,
    "tags": [
      "lava",
      "hazard",
      "pool"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "9,8": {
    "id": "ash_a5_r08_c09",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      9,
      8
    ],
    "group": "lava_full",
    "semantic": "full lava pool / molten floor tile",
    "walkable_default": False,
    "tags": [
      "lava",
      "hazard",
      "pool"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "10,8": {
    "id": "ash_a5_r08_c10",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      10,
      8
    ],
    "group": "lava_full",
    "semantic": "full lava pool / molten floor tile",
    "walkable_default": False,
    "tags": [
      "lava",
      "hazard",
      "pool"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "11,8": {
    "id": "ash_a5_r08_c11",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      11,
      8
    ],
    "group": "lava_full",
    "semantic": "full lava pool / molten floor tile",
    "walkable_default": False,
    "tags": [
      "lava",
      "hazard",
      "pool"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "12,8": {
    "id": "ash_a5_r08_c12",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      12,
      8
    ],
    "group": "lava_full",
    "semantic": "full lava pool / molten floor tile",
    "walkable_default": False,
    "tags": [
      "lava",
      "hazard",
      "pool"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "13,8": {
    "id": "ash_a5_r08_c13",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      13,
      8
    ],
    "group": "lava_full",
    "semantic": "full lava pool / molten floor tile",
    "walkable_default": False,
    "tags": [
      "lava",
      "hazard",
      "pool"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "14,8": {
    "id": "ash_a5_r08_c14",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      14,
      8
    ],
    "group": "lava_full",
    "semantic": "full lava pool / molten floor tile",
    "walkable_default": False,
    "tags": [
      "lava",
      "hazard",
      "pool"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "15,8": {
    "id": "ash_a5_r08_c15",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      15,
      8
    ],
    "group": "lava_full",
    "semantic": "full lava pool / molten floor tile",
    "walkable_default": False,
    "tags": [
      "lava",
      "hazard",
      "pool"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "0,9": {
    "id": "ash_a5_r09_c00",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      0,
      9
    ],
    "group": "lava_full",
    "semantic": "full lava pool / molten floor tile",
    "walkable_default": False,
    "tags": [
      "lava",
      "hazard",
      "pool"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "1,9": {
    "id": "ash_a5_r09_c01",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      1,
      9
    ],
    "group": "lava_full",
    "semantic": "full lava pool / molten floor tile",
    "walkable_default": False,
    "tags": [
      "lava",
      "hazard",
      "pool"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "2,9": {
    "id": "ash_a5_r09_c02",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      2,
      9
    ],
    "group": "lava_full",
    "semantic": "full lava pool / molten floor tile",
    "walkable_default": False,
    "tags": [
      "lava",
      "hazard",
      "pool"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "3,9": {
    "id": "ash_a5_r09_c03",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      3,
      9
    ],
    "group": "lava_full",
    "semantic": "full lava pool / molten floor tile",
    "walkable_default": False,
    "tags": [
      "lava",
      "hazard",
      "pool"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "4,9": {
    "id": "ash_a5_r09_c04",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      4,
      9
    ],
    "group": "lava_full",
    "semantic": "full lava pool / molten floor tile",
    "walkable_default": False,
    "tags": [
      "lava",
      "hazard",
      "pool"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "5,9": {
    "id": "ash_a5_r09_c05",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      5,
      9
    ],
    "group": "lava_full",
    "semantic": "full lava pool / molten floor tile",
    "walkable_default": False,
    "tags": [
      "lava",
      "hazard",
      "pool"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "6,9": {
    "id": "ash_a5_r09_c06",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      6,
      9
    ],
    "group": "lava_full",
    "semantic": "full lava pool / molten floor tile",
    "walkable_default": False,
    "tags": [
      "lava",
      "hazard",
      "pool"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "7,9": {
    "id": "ash_a5_r09_c07",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      7,
      9
    ],
    "group": "lava_full",
    "semantic": "full lava pool / molten floor tile",
    "walkable_default": False,
    "tags": [
      "lava",
      "hazard",
      "pool"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "8,9": {
    "id": "ash_a5_r09_c08",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      8,
      9
    ],
    "group": "lava_full",
    "semantic": "full lava pool / molten floor tile",
    "walkable_default": False,
    "tags": [
      "lava",
      "hazard",
      "pool"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "9,9": {
    "id": "ash_a5_r09_c09",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      9,
      9
    ],
    "group": "lava_full",
    "semantic": "full lava pool / molten floor tile",
    "walkable_default": False,
    "tags": [
      "lava",
      "hazard",
      "pool"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "10,9": {
    "id": "ash_a5_r09_c10",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      10,
      9
    ],
    "group": "lava_full",
    "semantic": "full lava pool / molten floor tile",
    "walkable_default": False,
    "tags": [
      "lava",
      "hazard",
      "pool"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "11,9": {
    "id": "ash_a5_r09_c11",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      11,
      9
    ],
    "group": "lava_full",
    "semantic": "full lava pool / molten floor tile",
    "walkable_default": False,
    "tags": [
      "lava",
      "hazard",
      "pool"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "12,9": {
    "id": "ash_a5_r09_c12",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      12,
      9
    ],
    "group": "lava_full",
    "semantic": "full lava pool / molten floor tile",
    "walkable_default": False,
    "tags": [
      "lava",
      "hazard",
      "pool"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "13,9": {
    "id": "ash_a5_r09_c13",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      13,
      9
    ],
    "group": "lava_full",
    "semantic": "full lava pool / molten floor tile",
    "walkable_default": False,
    "tags": [
      "lava",
      "hazard",
      "pool"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "14,9": {
    "id": "ash_a5_r09_c14",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      14,
      9
    ],
    "group": "lava_full",
    "semantic": "full lava pool / molten floor tile",
    "walkable_default": False,
    "tags": [
      "lava",
      "hazard",
      "pool"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "15,9": {
    "id": "ash_a5_r09_c15",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      15,
      9
    ],
    "group": "lava_full",
    "semantic": "full lava pool / molten floor tile",
    "walkable_default": False,
    "tags": [
      "lava",
      "hazard",
      "pool"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "0,10": {
    "id": "ash_a5_r10_c00",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      0,
      10
    ],
    "group": "path_cobble",
    "semantic": "cobble/stone path tile",
    "walkable_default": True,
    "tags": [
      "path",
      "stone",
      "walkable"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "1,10": {
    "id": "ash_a5_r10_c01",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      1,
      10
    ],
    "group": "path_cobble",
    "semantic": "cobble/stone path tile",
    "walkable_default": True,
    "tags": [
      "path",
      "stone",
      "walkable"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "2,10": {
    "id": "ash_a5_r10_c02",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      2,
      10
    ],
    "group": "path_cobble",
    "semantic": "cobble/stone path tile",
    "walkable_default": True,
    "tags": [
      "path",
      "stone",
      "walkable"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "3,10": {
    "id": "ash_a5_r10_c03",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      3,
      10
    ],
    "group": "path_cobble",
    "semantic": "cobble/stone path tile",
    "walkable_default": True,
    "tags": [
      "path",
      "stone",
      "walkable"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "4,10": {
    "id": "ash_a5_r10_c04",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      4,
      10
    ],
    "group": "path_cobble",
    "semantic": "cobble/stone path tile",
    "walkable_default": True,
    "tags": [
      "path",
      "stone",
      "walkable"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "5,10": {
    "id": "ash_a5_r10_c05",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      5,
      10
    ],
    "group": "path_cobble",
    "semantic": "cobble/stone path tile",
    "walkable_default": True,
    "tags": [
      "path",
      "stone",
      "walkable"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "6,10": {
    "id": "ash_a5_r10_c06",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      6,
      10
    ],
    "group": "path_cobble",
    "semantic": "cobble/stone path tile",
    "walkable_default": True,
    "tags": [
      "path",
      "stone",
      "walkable"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "7,10": {
    "id": "ash_a5_r10_c07",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      7,
      10
    ],
    "group": "path_cobble",
    "semantic": "cobble/stone path tile",
    "walkable_default": True,
    "tags": [
      "path",
      "stone",
      "walkable"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "8,10": {
    "id": "ash_a5_r10_c08",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      8,
      10
    ],
    "group": "path_cobble",
    "semantic": "cobble/stone path tile",
    "walkable_default": True,
    "tags": [
      "path",
      "stone",
      "walkable"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "9,10": {
    "id": "ash_a5_r10_c09",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      9,
      10
    ],
    "group": "path_cobble",
    "semantic": "cobble/stone path tile",
    "walkable_default": True,
    "tags": [
      "path",
      "stone",
      "walkable"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "10,10": {
    "id": "ash_a5_r10_c10",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      10,
      10
    ],
    "group": "path_cobble",
    "semantic": "cobble/stone path tile",
    "walkable_default": True,
    "tags": [
      "path",
      "stone",
      "walkable"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "11,10": {
    "id": "ash_a5_r10_c11",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      11,
      10
    ],
    "group": "path_cobble",
    "semantic": "cobble/stone path tile",
    "walkable_default": True,
    "tags": [
      "path",
      "stone",
      "walkable"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "12,10": {
    "id": "ash_a5_r10_c12",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      12,
      10
    ],
    "group": "path_cobble",
    "semantic": "cobble/stone path tile",
    "walkable_default": True,
    "tags": [
      "path",
      "stone",
      "walkable"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "13,10": {
    "id": "ash_a5_r10_c13",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      13,
      10
    ],
    "group": "path_cobble",
    "semantic": "cobble/stone path tile",
    "walkable_default": True,
    "tags": [
      "path",
      "stone",
      "walkable"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "14,10": {
    "id": "ash_a5_r10_c14",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      14,
      10
    ],
    "group": "path_cobble",
    "semantic": "cobble/stone path tile",
    "walkable_default": True,
    "tags": [
      "path",
      "stone",
      "walkable"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "15,10": {
    "id": "ash_a5_r10_c15",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      15,
      10
    ],
    "group": "path_cobble",
    "semantic": "cobble/stone path tile",
    "walkable_default": True,
    "tags": [
      "path",
      "stone",
      "walkable"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "0,11": {
    "id": "ash_a5_r11_c00",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      0,
      11
    ],
    "group": "path_cobble",
    "semantic": "cobble/stone path tile",
    "walkable_default": True,
    "tags": [
      "path",
      "stone",
      "walkable"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "1,11": {
    "id": "ash_a5_r11_c01",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      1,
      11
    ],
    "group": "path_cobble",
    "semantic": "cobble/stone path tile",
    "walkable_default": True,
    "tags": [
      "path",
      "stone",
      "walkable"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "2,11": {
    "id": "ash_a5_r11_c02",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      2,
      11
    ],
    "group": "path_cobble",
    "semantic": "cobble/stone path tile",
    "walkable_default": True,
    "tags": [
      "path",
      "stone",
      "walkable"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "3,11": {
    "id": "ash_a5_r11_c03",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      3,
      11
    ],
    "group": "path_cobble",
    "semantic": "cobble/stone path tile",
    "walkable_default": True,
    "tags": [
      "path",
      "stone",
      "walkable"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "4,11": {
    "id": "ash_a5_r11_c04",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      4,
      11
    ],
    "group": "path_cobble",
    "semantic": "cobble/stone path tile",
    "walkable_default": True,
    "tags": [
      "path",
      "stone",
      "walkable"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "5,11": {
    "id": "ash_a5_r11_c05",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      5,
      11
    ],
    "group": "path_cobble",
    "semantic": "cobble/stone path tile",
    "walkable_default": True,
    "tags": [
      "path",
      "stone",
      "walkable"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "6,11": {
    "id": "ash_a5_r11_c06",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      6,
      11
    ],
    "group": "path_cobble",
    "semantic": "cobble/stone path tile",
    "walkable_default": True,
    "tags": [
      "path",
      "stone",
      "walkable"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "7,11": {
    "id": "ash_a5_r11_c07",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      7,
      11
    ],
    "group": "path_cobble",
    "semantic": "cobble/stone path tile",
    "walkable_default": True,
    "tags": [
      "path",
      "stone",
      "walkable"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "8,11": {
    "id": "ash_a5_r11_c08",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      8,
      11
    ],
    "group": "path_cobble",
    "semantic": "cobble/stone path tile",
    "walkable_default": True,
    "tags": [
      "path",
      "stone",
      "walkable"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "9,11": {
    "id": "ash_a5_r11_c09",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      9,
      11
    ],
    "group": "path_cobble",
    "semantic": "cobble/stone path tile",
    "walkable_default": True,
    "tags": [
      "path",
      "stone",
      "walkable"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "10,11": {
    "id": "ash_a5_r11_c10",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      10,
      11
    ],
    "group": "path_cobble",
    "semantic": "cobble/stone path tile",
    "walkable_default": True,
    "tags": [
      "path",
      "stone",
      "walkable"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "11,11": {
    "id": "ash_a5_r11_c11",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      11,
      11
    ],
    "group": "path_cobble",
    "semantic": "cobble/stone path tile",
    "walkable_default": True,
    "tags": [
      "path",
      "stone",
      "walkable"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "12,11": {
    "id": "ash_a5_r11_c12",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      12,
      11
    ],
    "group": "path_cobble",
    "semantic": "cobble/stone path tile",
    "walkable_default": True,
    "tags": [
      "path",
      "stone",
      "walkable"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "13,11": {
    "id": "ash_a5_r11_c13",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      13,
      11
    ],
    "group": "path_cobble",
    "semantic": "cobble/stone path tile",
    "walkable_default": True,
    "tags": [
      "path",
      "stone",
      "walkable"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "14,11": {
    "id": "ash_a5_r11_c14",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      14,
      11
    ],
    "group": "path_cobble",
    "semantic": "cobble/stone path tile",
    "walkable_default": True,
    "tags": [
      "path",
      "stone",
      "walkable"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "15,11": {
    "id": "ash_a5_r11_c15",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      15,
      11
    ],
    "group": "path_cobble",
    "semantic": "cobble/stone path tile",
    "walkable_default": True,
    "tags": [
      "path",
      "stone",
      "walkable"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "0,12": {
    "id": "ash_a5_r12_c00",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      0,
      12
    ],
    "group": "gravel_patch",
    "semantic": "gravel / rough ash patch tile",
    "walkable_default": True,
    "tags": [
      "gravel",
      "rough",
      "ground"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "1,12": {
    "id": "ash_a5_r12_c01",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      1,
      12
    ],
    "group": "gravel_patch",
    "semantic": "gravel / rough ash patch tile",
    "walkable_default": True,
    "tags": [
      "gravel",
      "rough",
      "ground"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "2,12": {
    "id": "ash_a5_r12_c02",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      2,
      12
    ],
    "group": "gravel_patch",
    "semantic": "gravel / rough ash patch tile",
    "walkable_default": True,
    "tags": [
      "gravel",
      "rough",
      "ground"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "3,12": {
    "id": "ash_a5_r12_c03",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      3,
      12
    ],
    "group": "gravel_patch",
    "semantic": "gravel / rough ash patch tile",
    "walkable_default": True,
    "tags": [
      "gravel",
      "rough",
      "ground"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "4,12": {
    "id": "ash_a5_r12_c04",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      4,
      12
    ],
    "group": "gravel_patch",
    "semantic": "gravel / rough ash patch tile",
    "walkable_default": True,
    "tags": [
      "gravel",
      "rough",
      "ground"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "5,12": {
    "id": "ash_a5_r12_c05",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      5,
      12
    ],
    "group": "gravel_patch",
    "semantic": "gravel / rough ash patch tile",
    "walkable_default": True,
    "tags": [
      "gravel",
      "rough",
      "ground"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "6,12": {
    "id": "ash_a5_r12_c06",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      6,
      12
    ],
    "group": "gravel_patch",
    "semantic": "gravel / rough ash patch tile",
    "walkable_default": True,
    "tags": [
      "gravel",
      "rough",
      "ground"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "7,12": {
    "id": "ash_a5_r12_c07",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      7,
      12
    ],
    "group": "gravel_patch",
    "semantic": "gravel / rough ash patch tile",
    "walkable_default": True,
    "tags": [
      "gravel",
      "rough",
      "ground"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "8,12": {
    "id": "ash_a5_r12_c08",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      8,
      12
    ],
    "group": "gravel_patch",
    "semantic": "gravel / rough ash patch tile",
    "walkable_default": True,
    "tags": [
      "gravel",
      "rough",
      "ground"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "9,12": {
    "id": "ash_a5_r12_c09",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      9,
      12
    ],
    "group": "gravel_patch",
    "semantic": "gravel / rough ash patch tile",
    "walkable_default": True,
    "tags": [
      "gravel",
      "rough",
      "ground"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "10,12": {
    "id": "ash_a5_r12_c10",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      10,
      12
    ],
    "group": "gravel_patch",
    "semantic": "gravel / rough ash patch tile",
    "walkable_default": True,
    "tags": [
      "gravel",
      "rough",
      "ground"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "11,12": {
    "id": "ash_a5_r12_c11",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      11,
      12
    ],
    "group": "gravel_patch",
    "semantic": "gravel / rough ash patch tile",
    "walkable_default": True,
    "tags": [
      "gravel",
      "rough",
      "ground"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "12,12": {
    "id": "ash_a5_r12_c12",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      12,
      12
    ],
    "group": "gravel_patch",
    "semantic": "gravel / rough ash patch tile",
    "walkable_default": True,
    "tags": [
      "gravel",
      "rough",
      "ground"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "13,12": {
    "id": "ash_a5_r12_c13",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      13,
      12
    ],
    "group": "gravel_patch",
    "semantic": "gravel / rough ash patch tile",
    "walkable_default": True,
    "tags": [
      "gravel",
      "rough",
      "ground"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "14,12": {
    "id": "ash_a5_r12_c14",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      14,
      12
    ],
    "group": "gravel_patch",
    "semantic": "gravel / rough ash patch tile",
    "walkable_default": True,
    "tags": [
      "gravel",
      "rough",
      "ground"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "15,12": {
    "id": "ash_a5_r12_c15",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      15,
      12
    ],
    "group": "gravel_patch",
    "semantic": "gravel / rough ash patch tile",
    "walkable_default": True,
    "tags": [
      "gravel",
      "rough",
      "ground"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "0,13": {
    "id": "ash_a5_r13_c00",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      0,
      13
    ],
    "group": "gravel_patch",
    "semantic": "gravel / rough ash patch tile",
    "walkable_default": True,
    "tags": [
      "gravel",
      "rough",
      "ground"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "1,13": {
    "id": "ash_a5_r13_c01",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      1,
      13
    ],
    "group": "gravel_patch",
    "semantic": "gravel / rough ash patch tile",
    "walkable_default": True,
    "tags": [
      "gravel",
      "rough",
      "ground"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "2,13": {
    "id": "ash_a5_r13_c02",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      2,
      13
    ],
    "group": "gravel_patch",
    "semantic": "gravel / rough ash patch tile",
    "walkable_default": True,
    "tags": [
      "gravel",
      "rough",
      "ground"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "3,13": {
    "id": "ash_a5_r13_c03",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      3,
      13
    ],
    "group": "gravel_patch",
    "semantic": "gravel / rough ash patch tile",
    "walkable_default": True,
    "tags": [
      "gravel",
      "rough",
      "ground"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "4,13": {
    "id": "ash_a5_r13_c04",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      4,
      13
    ],
    "group": "gravel_patch",
    "semantic": "gravel / rough ash patch tile",
    "walkable_default": True,
    "tags": [
      "gravel",
      "rough",
      "ground"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "5,13": {
    "id": "ash_a5_r13_c05",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      5,
      13
    ],
    "group": "gravel_patch",
    "semantic": "gravel / rough ash patch tile",
    "walkable_default": True,
    "tags": [
      "gravel",
      "rough",
      "ground"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "6,13": {
    "id": "ash_a5_r13_c06",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      6,
      13
    ],
    "group": "gravel_patch",
    "semantic": "gravel / rough ash patch tile",
    "walkable_default": True,
    "tags": [
      "gravel",
      "rough",
      "ground"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "7,13": {
    "id": "ash_a5_r13_c07",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      7,
      13
    ],
    "group": "gravel_patch",
    "semantic": "gravel / rough ash patch tile",
    "walkable_default": True,
    "tags": [
      "gravel",
      "rough",
      "ground"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "8,13": {
    "id": "ash_a5_r13_c08",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      8,
      13
    ],
    "group": "gravel_patch",
    "semantic": "gravel / rough ash patch tile",
    "walkable_default": True,
    "tags": [
      "gravel",
      "rough",
      "ground"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "9,13": {
    "id": "ash_a5_r13_c09",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      9,
      13
    ],
    "group": "gravel_patch",
    "semantic": "gravel / rough ash patch tile",
    "walkable_default": True,
    "tags": [
      "gravel",
      "rough",
      "ground"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "10,13": {
    "id": "ash_a5_r13_c10",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      10,
      13
    ],
    "group": "gravel_patch",
    "semantic": "gravel / rough ash patch tile",
    "walkable_default": True,
    "tags": [
      "gravel",
      "rough",
      "ground"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "11,13": {
    "id": "ash_a5_r13_c11",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      11,
      13
    ],
    "group": "gravel_patch",
    "semantic": "gravel / rough ash patch tile",
    "walkable_default": True,
    "tags": [
      "gravel",
      "rough",
      "ground"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "12,13": {
    "id": "ash_a5_r13_c12",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      12,
      13
    ],
    "group": "gravel_patch",
    "semantic": "gravel / rough ash patch tile",
    "walkable_default": True,
    "tags": [
      "gravel",
      "rough",
      "ground"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "13,13": {
    "id": "ash_a5_r13_c13",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      13,
      13
    ],
    "group": "gravel_patch",
    "semantic": "gravel / rough ash patch tile",
    "walkable_default": True,
    "tags": [
      "gravel",
      "rough",
      "ground"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "14,13": {
    "id": "ash_a5_r13_c14",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      14,
      13
    ],
    "group": "gravel_patch",
    "semantic": "gravel / rough ash patch tile",
    "walkable_default": True,
    "tags": [
      "gravel",
      "rough",
      "ground"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "15,13": {
    "id": "ash_a5_r13_c15",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      15,
      13
    ],
    "group": "gravel_patch",
    "semantic": "gravel / rough ash patch tile",
    "walkable_default": True,
    "tags": [
      "gravel",
      "rough",
      "ground"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "0,14": {
    "id": "ash_a5_r14_c00",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      0,
      14
    ],
    "group": "transition_edge",
    "semantic": "ground transition / edge tile",
    "walkable_default": True,
    "tags": [
      "transition",
      "edge",
      "ground"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "1,14": {
    "id": "ash_a5_r14_c01",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      1,
      14
    ],
    "group": "transition_edge",
    "semantic": "ground transition / edge tile",
    "walkable_default": True,
    "tags": [
      "transition",
      "edge",
      "ground"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "2,14": {
    "id": "ash_a5_r14_c02",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      2,
      14
    ],
    "group": "transition_edge",
    "semantic": "ground transition / edge tile",
    "walkable_default": True,
    "tags": [
      "transition",
      "edge",
      "ground"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "3,14": {
    "id": "ash_a5_r14_c03",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      3,
      14
    ],
    "group": "transition_edge",
    "semantic": "ground transition / edge tile",
    "walkable_default": True,
    "tags": [
      "transition",
      "edge",
      "ground"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "4,14": {
    "id": "ash_a5_r14_c04",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      4,
      14
    ],
    "group": "transition_edge",
    "semantic": "ground transition / edge tile",
    "walkable_default": True,
    "tags": [
      "transition",
      "edge",
      "ground"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "5,14": {
    "id": "ash_a5_r14_c05",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      5,
      14
    ],
    "group": "transition_edge",
    "semantic": "ground transition / edge tile",
    "walkable_default": True,
    "tags": [
      "transition",
      "edge",
      "ground"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "6,14": {
    "id": "ash_a5_r14_c06",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      6,
      14
    ],
    "group": "transition_edge",
    "semantic": "ground transition / edge tile",
    "walkable_default": True,
    "tags": [
      "transition",
      "edge",
      "ground"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "7,14": {
    "id": "ash_a5_r14_c07",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      7,
      14
    ],
    "group": "transition_edge",
    "semantic": "ground transition / edge tile",
    "walkable_default": True,
    "tags": [
      "transition",
      "edge",
      "ground"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "8,14": {
    "id": "ash_a5_r14_c08",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      8,
      14
    ],
    "group": "transition_edge",
    "semantic": "ground transition / edge tile",
    "walkable_default": True,
    "tags": [
      "transition",
      "edge",
      "ground"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "9,14": {
    "id": "ash_a5_r14_c09",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      9,
      14
    ],
    "group": "transition_edge",
    "semantic": "ground transition / edge tile",
    "walkable_default": True,
    "tags": [
      "transition",
      "edge",
      "ground"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "10,14": {
    "id": "ash_a5_r14_c10",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      10,
      14
    ],
    "group": "transition_edge",
    "semantic": "ground transition / edge tile",
    "walkable_default": True,
    "tags": [
      "transition",
      "edge",
      "ground"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "11,14": {
    "id": "ash_a5_r14_c11",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      11,
      14
    ],
    "group": "transition_edge",
    "semantic": "ground transition / edge tile",
    "walkable_default": True,
    "tags": [
      "transition",
      "edge",
      "ground"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "12,14": {
    "id": "ash_a5_r14_c12",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      12,
      14
    ],
    "group": "transition_edge",
    "semantic": "ground transition / edge tile",
    "walkable_default": True,
    "tags": [
      "transition",
      "edge",
      "ground"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "13,14": {
    "id": "ash_a5_r14_c13",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      13,
      14
    ],
    "group": "transition_edge",
    "semantic": "ground transition / edge tile",
    "walkable_default": True,
    "tags": [
      "transition",
      "edge",
      "ground"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "14,14": {
    "id": "ash_a5_r14_c14",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      14,
      14
    ],
    "group": "transition_edge",
    "semantic": "ground transition / edge tile",
    "walkable_default": True,
    "tags": [
      "transition",
      "edge",
      "ground"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "15,14": {
    "id": "ash_a5_r14_c15",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      15,
      14
    ],
    "group": "transition_edge",
    "semantic": "ground transition / edge tile",
    "walkable_default": True,
    "tags": [
      "transition",
      "edge",
      "ground"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "0,15": {
    "id": "ash_a5_r15_c00",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      0,
      15
    ],
    "group": "plateau_top",
    "semantic": "raised ground / plateau top tile",
    "walkable_default": True,
    "tags": [
      "plateau",
      "top",
      "ground"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "1,15": {
    "id": "ash_a5_r15_c01",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      1,
      15
    ],
    "group": "plateau_top",
    "semantic": "raised ground / plateau top tile",
    "walkable_default": True,
    "tags": [
      "plateau",
      "top",
      "ground"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "2,15": {
    "id": "ash_a5_r15_c02",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      2,
      15
    ],
    "group": "plateau_top",
    "semantic": "raised ground / plateau top tile",
    "walkable_default": True,
    "tags": [
      "plateau",
      "top",
      "ground"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "3,15": {
    "id": "ash_a5_r15_c03",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      3,
      15
    ],
    "group": "plateau_top",
    "semantic": "raised ground / plateau top tile",
    "walkable_default": True,
    "tags": [
      "plateau",
      "top",
      "ground"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "4,15": {
    "id": "ash_a5_r15_c04",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      4,
      15
    ],
    "group": "plateau_top",
    "semantic": "raised ground / plateau top tile",
    "walkable_default": True,
    "tags": [
      "plateau",
      "top",
      "ground"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "5,15": {
    "id": "ash_a5_r15_c05",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      5,
      15
    ],
    "group": "plateau_top",
    "semantic": "raised ground / plateau top tile",
    "walkable_default": True,
    "tags": [
      "plateau",
      "top",
      "ground"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "6,15": {
    "id": "ash_a5_r15_c06",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      6,
      15
    ],
    "group": "plateau_top",
    "semantic": "raised ground / plateau top tile",
    "walkable_default": True,
    "tags": [
      "plateau",
      "top",
      "ground"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "7,15": {
    "id": "ash_a5_r15_c07",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      7,
      15
    ],
    "group": "plateau_top",
    "semantic": "raised ground / plateau top tile",
    "walkable_default": True,
    "tags": [
      "plateau",
      "top",
      "ground"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "8,15": {
    "id": "ash_a5_r15_c08",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      8,
      15
    ],
    "group": "plateau_top",
    "semantic": "raised ground / plateau top tile",
    "walkable_default": True,
    "tags": [
      "plateau",
      "top",
      "ground"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "9,15": {
    "id": "ash_a5_r15_c09",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      9,
      15
    ],
    "group": "plateau_top",
    "semantic": "raised ground / plateau top tile",
    "walkable_default": True,
    "tags": [
      "plateau",
      "top",
      "ground"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "10,15": {
    "id": "ash_a5_r15_c10",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      10,
      15
    ],
    "group": "plateau_top",
    "semantic": "raised ground / plateau top tile",
    "walkable_default": True,
    "tags": [
      "plateau",
      "top",
      "ground"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "11,15": {
    "id": "ash_a5_r15_c11",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      11,
      15
    ],
    "group": "plateau_top",
    "semantic": "raised ground / plateau top tile",
    "walkable_default": True,
    "tags": [
      "plateau",
      "top",
      "ground"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "12,15": {
    "id": "ash_a5_r15_c12",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      12,
      15
    ],
    "group": "plateau_top",
    "semantic": "raised ground / plateau top tile",
    "walkable_default": True,
    "tags": [
      "plateau",
      "top",
      "ground"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "13,15": {
    "id": "ash_a5_r15_c13",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      13,
      15
    ],
    "group": "plateau_top",
    "semantic": "raised ground / plateau top tile",
    "walkable_default": True,
    "tags": [
      "plateau",
      "top",
      "ground"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "14,15": {
    "id": "ash_a5_r15_c14",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      14,
      15
    ],
    "group": "plateau_top",
    "semantic": "raised ground / plateau top tile",
    "walkable_default": True,
    "tags": [
      "plateau",
      "top",
      "ground"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "15,15": {
    "id": "ash_a5_r15_c15",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      15,
      15
    ],
    "group": "plateau_top",
    "semantic": "raised ground / plateau top tile",
    "walkable_default": True,
    "tags": [
      "plateau",
      "top",
      "ground"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "0,16": {
    "id": "ash_a5_r16_c00",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      0,
      16
    ],
    "group": "wall_cap",
    "semantic": "wall cap / raised ledge top tile",
    "walkable_default": False,
    "tags": [
      "wall",
      "ledge",
      "top"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "1,16": {
    "id": "ash_a5_r16_c01",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      1,
      16
    ],
    "group": "wall_cap",
    "semantic": "wall cap / raised ledge top tile",
    "walkable_default": False,
    "tags": [
      "wall",
      "ledge",
      "top"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "2,16": {
    "id": "ash_a5_r16_c02",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      2,
      16
    ],
    "group": "wall_cap",
    "semantic": "wall cap / raised ledge top tile",
    "walkable_default": False,
    "tags": [
      "wall",
      "ledge",
      "top"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "3,16": {
    "id": "ash_a5_r16_c03",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      3,
      16
    ],
    "group": "wall_cap",
    "semantic": "wall cap / raised ledge top tile",
    "walkable_default": False,
    "tags": [
      "wall",
      "ledge",
      "top"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "4,16": {
    "id": "ash_a5_r16_c04",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      4,
      16
    ],
    "group": "wall_cap",
    "semantic": "wall cap / raised ledge top tile",
    "walkable_default": False,
    "tags": [
      "wall",
      "ledge",
      "top"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "5,16": {
    "id": "ash_a5_r16_c05",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      5,
      16
    ],
    "group": "wall_cap",
    "semantic": "wall cap / raised ledge top tile",
    "walkable_default": False,
    "tags": [
      "wall",
      "ledge",
      "top"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "6,16": {
    "id": "ash_a5_r16_c06",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      6,
      16
    ],
    "group": "wall_cap",
    "semantic": "wall cap / raised ledge top tile",
    "walkable_default": False,
    "tags": [
      "wall",
      "ledge",
      "top"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "7,16": {
    "id": "ash_a5_r16_c07",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      7,
      16
    ],
    "group": "wall_cap",
    "semantic": "wall cap / raised ledge top tile",
    "walkable_default": False,
    "tags": [
      "wall",
      "ledge",
      "top"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "8,16": {
    "id": "ash_a5_r16_c08",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      8,
      16
    ],
    "group": "wall_cap",
    "semantic": "wall cap / raised ledge top tile",
    "walkable_default": False,
    "tags": [
      "wall",
      "ledge",
      "top"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "9,16": {
    "id": "ash_a5_r16_c09",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      9,
      16
    ],
    "group": "wall_cap",
    "semantic": "wall cap / raised ledge top tile",
    "walkable_default": False,
    "tags": [
      "wall",
      "ledge",
      "top"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "10,16": {
    "id": "ash_a5_r16_c10",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      10,
      16
    ],
    "group": "wall_cap",
    "semantic": "wall cap / raised ledge top tile",
    "walkable_default": False,
    "tags": [
      "wall",
      "ledge",
      "top"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "11,16": {
    "id": "ash_a5_r16_c11",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      11,
      16
    ],
    "group": "wall_cap",
    "semantic": "wall cap / raised ledge top tile",
    "walkable_default": False,
    "tags": [
      "wall",
      "ledge",
      "top"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "12,16": {
    "id": "ash_a5_r16_c12",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      12,
      16
    ],
    "group": "wall_cap",
    "semantic": "wall cap / raised ledge top tile",
    "walkable_default": False,
    "tags": [
      "wall",
      "ledge",
      "top"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "13,16": {
    "id": "ash_a5_r16_c13",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      13,
      16
    ],
    "group": "wall_cap",
    "semantic": "wall cap / raised ledge top tile",
    "walkable_default": False,
    "tags": [
      "wall",
      "ledge",
      "top"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "14,16": {
    "id": "ash_a5_r16_c14",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      14,
      16
    ],
    "group": "wall_cap",
    "semantic": "wall cap / raised ledge top tile",
    "walkable_default": False,
    "tags": [
      "wall",
      "ledge",
      "top"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "15,16": {
    "id": "ash_a5_r16_c15",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      15,
      16
    ],
    "group": "wall_cap",
    "semantic": "wall cap / raised ledge top tile",
    "walkable_default": False,
    "tags": [
      "wall",
      "ledge",
      "top"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "0,17": {
    "id": "ash_a5_r17_c00",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      0,
      17
    ],
    "group": "wall_cap",
    "semantic": "wall cap / raised ledge top tile",
    "walkable_default": False,
    "tags": [
      "wall",
      "ledge",
      "top"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "1,17": {
    "id": "ash_a5_r17_c01",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      1,
      17
    ],
    "group": "wall_cap",
    "semantic": "wall cap / raised ledge top tile",
    "walkable_default": False,
    "tags": [
      "wall",
      "ledge",
      "top"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "2,17": {
    "id": "ash_a5_r17_c02",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      2,
      17
    ],
    "group": "wall_cap",
    "semantic": "wall cap / raised ledge top tile",
    "walkable_default": False,
    "tags": [
      "wall",
      "ledge",
      "top"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "3,17": {
    "id": "ash_a5_r17_c03",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      3,
      17
    ],
    "group": "wall_cap",
    "semantic": "wall cap / raised ledge top tile",
    "walkable_default": False,
    "tags": [
      "wall",
      "ledge",
      "top"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "4,17": {
    "id": "ash_a5_r17_c04",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      4,
      17
    ],
    "group": "wall_cap",
    "semantic": "wall cap / raised ledge top tile",
    "walkable_default": False,
    "tags": [
      "wall",
      "ledge",
      "top"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "5,17": {
    "id": "ash_a5_r17_c05",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      5,
      17
    ],
    "group": "wall_cap",
    "semantic": "wall cap / raised ledge top tile",
    "walkable_default": False,
    "tags": [
      "wall",
      "ledge",
      "top"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "6,17": {
    "id": "ash_a5_r17_c06",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      6,
      17
    ],
    "group": "wall_cap",
    "semantic": "wall cap / raised ledge top tile",
    "walkable_default": False,
    "tags": [
      "wall",
      "ledge",
      "top"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "7,17": {
    "id": "ash_a5_r17_c07",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      7,
      17
    ],
    "group": "wall_cap",
    "semantic": "wall cap / raised ledge top tile",
    "walkable_default": False,
    "tags": [
      "wall",
      "ledge",
      "top"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "8,17": {
    "id": "ash_a5_r17_c08",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      8,
      17
    ],
    "group": "wall_cap",
    "semantic": "wall cap / raised ledge top tile",
    "walkable_default": False,
    "tags": [
      "wall",
      "ledge",
      "top"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "9,17": {
    "id": "ash_a5_r17_c09",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      9,
      17
    ],
    "group": "wall_cap",
    "semantic": "wall cap / raised ledge top tile",
    "walkable_default": False,
    "tags": [
      "wall",
      "ledge",
      "top"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "10,17": {
    "id": "ash_a5_r17_c10",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      10,
      17
    ],
    "group": "wall_cap",
    "semantic": "wall cap / raised ledge top tile",
    "walkable_default": False,
    "tags": [
      "wall",
      "ledge",
      "top"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "11,17": {
    "id": "ash_a5_r17_c11",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      11,
      17
    ],
    "group": "wall_cap",
    "semantic": "wall cap / raised ledge top tile",
    "walkable_default": False,
    "tags": [
      "wall",
      "ledge",
      "top"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "12,17": {
    "id": "ash_a5_r17_c12",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      12,
      17
    ],
    "group": "wall_cap",
    "semantic": "wall cap / raised ledge top tile",
    "walkable_default": False,
    "tags": [
      "wall",
      "ledge",
      "top"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "13,17": {
    "id": "ash_a5_r17_c13",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      13,
      17
    ],
    "group": "wall_cap",
    "semantic": "wall cap / raised ledge top tile",
    "walkable_default": False,
    "tags": [
      "wall",
      "ledge",
      "top"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "14,17": {
    "id": "ash_a5_r17_c14",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      14,
      17
    ],
    "group": "wall_cap",
    "semantic": "wall cap / raised ledge top tile",
    "walkable_default": False,
    "tags": [
      "wall",
      "ledge",
      "top"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "15,17": {
    "id": "ash_a5_r17_c15",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      15,
      17
    ],
    "group": "wall_cap",
    "semantic": "wall cap / raised ledge top tile",
    "walkable_default": False,
    "tags": [
      "wall",
      "ledge",
      "top"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "0,18": {
    "id": "ash_a5_r18_c00",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      0,
      18
    ],
    "group": "wall_face",
    "semantic": "wall face / cliff face tile",
    "walkable_default": False,
    "tags": [
      "wall",
      "cliff",
      "vertical"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "1,18": {
    "id": "ash_a5_r18_c01",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      1,
      18
    ],
    "group": "wall_face",
    "semantic": "wall face / cliff face tile",
    "walkable_default": False,
    "tags": [
      "wall",
      "cliff",
      "vertical"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "2,18": {
    "id": "ash_a5_r18_c02",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      2,
      18
    ],
    "group": "wall_face",
    "semantic": "wall face / cliff face tile",
    "walkable_default": False,
    "tags": [
      "wall",
      "cliff",
      "vertical"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "3,18": {
    "id": "ash_a5_r18_c03",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      3,
      18
    ],
    "group": "wall_face",
    "semantic": "wall face / cliff face tile",
    "walkable_default": False,
    "tags": [
      "wall",
      "cliff",
      "vertical"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "4,18": {
    "id": "ash_a5_r18_c04",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      4,
      18
    ],
    "group": "wall_face",
    "semantic": "wall face / cliff face tile",
    "walkable_default": False,
    "tags": [
      "wall",
      "cliff",
      "vertical"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "5,18": {
    "id": "ash_a5_r18_c05",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      5,
      18
    ],
    "group": "wall_face",
    "semantic": "wall face / cliff face tile",
    "walkable_default": False,
    "tags": [
      "wall",
      "cliff",
      "vertical"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "6,18": {
    "id": "ash_a5_r18_c06",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      6,
      18
    ],
    "group": "wall_face",
    "semantic": "wall face / cliff face tile",
    "walkable_default": False,
    "tags": [
      "wall",
      "cliff",
      "vertical"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "7,18": {
    "id": "ash_a5_r18_c07",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      7,
      18
    ],
    "group": "wall_face",
    "semantic": "wall face / cliff face tile",
    "walkable_default": False,
    "tags": [
      "wall",
      "cliff",
      "vertical"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "8,18": {
    "id": "ash_a5_r18_c08",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      8,
      18
    ],
    "group": "wall_face",
    "semantic": "wall face / cliff face tile",
    "walkable_default": False,
    "tags": [
      "wall",
      "cliff",
      "vertical"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "9,18": {
    "id": "ash_a5_r18_c09",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      9,
      18
    ],
    "group": "wall_face",
    "semantic": "wall face / cliff face tile",
    "walkable_default": False,
    "tags": [
      "wall",
      "cliff",
      "vertical"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "10,18": {
    "id": "ash_a5_r18_c10",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      10,
      18
    ],
    "group": "wall_face",
    "semantic": "wall face / cliff face tile",
    "walkable_default": False,
    "tags": [
      "wall",
      "cliff",
      "vertical"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "11,18": {
    "id": "ash_a5_r18_c11",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      11,
      18
    ],
    "group": "wall_face",
    "semantic": "wall face / cliff face tile",
    "walkable_default": False,
    "tags": [
      "wall",
      "cliff",
      "vertical"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "12,18": {
    "id": "ash_a5_r18_c12",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      12,
      18
    ],
    "group": "wall_face",
    "semantic": "wall face / cliff face tile",
    "walkable_default": False,
    "tags": [
      "wall",
      "cliff",
      "vertical"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "13,18": {
    "id": "ash_a5_r18_c13",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      13,
      18
    ],
    "group": "wall_face",
    "semantic": "wall face / cliff face tile",
    "walkable_default": False,
    "tags": [
      "wall",
      "cliff",
      "vertical"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "14,18": {
    "id": "ash_a5_r18_c14",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      14,
      18
    ],
    "group": "wall_face",
    "semantic": "wall face / cliff face tile",
    "walkable_default": False,
    "tags": [
      "wall",
      "cliff",
      "vertical"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "15,18": {
    "id": "ash_a5_r18_c15",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      15,
      18
    ],
    "group": "wall_face",
    "semantic": "wall face / cliff face tile",
    "walkable_default": False,
    "tags": [
      "wall",
      "cliff",
      "vertical"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "0,19": {
    "id": "ash_a5_r19_c00",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      0,
      19
    ],
    "group": "wall_face",
    "semantic": "wall face / cliff face tile",
    "walkable_default": False,
    "tags": [
      "wall",
      "cliff",
      "vertical"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "1,19": {
    "id": "ash_a5_r19_c01",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      1,
      19
    ],
    "group": "wall_face",
    "semantic": "wall face / cliff face tile",
    "walkable_default": False,
    "tags": [
      "wall",
      "cliff",
      "vertical"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "2,19": {
    "id": "ash_a5_r19_c02",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      2,
      19
    ],
    "group": "wall_face",
    "semantic": "wall face / cliff face tile",
    "walkable_default": False,
    "tags": [
      "wall",
      "cliff",
      "vertical"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "3,19": {
    "id": "ash_a5_r19_c03",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      3,
      19
    ],
    "group": "wall_face",
    "semantic": "wall face / cliff face tile",
    "walkable_default": False,
    "tags": [
      "wall",
      "cliff",
      "vertical"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "4,19": {
    "id": "ash_a5_r19_c04",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      4,
      19
    ],
    "group": "wall_face",
    "semantic": "wall face / cliff face tile",
    "walkable_default": False,
    "tags": [
      "wall",
      "cliff",
      "vertical"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "5,19": {
    "id": "ash_a5_r19_c05",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      5,
      19
    ],
    "group": "wall_face",
    "semantic": "wall face / cliff face tile",
    "walkable_default": False,
    "tags": [
      "wall",
      "cliff",
      "vertical"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "6,19": {
    "id": "ash_a5_r19_c06",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      6,
      19
    ],
    "group": "wall_face",
    "semantic": "wall face / cliff face tile",
    "walkable_default": False,
    "tags": [
      "wall",
      "cliff",
      "vertical"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "7,19": {
    "id": "ash_a5_r19_c07",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      7,
      19
    ],
    "group": "wall_face",
    "semantic": "wall face / cliff face tile",
    "walkable_default": False,
    "tags": [
      "wall",
      "cliff",
      "vertical"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "8,19": {
    "id": "ash_a5_r19_c08",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      8,
      19
    ],
    "group": "wall_face",
    "semantic": "wall face / cliff face tile",
    "walkable_default": False,
    "tags": [
      "wall",
      "cliff",
      "vertical"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "9,19": {
    "id": "ash_a5_r19_c09",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      9,
      19
    ],
    "group": "wall_face",
    "semantic": "wall face / cliff face tile",
    "walkable_default": False,
    "tags": [
      "wall",
      "cliff",
      "vertical"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "10,19": {
    "id": "ash_a5_r19_c10",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      10,
      19
    ],
    "group": "wall_face",
    "semantic": "wall face / cliff face tile",
    "walkable_default": False,
    "tags": [
      "wall",
      "cliff",
      "vertical"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "11,19": {
    "id": "ash_a5_r19_c11",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      11,
      19
    ],
    "group": "wall_face",
    "semantic": "wall face / cliff face tile",
    "walkable_default": False,
    "tags": [
      "wall",
      "cliff",
      "vertical"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "12,19": {
    "id": "ash_a5_r19_c12",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      12,
      19
    ],
    "group": "wall_face",
    "semantic": "wall face / cliff face tile",
    "walkable_default": False,
    "tags": [
      "wall",
      "cliff",
      "vertical"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "13,19": {
    "id": "ash_a5_r19_c13",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      13,
      19
    ],
    "group": "wall_face",
    "semantic": "wall face / cliff face tile",
    "walkable_default": False,
    "tags": [
      "wall",
      "cliff",
      "vertical"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "14,19": {
    "id": "ash_a5_r19_c14",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      14,
      19
    ],
    "group": "wall_face",
    "semantic": "wall face / cliff face tile",
    "walkable_default": False,
    "tags": [
      "wall",
      "cliff",
      "vertical"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "15,19": {
    "id": "ash_a5_r19_c15",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      15,
      19
    ],
    "group": "wall_face",
    "semantic": "wall face / cliff face tile",
    "walkable_default": False,
    "tags": [
      "wall",
      "cliff",
      "vertical"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "0,20": {
    "id": "ash_a5_r20_c00",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      0,
      20
    ],
    "group": "stairs_upper",
    "semantic": "stairs / step segment upper",
    "walkable_default": True,
    "tags": [
      "stairs",
      "steps",
      "walkable"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "1,20": {
    "id": "ash_a5_r20_c01",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      1,
      20
    ],
    "group": "stairs_upper",
    "semantic": "stairs / step segment upper",
    "walkable_default": True,
    "tags": [
      "stairs",
      "steps",
      "walkable"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "2,20": {
    "id": "ash_a5_r20_c02",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      2,
      20
    ],
    "group": "stairs_upper",
    "semantic": "stairs / step segment upper",
    "walkable_default": True,
    "tags": [
      "stairs",
      "steps",
      "walkable"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "3,20": {
    "id": "ash_a5_r20_c03",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      3,
      20
    ],
    "group": "stairs_upper",
    "semantic": "stairs / step segment upper",
    "walkable_default": True,
    "tags": [
      "stairs",
      "steps",
      "walkable"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "4,20": {
    "id": "ash_a5_r20_c04",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      4,
      20
    ],
    "group": "stairs_upper",
    "semantic": "stairs / step segment upper",
    "walkable_default": True,
    "tags": [
      "stairs",
      "steps",
      "walkable"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "5,20": {
    "id": "ash_a5_r20_c05",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      5,
      20
    ],
    "group": "stairs_upper",
    "semantic": "stairs / step segment upper",
    "walkable_default": True,
    "tags": [
      "stairs",
      "steps",
      "walkable"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "6,20": {
    "id": "ash_a5_r20_c06",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      6,
      20
    ],
    "group": "stairs_upper",
    "semantic": "stairs / step segment upper",
    "walkable_default": True,
    "tags": [
      "stairs",
      "steps",
      "walkable"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "7,20": {
    "id": "ash_a5_r20_c07",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      7,
      20
    ],
    "group": "stairs_upper",
    "semantic": "stairs / step segment upper",
    "walkable_default": True,
    "tags": [
      "stairs",
      "steps",
      "walkable"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "8,20": {
    "id": "ash_a5_r20_c08",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      8,
      20
    ],
    "group": "stairs_upper",
    "semantic": "stairs / step segment upper",
    "walkable_default": True,
    "tags": [
      "stairs",
      "steps",
      "walkable"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "9,20": {
    "id": "ash_a5_r20_c09",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      9,
      20
    ],
    "group": "stairs_upper",
    "semantic": "stairs / step segment upper",
    "walkable_default": True,
    "tags": [
      "stairs",
      "steps",
      "walkable"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "10,20": {
    "id": "ash_a5_r20_c10",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      10,
      20
    ],
    "group": "stairs_upper",
    "semantic": "stairs / step segment upper",
    "walkable_default": True,
    "tags": [
      "stairs",
      "steps",
      "walkable"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "11,20": {
    "id": "ash_a5_r20_c11",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      11,
      20
    ],
    "group": "stairs_upper",
    "semantic": "stairs / step segment upper",
    "walkable_default": True,
    "tags": [
      "stairs",
      "steps",
      "walkable"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "12,20": {
    "id": "ash_a5_r20_c12",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      12,
      20
    ],
    "group": "stairs_upper",
    "semantic": "stairs / step segment upper",
    "walkable_default": True,
    "tags": [
      "stairs",
      "steps",
      "walkable"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "13,20": {
    "id": "ash_a5_r20_c13",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      13,
      20
    ],
    "group": "stairs_upper",
    "semantic": "stairs / step segment upper",
    "walkable_default": True,
    "tags": [
      "stairs",
      "steps",
      "walkable"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "14,20": {
    "id": "ash_a5_r20_c14",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      14,
      20
    ],
    "group": "stairs_upper",
    "semantic": "stairs / step segment upper",
    "walkable_default": True,
    "tags": [
      "stairs",
      "steps",
      "walkable"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "15,20": {
    "id": "ash_a5_r20_c15",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      15,
      20
    ],
    "group": "stairs_upper",
    "semantic": "stairs / step segment upper",
    "walkable_default": True,
    "tags": [
      "stairs",
      "steps",
      "walkable"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "0,21": {
    "id": "ash_a5_r21_c00",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      0,
      21
    ],
    "group": "stairs_lower",
    "semantic": "stairs / step segment lower",
    "walkable_default": True,
    "tags": [
      "stairs",
      "steps",
      "walkable"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "1,21": {
    "id": "ash_a5_r21_c01",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      1,
      21
    ],
    "group": "stairs_lower",
    "semantic": "stairs / step segment lower",
    "walkable_default": True,
    "tags": [
      "stairs",
      "steps",
      "walkable"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "2,21": {
    "id": "ash_a5_r21_c02",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      2,
      21
    ],
    "group": "stairs_lower",
    "semantic": "stairs / step segment lower",
    "walkable_default": True,
    "tags": [
      "stairs",
      "steps",
      "walkable"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "3,21": {
    "id": "ash_a5_r21_c03",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      3,
      21
    ],
    "group": "stairs_lower",
    "semantic": "stairs / step segment lower",
    "walkable_default": True,
    "tags": [
      "stairs",
      "steps",
      "walkable"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "4,21": {
    "id": "ash_a5_r21_c04",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      4,
      21
    ],
    "group": "stairs_lower",
    "semantic": "stairs / step segment lower",
    "walkable_default": True,
    "tags": [
      "stairs",
      "steps",
      "walkable"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "5,21": {
    "id": "ash_a5_r21_c05",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      5,
      21
    ],
    "group": "stairs_lower",
    "semantic": "stairs / step segment lower",
    "walkable_default": True,
    "tags": [
      "stairs",
      "steps",
      "walkable"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "6,21": {
    "id": "ash_a5_r21_c06",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      6,
      21
    ],
    "group": "stairs_lower",
    "semantic": "stairs / step segment lower",
    "walkable_default": True,
    "tags": [
      "stairs",
      "steps",
      "walkable"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "7,21": {
    "id": "ash_a5_r21_c07",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      7,
      21
    ],
    "group": "stairs_lower",
    "semantic": "stairs / step segment lower",
    "walkable_default": True,
    "tags": [
      "stairs",
      "steps",
      "walkable"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "8,21": {
    "id": "ash_a5_r21_c08",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      8,
      21
    ],
    "group": "stairs_lower",
    "semantic": "stairs / step segment lower",
    "walkable_default": True,
    "tags": [
      "stairs",
      "steps",
      "walkable"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "9,21": {
    "id": "ash_a5_r21_c09",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      9,
      21
    ],
    "group": "stairs_lower",
    "semantic": "stairs / step segment lower",
    "walkable_default": True,
    "tags": [
      "stairs",
      "steps",
      "walkable"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "10,21": {
    "id": "ash_a5_r21_c10",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      10,
      21
    ],
    "group": "stairs_lower",
    "semantic": "stairs / step segment lower",
    "walkable_default": True,
    "tags": [
      "stairs",
      "steps",
      "walkable"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "11,21": {
    "id": "ash_a5_r21_c11",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      11,
      21
    ],
    "group": "stairs_lower",
    "semantic": "stairs / step segment lower",
    "walkable_default": True,
    "tags": [
      "stairs",
      "steps",
      "walkable"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "12,21": {
    "id": "ash_a5_r21_c12",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      12,
      21
    ],
    "group": "stairs_lower",
    "semantic": "stairs / step segment lower",
    "walkable_default": True,
    "tags": [
      "stairs",
      "steps",
      "walkable"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "13,21": {
    "id": "ash_a5_r21_c13",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      13,
      21
    ],
    "group": "stairs_lower",
    "semantic": "stairs / step segment lower",
    "walkable_default": True,
    "tags": [
      "stairs",
      "steps",
      "walkable"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "14,21": {
    "id": "ash_a5_r21_c14",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      14,
      21
    ],
    "group": "stairs_lower",
    "semantic": "stairs / step segment lower",
    "walkable_default": True,
    "tags": [
      "stairs",
      "steps",
      "walkable"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "15,21": {
    "id": "ash_a5_r21_c15",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      15,
      21
    ],
    "group": "stairs_lower",
    "semantic": "stairs / step segment lower",
    "walkable_default": True,
    "tags": [
      "stairs",
      "steps",
      "walkable"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "0,22": {
    "id": "ash_a5_r22_c00",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      0,
      22
    ],
    "group": "ruin_floor",
    "semantic": "ruin / brick floor tile",
    "walkable_default": True,
    "tags": [
      "ruin",
      "brick",
      "floor"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "1,22": {
    "id": "ash_a5_r22_c01",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      1,
      22
    ],
    "group": "ruin_floor",
    "semantic": "ruin / brick floor tile",
    "walkable_default": True,
    "tags": [
      "ruin",
      "brick",
      "floor"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "2,22": {
    "id": "ash_a5_r22_c02",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      2,
      22
    ],
    "group": "ruin_floor",
    "semantic": "ruin / brick floor tile",
    "walkable_default": True,
    "tags": [
      "ruin",
      "brick",
      "floor"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "3,22": {
    "id": "ash_a5_r22_c03",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      3,
      22
    ],
    "group": "ruin_floor",
    "semantic": "ruin / brick floor tile",
    "walkable_default": True,
    "tags": [
      "ruin",
      "brick",
      "floor"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "4,22": {
    "id": "ash_a5_r22_c04",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      4,
      22
    ],
    "group": "ruin_floor",
    "semantic": "ruin / brick floor tile",
    "walkable_default": True,
    "tags": [
      "ruin",
      "brick",
      "floor"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "5,22": {
    "id": "ash_a5_r22_c05",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      5,
      22
    ],
    "group": "ruin_floor",
    "semantic": "ruin / brick floor tile",
    "walkable_default": True,
    "tags": [
      "ruin",
      "brick",
      "floor"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "6,22": {
    "id": "ash_a5_r22_c06",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      6,
      22
    ],
    "group": "ruin_floor",
    "semantic": "ruin / brick floor tile",
    "walkable_default": True,
    "tags": [
      "ruin",
      "brick",
      "floor"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "7,22": {
    "id": "ash_a5_r22_c07",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      7,
      22
    ],
    "group": "ruin_floor",
    "semantic": "ruin / brick floor tile",
    "walkable_default": True,
    "tags": [
      "ruin",
      "brick",
      "floor"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "8,22": {
    "id": "ash_a5_r22_c08",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      8,
      22
    ],
    "group": "ruin_floor",
    "semantic": "ruin / brick floor tile",
    "walkable_default": True,
    "tags": [
      "ruin",
      "brick",
      "floor"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "9,22": {
    "id": "ash_a5_r22_c09",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      9,
      22
    ],
    "group": "ruin_floor",
    "semantic": "ruin / brick floor tile",
    "walkable_default": True,
    "tags": [
      "ruin",
      "brick",
      "floor"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "10,22": {
    "id": "ash_a5_r22_c10",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      10,
      22
    ],
    "group": "ruin_floor",
    "semantic": "ruin / brick floor tile",
    "walkable_default": True,
    "tags": [
      "ruin",
      "brick",
      "floor"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "11,22": {
    "id": "ash_a5_r22_c11",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      11,
      22
    ],
    "group": "ruin_floor",
    "semantic": "ruin / brick floor tile",
    "walkable_default": True,
    "tags": [
      "ruin",
      "brick",
      "floor"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "12,22": {
    "id": "ash_a5_r22_c12",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      12,
      22
    ],
    "group": "ruin_floor",
    "semantic": "ruin / brick floor tile",
    "walkable_default": True,
    "tags": [
      "ruin",
      "brick",
      "floor"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "13,22": {
    "id": "ash_a5_r22_c13",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      13,
      22
    ],
    "group": "ruin_floor",
    "semantic": "ruin / brick floor tile",
    "walkable_default": True,
    "tags": [
      "ruin",
      "brick",
      "floor"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "14,22": {
    "id": "ash_a5_r22_c14",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      14,
      22
    ],
    "group": "ruin_floor",
    "semantic": "ruin / brick floor tile",
    "walkable_default": True,
    "tags": [
      "ruin",
      "brick",
      "floor"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "15,22": {
    "id": "ash_a5_r22_c15",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      15,
      22
    ],
    "group": "ruin_floor",
    "semantic": "ruin / brick floor tile",
    "walkable_default": True,
    "tags": [
      "ruin",
      "brick",
      "floor"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "0,23": {
    "id": "ash_a5_r23_c00",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      0,
      23
    ],
    "group": "ruin_wall",
    "semantic": "ruin / brick wall tile",
    "walkable_default": False,
    "tags": [
      "ruin",
      "brick",
      "wall"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "1,23": {
    "id": "ash_a5_r23_c01",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      1,
      23
    ],
    "group": "ruin_wall",
    "semantic": "ruin / brick wall tile",
    "walkable_default": False,
    "tags": [
      "ruin",
      "brick",
      "wall"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "2,23": {
    "id": "ash_a5_r23_c02",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      2,
      23
    ],
    "group": "ruin_wall",
    "semantic": "ruin / brick wall tile",
    "walkable_default": False,
    "tags": [
      "ruin",
      "brick",
      "wall"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "3,23": {
    "id": "ash_a5_r23_c03",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      3,
      23
    ],
    "group": "ruin_wall",
    "semantic": "ruin / brick wall tile",
    "walkable_default": False,
    "tags": [
      "ruin",
      "brick",
      "wall"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "4,23": {
    "id": "ash_a5_r23_c04",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      4,
      23
    ],
    "group": "ruin_wall",
    "semantic": "ruin / brick wall tile",
    "walkable_default": False,
    "tags": [
      "ruin",
      "brick",
      "wall"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "5,23": {
    "id": "ash_a5_r23_c05",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      5,
      23
    ],
    "group": "ruin_wall",
    "semantic": "ruin / brick wall tile",
    "walkable_default": False,
    "tags": [
      "ruin",
      "brick",
      "wall"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "6,23": {
    "id": "ash_a5_r23_c06",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      6,
      23
    ],
    "group": "ruin_wall",
    "semantic": "ruin / brick wall tile",
    "walkable_default": False,
    "tags": [
      "ruin",
      "brick",
      "wall"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "7,23": {
    "id": "ash_a5_r23_c07",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      7,
      23
    ],
    "group": "ruin_wall",
    "semantic": "ruin / brick wall tile",
    "walkable_default": False,
    "tags": [
      "ruin",
      "brick",
      "wall"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "8,23": {
    "id": "ash_a5_r23_c08",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      8,
      23
    ],
    "group": "ruin_wall",
    "semantic": "ruin / brick wall tile",
    "walkable_default": False,
    "tags": [
      "ruin",
      "brick",
      "wall"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "9,23": {
    "id": "ash_a5_r23_c09",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      9,
      23
    ],
    "group": "ruin_wall",
    "semantic": "ruin / brick wall tile",
    "walkable_default": False,
    "tags": [
      "ruin",
      "brick",
      "wall"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "10,23": {
    "id": "ash_a5_r23_c10",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      10,
      23
    ],
    "group": "ruin_wall",
    "semantic": "ruin / brick wall tile",
    "walkable_default": False,
    "tags": [
      "ruin",
      "brick",
      "wall"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "11,23": {
    "id": "ash_a5_r23_c11",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      11,
      23
    ],
    "group": "ruin_wall",
    "semantic": "ruin / brick wall tile",
    "walkable_default": False,
    "tags": [
      "ruin",
      "brick",
      "wall"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "12,23": {
    "id": "ash_a5_r23_c12",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      12,
      23
    ],
    "group": "ruin_wall",
    "semantic": "ruin / brick wall tile",
    "walkable_default": False,
    "tags": [
      "ruin",
      "brick",
      "wall"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "13,23": {
    "id": "ash_a5_r23_c13",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      13,
      23
    ],
    "group": "ruin_wall",
    "semantic": "ruin / brick wall tile",
    "walkable_default": False,
    "tags": [
      "ruin",
      "brick",
      "wall"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "14,23": {
    "id": "ash_a5_r23_c14",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      14,
      23
    ],
    "group": "ruin_wall",
    "semantic": "ruin / brick wall tile",
    "walkable_default": False,
    "tags": [
      "ruin",
      "brick",
      "wall"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "15,23": {
    "id": "ash_a5_r23_c15",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      15,
      23
    ],
    "group": "ruin_wall",
    "semantic": "ruin / brick wall tile",
    "walkable_default": False,
    "tags": [
      "ruin",
      "brick",
      "wall"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "0,24": {
    "id": "ash_a5_r24_c00",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      0,
      24
    ],
    "group": "cave_mouth",
    "semantic": "cave opening / dark entrance tile",
    "walkable_default": False,
    "tags": [
      "cave",
      "opening",
      "dark"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "1,24": {
    "id": "ash_a5_r24_c01",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      1,
      24
    ],
    "group": "cave_mouth",
    "semantic": "cave opening / dark entrance tile",
    "walkable_default": False,
    "tags": [
      "cave",
      "opening",
      "dark"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "2,24": {
    "id": "ash_a5_r24_c02",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      2,
      24
    ],
    "group": "cave_mouth",
    "semantic": "cave opening / dark entrance tile",
    "walkable_default": False,
    "tags": [
      "cave",
      "opening",
      "dark"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "3,24": {
    "id": "ash_a5_r24_c03",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      3,
      24
    ],
    "group": "cave_mouth",
    "semantic": "cave opening / dark entrance tile",
    "walkable_default": False,
    "tags": [
      "cave",
      "opening",
      "dark"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "4,24": {
    "id": "ash_a5_r24_c04",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      4,
      24
    ],
    "group": "cave_mouth",
    "semantic": "cave opening / dark entrance tile",
    "walkable_default": False,
    "tags": [
      "cave",
      "opening",
      "dark"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "5,24": {
    "id": "ash_a5_r24_c05",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      5,
      24
    ],
    "group": "cave_mouth",
    "semantic": "cave opening / dark entrance tile",
    "walkable_default": False,
    "tags": [
      "cave",
      "opening",
      "dark"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "6,24": {
    "id": "ash_a5_r24_c06",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      6,
      24
    ],
    "group": "cave_mouth",
    "semantic": "cave opening / dark entrance tile",
    "walkable_default": False,
    "tags": [
      "cave",
      "opening",
      "dark"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "7,24": {
    "id": "ash_a5_r24_c07",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      7,
      24
    ],
    "group": "cave_mouth",
    "semantic": "cave opening / dark entrance tile",
    "walkable_default": False,
    "tags": [
      "cave",
      "opening",
      "dark"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "8,24": {
    "id": "ash_a5_r24_c08",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      8,
      24
    ],
    "group": "cave_mouth",
    "semantic": "cave opening / dark entrance tile",
    "walkable_default": False,
    "tags": [
      "cave",
      "opening",
      "dark"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "9,24": {
    "id": "ash_a5_r24_c09",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      9,
      24
    ],
    "group": "cave_mouth",
    "semantic": "cave opening / dark entrance tile",
    "walkable_default": False,
    "tags": [
      "cave",
      "opening",
      "dark"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "10,24": {
    "id": "ash_a5_r24_c10",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      10,
      24
    ],
    "group": "cave_mouth",
    "semantic": "cave opening / dark entrance tile",
    "walkable_default": False,
    "tags": [
      "cave",
      "opening",
      "dark"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "11,24": {
    "id": "ash_a5_r24_c11",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      11,
      24
    ],
    "group": "cave_mouth",
    "semantic": "cave opening / dark entrance tile",
    "walkable_default": False,
    "tags": [
      "cave",
      "opening",
      "dark"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "12,24": {
    "id": "ash_a5_r24_c12",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      12,
      24
    ],
    "group": "cave_mouth",
    "semantic": "cave opening / dark entrance tile",
    "walkable_default": False,
    "tags": [
      "cave",
      "opening",
      "dark"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "13,24": {
    "id": "ash_a5_r24_c13",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      13,
      24
    ],
    "group": "cave_mouth",
    "semantic": "cave opening / dark entrance tile",
    "walkable_default": False,
    "tags": [
      "cave",
      "opening",
      "dark"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "14,24": {
    "id": "ash_a5_r24_c14",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      14,
      24
    ],
    "group": "cave_mouth",
    "semantic": "cave opening / dark entrance tile",
    "walkable_default": False,
    "tags": [
      "cave",
      "opening",
      "dark"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "15,24": {
    "id": "ash_a5_r24_c15",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      15,
      24
    ],
    "group": "cave_mouth",
    "semantic": "cave opening / dark entrance tile",
    "walkable_default": False,
    "tags": [
      "cave",
      "opening",
      "dark"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "0,25": {
    "id": "ash_a5_r25_c00",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      0,
      25
    ],
    "group": "cave_mouth",
    "semantic": "cave opening / dark entrance tile",
    "walkable_default": False,
    "tags": [
      "cave",
      "opening",
      "dark"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "1,25": {
    "id": "ash_a5_r25_c01",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      1,
      25
    ],
    "group": "cave_mouth",
    "semantic": "cave opening / dark entrance tile",
    "walkable_default": False,
    "tags": [
      "cave",
      "opening",
      "dark"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "2,25": {
    "id": "ash_a5_r25_c02",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      2,
      25
    ],
    "group": "cave_mouth",
    "semantic": "cave opening / dark entrance tile",
    "walkable_default": False,
    "tags": [
      "cave",
      "opening",
      "dark"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "3,25": {
    "id": "ash_a5_r25_c03",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      3,
      25
    ],
    "group": "cave_mouth",
    "semantic": "cave opening / dark entrance tile",
    "walkable_default": False,
    "tags": [
      "cave",
      "opening",
      "dark"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "4,25": {
    "id": "ash_a5_r25_c04",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      4,
      25
    ],
    "group": "cave_mouth",
    "semantic": "cave opening / dark entrance tile",
    "walkable_default": False,
    "tags": [
      "cave",
      "opening",
      "dark"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "5,25": {
    "id": "ash_a5_r25_c05",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      5,
      25
    ],
    "group": "cave_mouth",
    "semantic": "cave opening / dark entrance tile",
    "walkable_default": False,
    "tags": [
      "cave",
      "opening",
      "dark"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "6,25": {
    "id": "ash_a5_r25_c06",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      6,
      25
    ],
    "group": "cave_mouth",
    "semantic": "cave opening / dark entrance tile",
    "walkable_default": False,
    "tags": [
      "cave",
      "opening",
      "dark"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "7,25": {
    "id": "ash_a5_r25_c07",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      7,
      25
    ],
    "group": "cave_mouth",
    "semantic": "cave opening / dark entrance tile",
    "walkable_default": False,
    "tags": [
      "cave",
      "opening",
      "dark"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "8,25": {
    "id": "ash_a5_r25_c08",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      8,
      25
    ],
    "group": "cave_mouth",
    "semantic": "cave opening / dark entrance tile",
    "walkable_default": False,
    "tags": [
      "cave",
      "opening",
      "dark"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "9,25": {
    "id": "ash_a5_r25_c09",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      9,
      25
    ],
    "group": "cave_mouth",
    "semantic": "cave opening / dark entrance tile",
    "walkable_default": False,
    "tags": [
      "cave",
      "opening",
      "dark"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "10,25": {
    "id": "ash_a5_r25_c10",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      10,
      25
    ],
    "group": "cave_mouth",
    "semantic": "cave opening / dark entrance tile",
    "walkable_default": False,
    "tags": [
      "cave",
      "opening",
      "dark"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "11,25": {
    "id": "ash_a5_r25_c11",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      11,
      25
    ],
    "group": "cave_mouth",
    "semantic": "cave opening / dark entrance tile",
    "walkable_default": False,
    "tags": [
      "cave",
      "opening",
      "dark"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "12,25": {
    "id": "ash_a5_r25_c12",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      12,
      25
    ],
    "group": "cave_mouth",
    "semantic": "cave opening / dark entrance tile",
    "walkable_default": False,
    "tags": [
      "cave",
      "opening",
      "dark"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "13,25": {
    "id": "ash_a5_r25_c13",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      13,
      25
    ],
    "group": "cave_mouth",
    "semantic": "cave opening / dark entrance tile",
    "walkable_default": False,
    "tags": [
      "cave",
      "opening",
      "dark"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "14,25": {
    "id": "ash_a5_r25_c14",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      14,
      25
    ],
    "group": "cave_mouth",
    "semantic": "cave opening / dark entrance tile",
    "walkable_default": False,
    "tags": [
      "cave",
      "opening",
      "dark"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "15,25": {
    "id": "ash_a5_r25_c15",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      15,
      25
    ],
    "group": "cave_mouth",
    "semantic": "cave opening / dark entrance tile",
    "walkable_default": False,
    "tags": [
      "cave",
      "opening",
      "dark"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "0,26": {
    "id": "ash_a5_r26_c00",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      0,
      26
    ],
    "group": "cave_wall",
    "semantic": "cave wall / deep shadow tile",
    "walkable_default": False,
    "tags": [
      "cave",
      "wall",
      "dark"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "1,26": {
    "id": "ash_a5_r26_c01",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      1,
      26
    ],
    "group": "cave_wall",
    "semantic": "cave wall / deep shadow tile",
    "walkable_default": False,
    "tags": [
      "cave",
      "wall",
      "dark"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "2,26": {
    "id": "ash_a5_r26_c02",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      2,
      26
    ],
    "group": "cave_wall",
    "semantic": "cave wall / deep shadow tile",
    "walkable_default": False,
    "tags": [
      "cave",
      "wall",
      "dark"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "3,26": {
    "id": "ash_a5_r26_c03",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      3,
      26
    ],
    "group": "cave_wall",
    "semantic": "cave wall / deep shadow tile",
    "walkable_default": False,
    "tags": [
      "cave",
      "wall",
      "dark"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "4,26": {
    "id": "ash_a5_r26_c04",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      4,
      26
    ],
    "group": "cave_wall",
    "semantic": "cave wall / deep shadow tile",
    "walkable_default": False,
    "tags": [
      "cave",
      "wall",
      "dark"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "5,26": {
    "id": "ash_a5_r26_c05",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      5,
      26
    ],
    "group": "cave_wall",
    "semantic": "cave wall / deep shadow tile",
    "walkable_default": False,
    "tags": [
      "cave",
      "wall",
      "dark"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "6,26": {
    "id": "ash_a5_r26_c06",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      6,
      26
    ],
    "group": "cave_wall",
    "semantic": "cave wall / deep shadow tile",
    "walkable_default": False,
    "tags": [
      "cave",
      "wall",
      "dark"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "7,26": {
    "id": "ash_a5_r26_c07",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      7,
      26
    ],
    "group": "cave_wall",
    "semantic": "cave wall / deep shadow tile",
    "walkable_default": False,
    "tags": [
      "cave",
      "wall",
      "dark"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "8,26": {
    "id": "ash_a5_r26_c08",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      8,
      26
    ],
    "group": "cave_wall",
    "semantic": "cave wall / deep shadow tile",
    "walkable_default": False,
    "tags": [
      "cave",
      "wall",
      "dark"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "9,26": {
    "id": "ash_a5_r26_c09",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      9,
      26
    ],
    "group": "cave_wall",
    "semantic": "cave wall / deep shadow tile",
    "walkable_default": False,
    "tags": [
      "cave",
      "wall",
      "dark"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "10,26": {
    "id": "ash_a5_r26_c10",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      10,
      26
    ],
    "group": "cave_wall",
    "semantic": "cave wall / deep shadow tile",
    "walkable_default": False,
    "tags": [
      "cave",
      "wall",
      "dark"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "11,26": {
    "id": "ash_a5_r26_c11",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      11,
      26
    ],
    "group": "cave_wall",
    "semantic": "cave wall / deep shadow tile",
    "walkable_default": False,
    "tags": [
      "cave",
      "wall",
      "dark"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "12,26": {
    "id": "ash_a5_r26_c12",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      12,
      26
    ],
    "group": "cave_wall",
    "semantic": "cave wall / deep shadow tile",
    "walkable_default": False,
    "tags": [
      "cave",
      "wall",
      "dark"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "13,26": {
    "id": "ash_a5_r26_c13",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      13,
      26
    ],
    "group": "cave_wall",
    "semantic": "cave wall / deep shadow tile",
    "walkable_default": False,
    "tags": [
      "cave",
      "wall",
      "dark"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "14,26": {
    "id": "ash_a5_r26_c14",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      14,
      26
    ],
    "group": "cave_wall",
    "semantic": "cave wall / deep shadow tile",
    "walkable_default": False,
    "tags": [
      "cave",
      "wall",
      "dark"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "15,26": {
    "id": "ash_a5_r26_c15",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      15,
      26
    ],
    "group": "cave_wall",
    "semantic": "cave wall / deep shadow tile",
    "walkable_default": False,
    "tags": [
      "cave",
      "wall",
      "dark"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "0,27": {
    "id": "ash_a5_r27_c00",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      0,
      27
    ],
    "group": "cave_wall",
    "semantic": "cave wall / deep shadow tile",
    "walkable_default": False,
    "tags": [
      "cave",
      "wall",
      "dark"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "1,27": {
    "id": "ash_a5_r27_c01",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      1,
      27
    ],
    "group": "cave_wall",
    "semantic": "cave wall / deep shadow tile",
    "walkable_default": False,
    "tags": [
      "cave",
      "wall",
      "dark"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "2,27": {
    "id": "ash_a5_r27_c02",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      2,
      27
    ],
    "group": "cave_wall",
    "semantic": "cave wall / deep shadow tile",
    "walkable_default": False,
    "tags": [
      "cave",
      "wall",
      "dark"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "3,27": {
    "id": "ash_a5_r27_c03",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      3,
      27
    ],
    "group": "cave_wall",
    "semantic": "cave wall / deep shadow tile",
    "walkable_default": False,
    "tags": [
      "cave",
      "wall",
      "dark"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "4,27": {
    "id": "ash_a5_r27_c04",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      4,
      27
    ],
    "group": "cave_wall",
    "semantic": "cave wall / deep shadow tile",
    "walkable_default": False,
    "tags": [
      "cave",
      "wall",
      "dark"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "5,27": {
    "id": "ash_a5_r27_c05",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      5,
      27
    ],
    "group": "cave_wall",
    "semantic": "cave wall / deep shadow tile",
    "walkable_default": False,
    "tags": [
      "cave",
      "wall",
      "dark"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "6,27": {
    "id": "ash_a5_r27_c06",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      6,
      27
    ],
    "group": "cave_wall",
    "semantic": "cave wall / deep shadow tile",
    "walkable_default": False,
    "tags": [
      "cave",
      "wall",
      "dark"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "7,27": {
    "id": "ash_a5_r27_c07",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      7,
      27
    ],
    "group": "cave_wall",
    "semantic": "cave wall / deep shadow tile",
    "walkable_default": False,
    "tags": [
      "cave",
      "wall",
      "dark"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "8,27": {
    "id": "ash_a5_r27_c08",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      8,
      27
    ],
    "group": "cave_wall",
    "semantic": "cave wall / deep shadow tile",
    "walkable_default": False,
    "tags": [
      "cave",
      "wall",
      "dark"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "9,27": {
    "id": "ash_a5_r27_c09",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      9,
      27
    ],
    "group": "cave_wall",
    "semantic": "cave wall / deep shadow tile",
    "walkable_default": False,
    "tags": [
      "cave",
      "wall",
      "dark"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "10,27": {
    "id": "ash_a5_r27_c10",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      10,
      27
    ],
    "group": "cave_wall",
    "semantic": "cave wall / deep shadow tile",
    "walkable_default": False,
    "tags": [
      "cave",
      "wall",
      "dark"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "11,27": {
    "id": "ash_a5_r27_c11",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      11,
      27
    ],
    "group": "cave_wall",
    "semantic": "cave wall / deep shadow tile",
    "walkable_default": False,
    "tags": [
      "cave",
      "wall",
      "dark"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "12,27": {
    "id": "ash_a5_r27_c12",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      12,
      27
    ],
    "group": "cave_wall",
    "semantic": "cave wall / deep shadow tile",
    "walkable_default": False,
    "tags": [
      "cave",
      "wall",
      "dark"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "13,27": {
    "id": "ash_a5_r27_c13",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      13,
      27
    ],
    "group": "cave_wall",
    "semantic": "cave wall / deep shadow tile",
    "walkable_default": False,
    "tags": [
      "cave",
      "wall",
      "dark"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "14,27": {
    "id": "ash_a5_r27_c14",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      14,
      27
    ],
    "group": "cave_wall",
    "semantic": "cave wall / deep shadow tile",
    "walkable_default": False,
    "tags": [
      "cave",
      "wall",
      "dark"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "15,27": {
    "id": "ash_a5_r27_c15",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      15,
      27
    ],
    "group": "cave_wall",
    "semantic": "cave wall / deep shadow tile",
    "walkable_default": False,
    "tags": [
      "cave",
      "wall",
      "dark"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "0,28": {
    "id": "ash_a5_r28_c00",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      0,
      28
    ],
    "group": "debris",
    "semantic": "bones / debris / rubble accent tile",
    "walkable_default": True,
    "tags": [
      "debris",
      "accent",
      "scatter"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "1,28": {
    "id": "ash_a5_r28_c01",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      1,
      28
    ],
    "group": "debris",
    "semantic": "bones / debris / rubble accent tile",
    "walkable_default": True,
    "tags": [
      "debris",
      "accent",
      "scatter"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "2,28": {
    "id": "ash_a5_r28_c02",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      2,
      28
    ],
    "group": "debris",
    "semantic": "bones / debris / rubble accent tile",
    "walkable_default": True,
    "tags": [
      "debris",
      "accent",
      "scatter"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "3,28": {
    "id": "ash_a5_r28_c03",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      3,
      28
    ],
    "group": "debris",
    "semantic": "bones / debris / rubble accent tile",
    "walkable_default": True,
    "tags": [
      "debris",
      "accent",
      "scatter"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "4,28": {
    "id": "ash_a5_r28_c04",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      4,
      28
    ],
    "group": "debris",
    "semantic": "bones / debris / rubble accent tile",
    "walkable_default": True,
    "tags": [
      "debris",
      "accent",
      "scatter"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "5,28": {
    "id": "ash_a5_r28_c05",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      5,
      28
    ],
    "group": "debris",
    "semantic": "bones / debris / rubble accent tile",
    "walkable_default": True,
    "tags": [
      "debris",
      "accent",
      "scatter"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "6,28": {
    "id": "ash_a5_r28_c06",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      6,
      28
    ],
    "group": "debris",
    "semantic": "bones / debris / rubble accent tile",
    "walkable_default": True,
    "tags": [
      "debris",
      "accent",
      "scatter"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "7,28": {
    "id": "ash_a5_r28_c07",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      7,
      28
    ],
    "group": "debris",
    "semantic": "bones / debris / rubble accent tile",
    "walkable_default": True,
    "tags": [
      "debris",
      "accent",
      "scatter"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "8,28": {
    "id": "ash_a5_r28_c08",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      8,
      28
    ],
    "group": "debris",
    "semantic": "bones / debris / rubble accent tile",
    "walkable_default": True,
    "tags": [
      "debris",
      "accent",
      "scatter"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "9,28": {
    "id": "ash_a5_r28_c09",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      9,
      28
    ],
    "group": "debris",
    "semantic": "bones / debris / rubble accent tile",
    "walkable_default": True,
    "tags": [
      "debris",
      "accent",
      "scatter"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "10,28": {
    "id": "ash_a5_r28_c10",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      10,
      28
    ],
    "group": "debris",
    "semantic": "bones / debris / rubble accent tile",
    "walkable_default": True,
    "tags": [
      "debris",
      "accent",
      "scatter"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "11,28": {
    "id": "ash_a5_r28_c11",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      11,
      28
    ],
    "group": "debris",
    "semantic": "bones / debris / rubble accent tile",
    "walkable_default": True,
    "tags": [
      "debris",
      "accent",
      "scatter"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "12,28": {
    "id": "ash_a5_r28_c12",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      12,
      28
    ],
    "group": "debris",
    "semantic": "bones / debris / rubble accent tile",
    "walkable_default": True,
    "tags": [
      "debris",
      "accent",
      "scatter"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "13,28": {
    "id": "ash_a5_r28_c13",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      13,
      28
    ],
    "group": "debris",
    "semantic": "bones / debris / rubble accent tile",
    "walkable_default": True,
    "tags": [
      "debris",
      "accent",
      "scatter"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "14,28": {
    "id": "ash_a5_r28_c14",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      14,
      28
    ],
    "group": "debris",
    "semantic": "bones / debris / rubble accent tile",
    "walkable_default": True,
    "tags": [
      "debris",
      "accent",
      "scatter"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "15,28": {
    "id": "ash_a5_r28_c15",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      15,
      28
    ],
    "group": "debris",
    "semantic": "bones / debris / rubble accent tile",
    "walkable_default": True,
    "tags": [
      "debris",
      "accent",
      "scatter"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "0,29": {
    "id": "ash_a5_r29_c00",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      0,
      29
    ],
    "group": "marker",
    "semantic": "grave / marker / prop-support tile",
    "walkable_default": False,
    "tags": [
      "prop",
      "marker",
      "support"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "1,29": {
    "id": "ash_a5_r29_c01",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      1,
      29
    ],
    "group": "marker",
    "semantic": "grave / marker / prop-support tile",
    "walkable_default": False,
    "tags": [
      "prop",
      "marker",
      "support"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "2,29": {
    "id": "ash_a5_r29_c02",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      2,
      29
    ],
    "group": "marker",
    "semantic": "grave / marker / prop-support tile",
    "walkable_default": False,
    "tags": [
      "prop",
      "marker",
      "support"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "3,29": {
    "id": "ash_a5_r29_c03",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      3,
      29
    ],
    "group": "marker",
    "semantic": "grave / marker / prop-support tile",
    "walkable_default": False,
    "tags": [
      "prop",
      "marker",
      "support"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "4,29": {
    "id": "ash_a5_r29_c04",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      4,
      29
    ],
    "group": "marker",
    "semantic": "grave / marker / prop-support tile",
    "walkable_default": False,
    "tags": [
      "prop",
      "marker",
      "support"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "5,29": {
    "id": "ash_a5_r29_c05",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      5,
      29
    ],
    "group": "marker",
    "semantic": "grave / marker / prop-support tile",
    "walkable_default": False,
    "tags": [
      "prop",
      "marker",
      "support"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "6,29": {
    "id": "ash_a5_r29_c06",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      6,
      29
    ],
    "group": "marker",
    "semantic": "grave / marker / prop-support tile",
    "walkable_default": False,
    "tags": [
      "prop",
      "marker",
      "support"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "7,29": {
    "id": "ash_a5_r29_c07",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      7,
      29
    ],
    "group": "marker",
    "semantic": "grave / marker / prop-support tile",
    "walkable_default": False,
    "tags": [
      "prop",
      "marker",
      "support"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "8,29": {
    "id": "ash_a5_r29_c08",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      8,
      29
    ],
    "group": "marker",
    "semantic": "grave / marker / prop-support tile",
    "walkable_default": False,
    "tags": [
      "prop",
      "marker",
      "support"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "9,29": {
    "id": "ash_a5_r29_c09",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      9,
      29
    ],
    "group": "marker",
    "semantic": "grave / marker / prop-support tile",
    "walkable_default": False,
    "tags": [
      "prop",
      "marker",
      "support"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "10,29": {
    "id": "ash_a5_r29_c10",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      10,
      29
    ],
    "group": "marker",
    "semantic": "grave / marker / prop-support tile",
    "walkable_default": False,
    "tags": [
      "prop",
      "marker",
      "support"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "11,29": {
    "id": "ash_a5_r29_c11",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      11,
      29
    ],
    "group": "marker",
    "semantic": "grave / marker / prop-support tile",
    "walkable_default": False,
    "tags": [
      "prop",
      "marker",
      "support"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "12,29": {
    "id": "ash_a5_r29_c12",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      12,
      29
    ],
    "group": "marker",
    "semantic": "grave / marker / prop-support tile",
    "walkable_default": False,
    "tags": [
      "prop",
      "marker",
      "support"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "13,29": {
    "id": "ash_a5_r29_c13",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      13,
      29
    ],
    "group": "marker",
    "semantic": "grave / marker / prop-support tile",
    "walkable_default": False,
    "tags": [
      "prop",
      "marker",
      "support"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "14,29": {
    "id": "ash_a5_r29_c14",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      14,
      29
    ],
    "group": "marker",
    "semantic": "grave / marker / prop-support tile",
    "walkable_default": False,
    "tags": [
      "prop",
      "marker",
      "support"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "15,29": {
    "id": "ash_a5_r29_c15",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      15,
      29
    ],
    "group": "marker",
    "semantic": "grave / marker / prop-support tile",
    "walkable_default": False,
    "tags": [
      "prop",
      "marker",
      "support"
    ],
    "notes": "Provisional semantic label derived from tileset zone; refine individual tiles later if needed."
  },
  "0,30": {
    "id": "ash_a5_r30_c00",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      0,
      30
    ],
    "group": "empty",
    "semantic": "unused / empty row",
    "walkable_default": False,
    "tags": [
      "empty"
    ],
    "notes": "Bottom rows are empty in source sheet."
  },
  "1,30": {
    "id": "ash_a5_r30_c01",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      1,
      30
    ],
    "group": "empty",
    "semantic": "unused / empty row",
    "walkable_default": False,
    "tags": [
      "empty"
    ],
    "notes": "Bottom rows are empty in source sheet."
  },
  "2,30": {
    "id": "ash_a5_r30_c02",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      2,
      30
    ],
    "group": "empty",
    "semantic": "unused / empty row",
    "walkable_default": False,
    "tags": [
      "empty"
    ],
    "notes": "Bottom rows are empty in source sheet."
  },
  "3,30": {
    "id": "ash_a5_r30_c03",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      3,
      30
    ],
    "group": "empty",
    "semantic": "unused / empty row",
    "walkable_default": False,
    "tags": [
      "empty"
    ],
    "notes": "Bottom rows are empty in source sheet."
  },
  "4,30": {
    "id": "ash_a5_r30_c04",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      4,
      30
    ],
    "group": "empty",
    "semantic": "unused / empty row",
    "walkable_default": False,
    "tags": [
      "empty"
    ],
    "notes": "Bottom rows are empty in source sheet."
  },
  "5,30": {
    "id": "ash_a5_r30_c05",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      5,
      30
    ],
    "group": "empty",
    "semantic": "unused / empty row",
    "walkable_default": False,
    "tags": [
      "empty"
    ],
    "notes": "Bottom rows are empty in source sheet."
  },
  "6,30": {
    "id": "ash_a5_r30_c06",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      6,
      30
    ],
    "group": "empty",
    "semantic": "unused / empty row",
    "walkable_default": False,
    "tags": [
      "empty"
    ],
    "notes": "Bottom rows are empty in source sheet."
  },
  "7,30": {
    "id": "ash_a5_r30_c07",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      7,
      30
    ],
    "group": "empty",
    "semantic": "unused / empty row",
    "walkable_default": False,
    "tags": [
      "empty"
    ],
    "notes": "Bottom rows are empty in source sheet."
  },
  "8,30": {
    "id": "ash_a5_r30_c08",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      8,
      30
    ],
    "group": "empty",
    "semantic": "unused / empty row",
    "walkable_default": False,
    "tags": [
      "empty"
    ],
    "notes": "Bottom rows are empty in source sheet."
  },
  "9,30": {
    "id": "ash_a5_r30_c09",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      9,
      30
    ],
    "group": "empty",
    "semantic": "unused / empty row",
    "walkable_default": False,
    "tags": [
      "empty"
    ],
    "notes": "Bottom rows are empty in source sheet."
  },
  "10,30": {
    "id": "ash_a5_r30_c10",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      10,
      30
    ],
    "group": "empty",
    "semantic": "unused / empty row",
    "walkable_default": False,
    "tags": [
      "empty"
    ],
    "notes": "Bottom rows are empty in source sheet."
  },
  "11,30": {
    "id": "ash_a5_r30_c11",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      11,
      30
    ],
    "group": "empty",
    "semantic": "unused / empty row",
    "walkable_default": False,
    "tags": [
      "empty"
    ],
    "notes": "Bottom rows are empty in source sheet."
  },
  "12,30": {
    "id": "ash_a5_r30_c12",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      12,
      30
    ],
    "group": "empty",
    "semantic": "unused / empty row",
    "walkable_default": False,
    "tags": [
      "empty"
    ],
    "notes": "Bottom rows are empty in source sheet."
  },
  "13,30": {
    "id": "ash_a5_r30_c13",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      13,
      30
    ],
    "group": "empty",
    "semantic": "unused / empty row",
    "walkable_default": False,
    "tags": [
      "empty"
    ],
    "notes": "Bottom rows are empty in source sheet."
  },
  "14,30": {
    "id": "ash_a5_r30_c14",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      14,
      30
    ],
    "group": "empty",
    "semantic": "unused / empty row",
    "walkable_default": False,
    "tags": [
      "empty"
    ],
    "notes": "Bottom rows are empty in source sheet."
  },
  "15,30": {
    "id": "ash_a5_r30_c15",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      15,
      30
    ],
    "group": "empty",
    "semantic": "unused / empty row",
    "walkable_default": False,
    "tags": [
      "empty"
    ],
    "notes": "Bottom rows are empty in source sheet."
  },
  "0,31": {
    "id": "ash_a5_r31_c00",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      0,
      31
    ],
    "group": "empty",
    "semantic": "unused / empty row",
    "walkable_default": False,
    "tags": [
      "empty"
    ],
    "notes": "Bottom rows are empty in source sheet."
  },
  "1,31": {
    "id": "ash_a5_r31_c01",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      1,
      31
    ],
    "group": "empty",
    "semantic": "unused / empty row",
    "walkable_default": False,
    "tags": [
      "empty"
    ],
    "notes": "Bottom rows are empty in source sheet."
  },
  "2,31": {
    "id": "ash_a5_r31_c02",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      2,
      31
    ],
    "group": "empty",
    "semantic": "unused / empty row",
    "walkable_default": False,
    "tags": [
      "empty"
    ],
    "notes": "Bottom rows are empty in source sheet."
  },
  "3,31": {
    "id": "ash_a5_r31_c03",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      3,
      31
    ],
    "group": "empty",
    "semantic": "unused / empty row",
    "walkable_default": False,
    "tags": [
      "empty"
    ],
    "notes": "Bottom rows are empty in source sheet."
  },
  "4,31": {
    "id": "ash_a5_r31_c04",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      4,
      31
    ],
    "group": "empty",
    "semantic": "unused / empty row",
    "walkable_default": False,
    "tags": [
      "empty"
    ],
    "notes": "Bottom rows are empty in source sheet."
  },
  "5,31": {
    "id": "ash_a5_r31_c05",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      5,
      31
    ],
    "group": "empty",
    "semantic": "unused / empty row",
    "walkable_default": False,
    "tags": [
      "empty"
    ],
    "notes": "Bottom rows are empty in source sheet."
  },
  "6,31": {
    "id": "ash_a5_r31_c06",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      6,
      31
    ],
    "group": "empty",
    "semantic": "unused / empty row",
    "walkable_default": False,
    "tags": [
      "empty"
    ],
    "notes": "Bottom rows are empty in source sheet."
  },
  "7,31": {
    "id": "ash_a5_r31_c07",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      7,
      31
    ],
    "group": "empty",
    "semantic": "unused / empty row",
    "walkable_default": False,
    "tags": [
      "empty"
    ],
    "notes": "Bottom rows are empty in source sheet."
  },
  "8,31": {
    "id": "ash_a5_r31_c08",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      8,
      31
    ],
    "group": "empty",
    "semantic": "unused / empty row",
    "walkable_default": False,
    "tags": [
      "empty"
    ],
    "notes": "Bottom rows are empty in source sheet."
  },
  "9,31": {
    "id": "ash_a5_r31_c09",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      9,
      31
    ],
    "group": "empty",
    "semantic": "unused / empty row",
    "walkable_default": False,
    "tags": [
      "empty"
    ],
    "notes": "Bottom rows are empty in source sheet."
  },
  "10,31": {
    "id": "ash_a5_r31_c10",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      10,
      31
    ],
    "group": "empty",
    "semantic": "unused / empty row",
    "walkable_default": False,
    "tags": [
      "empty"
    ],
    "notes": "Bottom rows are empty in source sheet."
  },
  "11,31": {
    "id": "ash_a5_r31_c11",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      11,
      31
    ],
    "group": "empty",
    "semantic": "unused / empty row",
    "walkable_default": False,
    "tags": [
      "empty"
    ],
    "notes": "Bottom rows are empty in source sheet."
  },
  "12,31": {
    "id": "ash_a5_r31_c12",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      12,
      31
    ],
    "group": "empty",
    "semantic": "unused / empty row",
    "walkable_default": False,
    "tags": [
      "empty"
    ],
    "notes": "Bottom rows are empty in source sheet."
  },
  "13,31": {
    "id": "ash_a5_r31_c13",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      13,
      31
    ],
    "group": "empty",
    "semantic": "unused / empty row",
    "walkable_default": False,
    "tags": [
      "empty"
    ],
    "notes": "Bottom rows are empty in source sheet."
  },
  "14,31": {
    "id": "ash_a5_r31_c14",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      14,
      31
    ],
    "group": "empty",
    "semantic": "unused / empty row",
    "walkable_default": False,
    "tags": [
      "empty"
    ],
    "notes": "Bottom rows are empty in source sheet."
  },
  "15,31": {
    "id": "ash_a5_r31_c15",
    "sheet": "tf_A5_ashlands_2",
    "coord": [
      15,
      31
    ],
    "group": "empty",
    "semantic": "unused / empty row",
    "walkable_default": False,
    "tags": [
      "empty"
    ],
    "notes": "Bottom rows are empty in source sheet."
  }
}

ASHLAND_A5_GROUPS = {
  "ground_round": [
    "ash_a5_r00_c00",
    "ash_a5_r00_c01",
    "ash_a5_r00_c02",
    "ash_a5_r00_c03",
    "ash_a5_r00_c04",
    "ash_a5_r00_c05",
    "ash_a5_r00_c06",
    "ash_a5_r00_c07",
    "ash_a5_r00_c08",
    "ash_a5_r00_c09",
    "ash_a5_r00_c10",
    "ash_a5_r00_c11",
    "ash_a5_r00_c12",
    "ash_a5_r00_c13",
    "ash_a5_r00_c14",
    "ash_a5_r00_c15",
    "ash_a5_r01_c00",
    "ash_a5_r01_c01",
    "ash_a5_r01_c02",
    "ash_a5_r01_c03",
    "ash_a5_r01_c04",
    "ash_a5_r01_c05",
    "ash_a5_r01_c06",
    "ash_a5_r01_c07",
    "ash_a5_r01_c08",
    "ash_a5_r01_c09",
    "ash_a5_r01_c10",
    "ash_a5_r01_c11",
    "ash_a5_r01_c12",
    "ash_a5_r01_c13",
    "ash_a5_r01_c14",
    "ash_a5_r01_c15"
  ],
  "ground_square": [
    "ash_a5_r02_c00",
    "ash_a5_r02_c01",
    "ash_a5_r02_c02",
    "ash_a5_r02_c03",
    "ash_a5_r02_c04",
    "ash_a5_r02_c05",
    "ash_a5_r02_c06",
    "ash_a5_r02_c07",
    "ash_a5_r02_c08",
    "ash_a5_r02_c09",
    "ash_a5_r02_c10",
    "ash_a5_r02_c11",
    "ash_a5_r02_c12",
    "ash_a5_r02_c13",
    "ash_a5_r02_c14",
    "ash_a5_r02_c15",
    "ash_a5_r03_c00",
    "ash_a5_r03_c01",
    "ash_a5_r03_c02",
    "ash_a5_r03_c03",
    "ash_a5_r03_c04",
    "ash_a5_r03_c05",
    "ash_a5_r03_c06",
    "ash_a5_r03_c07",
    "ash_a5_r03_c08",
    "ash_a5_r03_c09",
    "ash_a5_r03_c10",
    "ash_a5_r03_c11",
    "ash_a5_r03_c12",
    "ash_a5_r03_c13",
    "ash_a5_r03_c14",
    "ash_a5_r03_c15"
  ],
  "ground_dark": [
    "ash_a5_r04_c00",
    "ash_a5_r04_c01",
    "ash_a5_r04_c02",
    "ash_a5_r04_c03",
    "ash_a5_r04_c04",
    "ash_a5_r04_c05",
    "ash_a5_r04_c06",
    "ash_a5_r04_c07",
    "ash_a5_r04_c08",
    "ash_a5_r04_c09",
    "ash_a5_r04_c10",
    "ash_a5_r04_c11",
    "ash_a5_r04_c12",
    "ash_a5_r04_c13",
    "ash_a5_r04_c14",
    "ash_a5_r04_c15",
    "ash_a5_r05_c00",
    "ash_a5_r05_c01",
    "ash_a5_r05_c02",
    "ash_a5_r05_c03",
    "ash_a5_r05_c04",
    "ash_a5_r05_c05",
    "ash_a5_r05_c06",
    "ash_a5_r05_c07",
    "ash_a5_r05_c08",
    "ash_a5_r05_c09",
    "ash_a5_r05_c10",
    "ash_a5_r05_c11",
    "ash_a5_r05_c12",
    "ash_a5_r05_c13",
    "ash_a5_r05_c14",
    "ash_a5_r05_c15"
  ],
  "lava_small": [
    "ash_a5_r06_c00",
    "ash_a5_r06_c01",
    "ash_a5_r06_c02",
    "ash_a5_r06_c03",
    "ash_a5_r06_c04",
    "ash_a5_r06_c05",
    "ash_a5_r06_c06",
    "ash_a5_r06_c07",
    "ash_a5_r06_c08",
    "ash_a5_r06_c09",
    "ash_a5_r06_c10",
    "ash_a5_r06_c11",
    "ash_a5_r06_c12",
    "ash_a5_r06_c13",
    "ash_a5_r06_c14",
    "ash_a5_r06_c15",
    "ash_a5_r07_c00",
    "ash_a5_r07_c01",
    "ash_a5_r07_c02",
    "ash_a5_r07_c03",
    "ash_a5_r07_c04",
    "ash_a5_r07_c05",
    "ash_a5_r07_c06",
    "ash_a5_r07_c07",
    "ash_a5_r07_c08",
    "ash_a5_r07_c09",
    "ash_a5_r07_c10",
    "ash_a5_r07_c11",
    "ash_a5_r07_c12",
    "ash_a5_r07_c13",
    "ash_a5_r07_c14",
    "ash_a5_r07_c15"
  ],
  "lava_full": [
    "ash_a5_r08_c00",
    "ash_a5_r08_c01",
    "ash_a5_r08_c02",
    "ash_a5_r08_c03",
    "ash_a5_r08_c04",
    "ash_a5_r08_c05",
    "ash_a5_r08_c06",
    "ash_a5_r08_c07",
    "ash_a5_r08_c08",
    "ash_a5_r08_c09",
    "ash_a5_r08_c10",
    "ash_a5_r08_c11",
    "ash_a5_r08_c12",
    "ash_a5_r08_c13",
    "ash_a5_r08_c14",
    "ash_a5_r08_c15",
    "ash_a5_r09_c00",
    "ash_a5_r09_c01",
    "ash_a5_r09_c02",
    "ash_a5_r09_c03",
    "ash_a5_r09_c04",
    "ash_a5_r09_c05",
    "ash_a5_r09_c06",
    "ash_a5_r09_c07",
    "ash_a5_r09_c08",
    "ash_a5_r09_c09",
    "ash_a5_r09_c10",
    "ash_a5_r09_c11",
    "ash_a5_r09_c12",
    "ash_a5_r09_c13",
    "ash_a5_r09_c14",
    "ash_a5_r09_c15"
  ],
  "path_cobble": [
    "ash_a5_r10_c00",
    "ash_a5_r10_c01",
    "ash_a5_r10_c02",
    "ash_a5_r10_c03",
    "ash_a5_r10_c04",
    "ash_a5_r10_c05",
    "ash_a5_r10_c06",
    "ash_a5_r10_c07",
    "ash_a5_r10_c08",
    "ash_a5_r10_c09",
    "ash_a5_r10_c10",
    "ash_a5_r10_c11",
    "ash_a5_r10_c12",
    "ash_a5_r10_c13",
    "ash_a5_r10_c14",
    "ash_a5_r10_c15",
    "ash_a5_r11_c00",
    "ash_a5_r11_c01",
    "ash_a5_r11_c02",
    "ash_a5_r11_c03",
    "ash_a5_r11_c04",
    "ash_a5_r11_c05",
    "ash_a5_r11_c06",
    "ash_a5_r11_c07",
    "ash_a5_r11_c08",
    "ash_a5_r11_c09",
    "ash_a5_r11_c10",
    "ash_a5_r11_c11",
    "ash_a5_r11_c12",
    "ash_a5_r11_c13",
    "ash_a5_r11_c14",
    "ash_a5_r11_c15"
  ],
  "gravel_patch": [
    "ash_a5_r12_c00",
    "ash_a5_r12_c01",
    "ash_a5_r12_c02",
    "ash_a5_r12_c03",
    "ash_a5_r12_c04",
    "ash_a5_r12_c05",
    "ash_a5_r12_c06",
    "ash_a5_r12_c07",
    "ash_a5_r12_c08",
    "ash_a5_r12_c09",
    "ash_a5_r12_c10",
    "ash_a5_r12_c11",
    "ash_a5_r12_c12",
    "ash_a5_r12_c13",
    "ash_a5_r12_c14",
    "ash_a5_r12_c15",
    "ash_a5_r13_c00",
    "ash_a5_r13_c01",
    "ash_a5_r13_c02",
    "ash_a5_r13_c03",
    "ash_a5_r13_c04",
    "ash_a5_r13_c05",
    "ash_a5_r13_c06",
    "ash_a5_r13_c07",
    "ash_a5_r13_c08",
    "ash_a5_r13_c09",
    "ash_a5_r13_c10",
    "ash_a5_r13_c11",
    "ash_a5_r13_c12",
    "ash_a5_r13_c13",
    "ash_a5_r13_c14",
    "ash_a5_r13_c15"
  ],
  "transition_edge": [
    "ash_a5_r14_c00",
    "ash_a5_r14_c01",
    "ash_a5_r14_c02",
    "ash_a5_r14_c03",
    "ash_a5_r14_c04",
    "ash_a5_r14_c05",
    "ash_a5_r14_c06",
    "ash_a5_r14_c07",
    "ash_a5_r14_c08",
    "ash_a5_r14_c09",
    "ash_a5_r14_c10",
    "ash_a5_r14_c11",
    "ash_a5_r14_c12",
    "ash_a5_r14_c13",
    "ash_a5_r14_c14",
    "ash_a5_r14_c15"
  ],
  "plateau_top": [
    "ash_a5_r15_c00",
    "ash_a5_r15_c01",
    "ash_a5_r15_c02",
    "ash_a5_r15_c03",
    "ash_a5_r15_c04",
    "ash_a5_r15_c05",
    "ash_a5_r15_c06",
    "ash_a5_r15_c07",
    "ash_a5_r15_c08",
    "ash_a5_r15_c09",
    "ash_a5_r15_c10",
    "ash_a5_r15_c11",
    "ash_a5_r15_c12",
    "ash_a5_r15_c13",
    "ash_a5_r15_c14",
    "ash_a5_r15_c15"
  ],
  "wall_cap": [
    "ash_a5_r16_c00",
    "ash_a5_r16_c01",
    "ash_a5_r16_c02",
    "ash_a5_r16_c03",
    "ash_a5_r16_c04",
    "ash_a5_r16_c05",
    "ash_a5_r16_c06",
    "ash_a5_r16_c07",
    "ash_a5_r16_c08",
    "ash_a5_r16_c09",
    "ash_a5_r16_c10",
    "ash_a5_r16_c11",
    "ash_a5_r16_c12",
    "ash_a5_r16_c13",
    "ash_a5_r16_c14",
    "ash_a5_r16_c15",
    "ash_a5_r17_c00",
    "ash_a5_r17_c01",
    "ash_a5_r17_c02",
    "ash_a5_r17_c03",
    "ash_a5_r17_c04",
    "ash_a5_r17_c05",
    "ash_a5_r17_c06",
    "ash_a5_r17_c07",
    "ash_a5_r17_c08",
    "ash_a5_r17_c09",
    "ash_a5_r17_c10",
    "ash_a5_r17_c11",
    "ash_a5_r17_c12",
    "ash_a5_r17_c13",
    "ash_a5_r17_c14",
    "ash_a5_r17_c15"
  ],
  "wall_face": [
    "ash_a5_r18_c00",
    "ash_a5_r18_c01",
    "ash_a5_r18_c02",
    "ash_a5_r18_c03",
    "ash_a5_r18_c04",
    "ash_a5_r18_c05",
    "ash_a5_r18_c06",
    "ash_a5_r18_c07",
    "ash_a5_r18_c08",
    "ash_a5_r18_c09",
    "ash_a5_r18_c10",
    "ash_a5_r18_c11",
    "ash_a5_r18_c12",
    "ash_a5_r18_c13",
    "ash_a5_r18_c14",
    "ash_a5_r18_c15",
    "ash_a5_r19_c00",
    "ash_a5_r19_c01",
    "ash_a5_r19_c02",
    "ash_a5_r19_c03",
    "ash_a5_r19_c04",
    "ash_a5_r19_c05",
    "ash_a5_r19_c06",
    "ash_a5_r19_c07",
    "ash_a5_r19_c08",
    "ash_a5_r19_c09",
    "ash_a5_r19_c10",
    "ash_a5_r19_c11",
    "ash_a5_r19_c12",
    "ash_a5_r19_c13",
    "ash_a5_r19_c14",
    "ash_a5_r19_c15"
  ],
  "stairs_upper": [
    "ash_a5_r20_c00",
    "ash_a5_r20_c01",
    "ash_a5_r20_c02",
    "ash_a5_r20_c03",
    "ash_a5_r20_c04",
    "ash_a5_r20_c05",
    "ash_a5_r20_c06",
    "ash_a5_r20_c07",
    "ash_a5_r20_c08",
    "ash_a5_r20_c09",
    "ash_a5_r20_c10",
    "ash_a5_r20_c11",
    "ash_a5_r20_c12",
    "ash_a5_r20_c13",
    "ash_a5_r20_c14",
    "ash_a5_r20_c15"
  ],
  "stairs_lower": [
    "ash_a5_r21_c00",
    "ash_a5_r21_c01",
    "ash_a5_r21_c02",
    "ash_a5_r21_c03",
    "ash_a5_r21_c04",
    "ash_a5_r21_c05",
    "ash_a5_r21_c06",
    "ash_a5_r21_c07",
    "ash_a5_r21_c08",
    "ash_a5_r21_c09",
    "ash_a5_r21_c10",
    "ash_a5_r21_c11",
    "ash_a5_r21_c12",
    "ash_a5_r21_c13",
    "ash_a5_r21_c14",
    "ash_a5_r21_c15"
  ],
  "ruin_floor": [
    "ash_a5_r22_c00",
    "ash_a5_r22_c01",
    "ash_a5_r22_c02",
    "ash_a5_r22_c03",
    "ash_a5_r22_c04",
    "ash_a5_r22_c05",
    "ash_a5_r22_c06",
    "ash_a5_r22_c07",
    "ash_a5_r22_c08",
    "ash_a5_r22_c09",
    "ash_a5_r22_c10",
    "ash_a5_r22_c11",
    "ash_a5_r22_c12",
    "ash_a5_r22_c13",
    "ash_a5_r22_c14",
    "ash_a5_r22_c15"
  ],
  "ruin_wall": [
    "ash_a5_r23_c00",
    "ash_a5_r23_c01",
    "ash_a5_r23_c02",
    "ash_a5_r23_c03",
    "ash_a5_r23_c04",
    "ash_a5_r23_c05",
    "ash_a5_r23_c06",
    "ash_a5_r23_c07",
    "ash_a5_r23_c08",
    "ash_a5_r23_c09",
    "ash_a5_r23_c10",
    "ash_a5_r23_c11",
    "ash_a5_r23_c12",
    "ash_a5_r23_c13",
    "ash_a5_r23_c14",
    "ash_a5_r23_c15"
  ],
  "cave_mouth": [
    "ash_a5_r24_c00",
    "ash_a5_r24_c01",
    "ash_a5_r24_c02",
    "ash_a5_r24_c03",
    "ash_a5_r24_c04",
    "ash_a5_r24_c05",
    "ash_a5_r24_c06",
    "ash_a5_r24_c07",
    "ash_a5_r24_c08",
    "ash_a5_r24_c09",
    "ash_a5_r24_c10",
    "ash_a5_r24_c11",
    "ash_a5_r24_c12",
    "ash_a5_r24_c13",
    "ash_a5_r24_c14",
    "ash_a5_r24_c15",
    "ash_a5_r25_c00",
    "ash_a5_r25_c01",
    "ash_a5_r25_c02",
    "ash_a5_r25_c03",
    "ash_a5_r25_c04",
    "ash_a5_r25_c05",
    "ash_a5_r25_c06",
    "ash_a5_r25_c07",
    "ash_a5_r25_c08",
    "ash_a5_r25_c09",
    "ash_a5_r25_c10",
    "ash_a5_r25_c11",
    "ash_a5_r25_c12",
    "ash_a5_r25_c13",
    "ash_a5_r25_c14",
    "ash_a5_r25_c15"
  ],
  "cave_wall": [
    "ash_a5_r26_c00",
    "ash_a5_r26_c01",
    "ash_a5_r26_c02",
    "ash_a5_r26_c03",
    "ash_a5_r26_c04",
    "ash_a5_r26_c05",
    "ash_a5_r26_c06",
    "ash_a5_r26_c07",
    "ash_a5_r26_c08",
    "ash_a5_r26_c09",
    "ash_a5_r26_c10",
    "ash_a5_r26_c11",
    "ash_a5_r26_c12",
    "ash_a5_r26_c13",
    "ash_a5_r26_c14",
    "ash_a5_r26_c15",
    "ash_a5_r27_c00",
    "ash_a5_r27_c01",
    "ash_a5_r27_c02",
    "ash_a5_r27_c03",
    "ash_a5_r27_c04",
    "ash_a5_r27_c05",
    "ash_a5_r27_c06",
    "ash_a5_r27_c07",
    "ash_a5_r27_c08",
    "ash_a5_r27_c09",
    "ash_a5_r27_c10",
    "ash_a5_r27_c11",
    "ash_a5_r27_c12",
    "ash_a5_r27_c13",
    "ash_a5_r27_c14",
    "ash_a5_r27_c15"
  ],
  "debris": [
    "ash_a5_r28_c00",
    "ash_a5_r28_c01",
    "ash_a5_r28_c02",
    "ash_a5_r28_c03",
    "ash_a5_r28_c04",
    "ash_a5_r28_c05",
    "ash_a5_r28_c06",
    "ash_a5_r28_c07",
    "ash_a5_r28_c08",
    "ash_a5_r28_c09",
    "ash_a5_r28_c10",
    "ash_a5_r28_c11",
    "ash_a5_r28_c12",
    "ash_a5_r28_c13",
    "ash_a5_r28_c14",
    "ash_a5_r28_c15"
  ],
  "marker": [
    "ash_a5_r29_c00",
    "ash_a5_r29_c01",
    "ash_a5_r29_c02",
    "ash_a5_r29_c03",
    "ash_a5_r29_c04",
    "ash_a5_r29_c05",
    "ash_a5_r29_c06",
    "ash_a5_r29_c07",
    "ash_a5_r29_c08",
    "ash_a5_r29_c09",
    "ash_a5_r29_c10",
    "ash_a5_r29_c11",
    "ash_a5_r29_c12",
    "ash_a5_r29_c13",
    "ash_a5_r29_c14",
    "ash_a5_r29_c15"
  ],
  "empty": [
    "ash_a5_r30_c00",
    "ash_a5_r30_c01",
    "ash_a5_r30_c02",
    "ash_a5_r30_c03",
    "ash_a5_r30_c04",
    "ash_a5_r30_c05",
    "ash_a5_r30_c06",
    "ash_a5_r30_c07",
    "ash_a5_r30_c08",
    "ash_a5_r30_c09",
    "ash_a5_r30_c10",
    "ash_a5_r30_c11",
    "ash_a5_r30_c12",
    "ash_a5_r30_c13",
    "ash_a5_r30_c14",
    "ash_a5_r30_c15",
    "ash_a5_r31_c00",
    "ash_a5_r31_c01",
    "ash_a5_r31_c02",
    "ash_a5_r31_c03",
    "ash_a5_r31_c04",
    "ash_a5_r31_c05",
    "ash_a5_r31_c06",
    "ash_a5_r31_c07",
    "ash_a5_r31_c08",
    "ash_a5_r31_c09",
    "ash_a5_r31_c10",
    "ash_a5_r31_c11",
    "ash_a5_r31_c12",
    "ash_a5_r31_c13",
    "ash_a5_r31_c14",
    "ash_a5_r31_c15"
  ]
}


# Semantic schema v2: adjacency-aware role metadata for deterministic tile selection.
ASHLAND_A5_SEMANTIC_SCHEMA_VERSION = 2


def _group_ids(group: str) -> list[str]:
    return list(ASHLAND_A5_GROUPS.get(group, []))


def _slice_ids(group: str, start: int, count: int) -> list[str]:
    ids = _group_ids(group)
    if not ids:
        return []
    return ids[start : start + count]


def _quarter_ids(group: str, quarter_index: int) -> list[str]:
    ids = _group_ids(group)
    if not ids:
        return []

    chunk_size = max(1, len(ids) // 4)
    start = min(len(ids) - 1, max(0, quarter_index) * chunk_size)
    end = min(len(ids), start + chunk_size)
    return ids[start:end]


ASHLAND_A5_ADJACENCY_RULES: list[dict[str, object]] = []


# Ground and path-like groups share the same adjacency role model.
for _group in (
    "ground_round",
    "ground_square",
    "ground_dark",
    "path_cobble",
    "gravel_patch",
):
    ASHLAND_A5_ADJACENCY_RULES.extend(
        [
            {
                "target_group": _group,
                "role": "fill",
                "orientation": "center",
                "transitions_from": [_group],
                "transitions_to": ["*"],
                "structure_role": "base_fill",
                "tile_ids": _slice_ids(_group, 0, 10),
            },
            {
                "target_group": _group,
                "role": "edge",
                "orientation": "top",
                "transitions_from": [_group],
                "transitions_to": ["*"],
                "structure_role": "edge",
                "tile_ids": _quarter_ids(_group, 0),
            },
            {
                "target_group": _group,
                "role": "edge",
                "orientation": "right",
                "transitions_from": [_group],
                "transitions_to": ["*"],
                "structure_role": "edge",
                "tile_ids": _quarter_ids(_group, 1),
            },
            {
                "target_group": _group,
                "role": "edge",
                "orientation": "bottom",
                "transitions_from": [_group],
                "transitions_to": ["*"],
                "structure_role": "edge",
                "tile_ids": _quarter_ids(_group, 2),
            },
            {
                "target_group": _group,
                "role": "edge",
                "orientation": "left",
                "transitions_from": [_group],
                "transitions_to": ["*"],
                "structure_role": "edge",
                "tile_ids": _quarter_ids(_group, 3),
            },
            {
                "target_group": _group,
                "role": "corner_outer",
                "orientation": "top_left",
                "transitions_from": [_group],
                "transitions_to": ["*"],
                "structure_role": "corner_outer",
                "tile_ids": _quarter_ids(_group, 0)[:2],
            },
            {
                "target_group": _group,
                "role": "corner_outer",
                "orientation": "top_right",
                "transitions_from": [_group],
                "transitions_to": ["*"],
                "structure_role": "corner_outer",
                "tile_ids": _quarter_ids(_group, 1)[:2],
            },
            {
                "target_group": _group,
                "role": "corner_outer",
                "orientation": "bottom_right",
                "transitions_from": [_group],
                "transitions_to": ["*"],
                "structure_role": "corner_outer",
                "tile_ids": _quarter_ids(_group, 2)[:2],
            },
            {
                "target_group": _group,
                "role": "corner_outer",
                "orientation": "bottom_left",
                "transitions_from": [_group],
                "transitions_to": ["*"],
                "structure_role": "corner_outer",
                "tile_ids": _quarter_ids(_group, 3)[:2],
            },
            {
                "target_group": _group,
                "role": "corner_inner",
                "orientation": "top_left",
                "transitions_from": [_group],
                "transitions_to": ["*"],
                "structure_role": "corner_inner",
                "tile_ids": _quarter_ids(_group, 0)[2:4],
            },
            {
                "target_group": _group,
                "role": "corner_inner",
                "orientation": "top_right",
                "transitions_from": [_group],
                "transitions_to": ["*"],
                "structure_role": "corner_inner",
                "tile_ids": _quarter_ids(_group, 1)[2:4],
            },
            {
                "target_group": _group,
                "role": "corner_inner",
                "orientation": "bottom_right",
                "transitions_from": [_group],
                "transitions_to": ["*"],
                "structure_role": "corner_inner",
                "tile_ids": _quarter_ids(_group, 2)[2:4],
            },
            {
                "target_group": _group,
                "role": "corner_inner",
                "orientation": "bottom_left",
                "transitions_from": [_group],
                "transitions_to": ["*"],
                "structure_role": "corner_inner",
                "tile_ids": _quarter_ids(_group, 3)[2:4],
            },
        ]
    )


# Ruin structures.
ASHLAND_A5_ADJACENCY_RULES.extend(
    [
        {
            "target_group": "ruin_floor",
            "role": "fill",
            "orientation": "center",
            "transitions_from": ["ruin_floor"],
            "transitions_to": ["ruin_wall", "wall_cap"],
            "structure_role": "ruin_floor",
            "tile_ids": _group_ids("ruin_floor"),
        },
        {
            "target_group": "ruin_wall",
            "role": "edge",
            "orientation": "top",
            "transitions_from": ["ruin_wall"],
            "transitions_to": ["ruin_floor"],
            "structure_role": "wall_cap",
            "tile_ids": _slice_ids("wall_cap", 0, 8),
        },
        {
            "target_group": "ruin_wall",
            "role": "edge",
            "orientation": "left",
            "transitions_from": ["ruin_wall"],
            "transitions_to": ["ruin_floor"],
            "structure_role": "wall_face",
            "tile_ids": _slice_ids("ruin_wall", 0, 4),
        },
        {
            "target_group": "ruin_wall",
            "role": "edge",
            "orientation": "right",
            "transitions_from": ["ruin_wall"],
            "transitions_to": ["ruin_floor"],
            "structure_role": "wall_face",
            "tile_ids": _slice_ids("ruin_wall", 4, 4),
        },
        {
            "target_group": "ruin_wall",
            "role": "edge",
            "orientation": "bottom",
            "transitions_from": ["ruin_wall"],
            "transitions_to": ["ruin_floor"],
            "structure_role": "wall_face",
            "tile_ids": _slice_ids("ruin_wall", 8, 8),
        },
        {
            "target_group": "ruin_wall",
            "role": "corner_outer",
            "orientation": "top_left",
            "transitions_from": ["ruin_wall"],
            "transitions_to": ["ruin_floor"],
            "structure_role": "corner_cap",
            "tile_ids": _slice_ids("wall_cap", 8, 2),
        },
        {
            "target_group": "ruin_wall",
            "role": "corner_outer",
            "orientation": "top_right",
            "transitions_from": ["ruin_wall"],
            "transitions_to": ["ruin_floor"],
            "structure_role": "corner_cap",
            "tile_ids": _slice_ids("wall_cap", 10, 2),
        },
    ]
)


# Cave structures.
ASHLAND_A5_ADJACENCY_RULES.extend(
    [
        {
            "target_group": "cave_wall",
            "role": "edge",
            "orientation": "top",
            "transitions_from": ["cave_wall"],
            "transitions_to": ["ground_dark", "cave_mouth"],
            "structure_role": "cave_rim",
            "tile_ids": _slice_ids("cave_wall", 0, 6),
        },
        {
            "target_group": "cave_wall",
            "role": "edge",
            "orientation": "bottom",
            "transitions_from": ["cave_wall"],
            "transitions_to": ["ground_dark"],
            "structure_role": "cave_rim",
            "tile_ids": _slice_ids("cave_wall", 6, 6),
        },
        {
            "target_group": "cave_wall",
            "role": "edge",
            "orientation": "left",
            "transitions_from": ["cave_wall"],
            "transitions_to": ["ground_dark"],
            "structure_role": "cave_side",
            "tile_ids": _slice_ids("cave_wall", 12, 4),
        },
        {
            "target_group": "cave_wall",
            "role": "edge",
            "orientation": "right",
            "transitions_from": ["cave_wall"],
            "transitions_to": ["ground_dark"],
            "structure_role": "cave_side",
            "tile_ids": _slice_ids("cave_wall", 16, 4),
        },
        {
            "target_group": "cave_mouth",
            "role": "fill",
            "orientation": "center",
            "transitions_from": ["cave_mouth"],
            "transitions_to": ["ground_dark", "cave_wall"],
            "structure_role": "cave_mouth",
            "tile_ids": _group_ids("cave_mouth"),
        },
    ]
)


# Stair orientation metadata.
ASHLAND_A5_ADJACENCY_RULES.extend(
    [
        {
            "target_group": "stairs_upper",
            "role": "fill",
            "orientation": "center",
            "transitions_from": ["stairs_upper"],
            "transitions_to": ["stairs_lower", "path_cobble", "ground_square"],
            "structure_role": "stairs_upper",
            "tile_ids": _group_ids("stairs_upper"),
        },
        {
            "target_group": "stairs_lower",
            "role": "fill",
            "orientation": "center",
            "transitions_from": ["stairs_lower"],
            "transitions_to": ["stairs_upper", "path_cobble", "ground_square"],
            "structure_role": "stairs_lower",
            "tile_ids": _group_ids("stairs_lower"),
        },
    ]
)


# Selection metadata for the renderer. This keeps black/void-like tiles out of
# current base-layer rendering until dedicated hole/liquid layering is added.
ASHLAND_A5_SELECTION_EXCLUDED_GROUPS = {"empty"}

# These tiles are fully transparent in tf_A5_ashlands_2 and render as black
# void when used as base-layer floor in the current single-layer setup.
ASHLAND_A5_KNOWN_TRANSPARENT_TILE_IDS = {
    "ash_a5_r00_c00",
    "ash_a5_r00_c01",
    "ash_a5_r01_c00",
    "ash_a5_r01_c01",
    "ash_a5_r12_c00",
    "ash_a5_r12_c05",
    "ash_a5_r14_c02",
    "ash_a5_r14_c03",
    "ash_a5_r15_c02",
    "ash_a5_r15_c03",
}

# Audit notes where the source image does not match the original coarse semantic
# labeling in the first-pass manifest.
ASHLAND_A5_DESCRIPTION_MISMATCHES = {
    "ash_a5_r00_c00": "Fully transparent in source sheet; not valid ground fill.",
    "ash_a5_r00_c01": "Fully transparent in source sheet; not valid ground fill.",
    "ash_a5_r01_c00": "Fully transparent in source sheet; not valid ground fill.",
    "ash_a5_r01_c01": "Fully transparent in source sheet; not valid ground fill.",
    "ash_a5_r14_c02": "Fully transparent in source sheet; reserved/void-like tile.",
    "ash_a5_r14_c03": "Fully transparent in source sheet; reserved/void-like tile.",
    "ash_a5_r15_c02": "Fully transparent in source sheet; reserved/void-like tile.",
    "ash_a5_r15_c03": "Fully transparent in source sheet; reserved/void-like tile.",
}


def _build_border_groups_by_tile_id() -> dict[str, tuple[str, ...]]:
    coord_to_group = {
        tuple(entry["coord"]): str(entry["group"]) for entry in ASHLAND_A5_MANIFEST.values()
    }
    borders_by_tile_id: dict[str, tuple[str, ...]] = {}
    for entry in ASHLAND_A5_MANIFEST.values():
        col, row = entry["coord"]
        neighbor_groups: set[str] = set()
        for d_col, d_row in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            neighbor = coord_to_group.get((col + d_col, row + d_row))
            if neighbor is not None:
                neighbor_groups.add(neighbor)
        borders_by_tile_id[str(entry["id"])] = tuple(sorted(neighbor_groups))
    return borders_by_tile_id


ASHLAND_A5_TILE_BORDER_GROUPS = _build_border_groups_by_tile_id()

# Per-tile flags consumed by selection logic.
ASHLAND_A5_TILE_SELECTION_FLAGS: dict[str, dict[str, object]] = {}
for _entry in ASHLAND_A5_MANIFEST.values():
    _tile_id = str(_entry["id"])
    _group = str(_entry["group"])
    _borders_groups = ASHLAND_A5_TILE_BORDER_GROUPS.get(_tile_id, ())
    _exclude_reasons: list[str] = []
    if _group in ASHLAND_A5_SELECTION_EXCLUDED_GROUPS:
        _exclude_reasons.append("excluded_group")
    if _tile_id in ASHLAND_A5_KNOWN_TRANSPARENT_TILE_IDS:
        _exclude_reasons.append("known_transparent_tile")
    if "empty" in _borders_groups:
        _exclude_reasons.append("borders_empty_group")

    ASHLAND_A5_TILE_SELECTION_FLAGS[_tile_id] = {
        "group": _group,
        "borders_groups": list(_borders_groups),
        "exclude_from_base_selection": bool(_exclude_reasons),
        "exclude_reasons": _exclude_reasons,
        "description_mismatch_note": ASHLAND_A5_DESCRIPTION_MISMATCHES.get(_tile_id),
    }

"""Map loader for CSV-based tile maps."""

import logging
from pathlib import Path
from typing import Dict, List, Tuple, Union

from src.core import constants


def load_map(level_number: Union[int, str]) -> Dict:
    """Load a map from a CSV file for the given level number.

    Args:
        level_number: The level number to load (1-5) or "test".

    Returns:
        Dictionary containing tiles, start_pos, exit_pos, doors,
        enemies_positions, items_positions.
    """
    map_path = Path(f"data/maps/level_{level_number}.csv")

    if not map_path.exists():
        logging.error(f"Map file not found: {map_path}")
        return _create_empty_map()

    tiles: List[List[str]] = []
    start_pos: Tuple[int, int] = (0, 0)
    exit_pos: List[Tuple[int, int]] = []
    doors: List[Tuple[int, int]] = []
    enemies_positions: List[Tuple[int, int]] = []
    items_positions: Dict[Tuple[int, int], str] = {}

    try:
        with open(map_path, "r") as f:
            for row_idx, line in enumerate(f):
                line = line.rstrip("\n")
                # Handle different line lengths by padding with floor
                tile_row: List[str] = []
                for col_idx, char in enumerate(line):
                    # Map character to tile type
                    if char == "#":
                        tile_row.append("wall")
                    elif char == "P":
                        tile_row.append("floor")
                        start_pos = (col_idx, row_idx)
                    elif char in ("E", "e"):
                        tile_row.append("exit")
                        exit_pos.append((col_idx, row_idx))
                    elif char == "D":
                        tile_row.append("door")
                        doors.append((col_idx, row_idx))
                    elif char in "0123456789":
                        tile_row.append("floor")
                        enemies_positions.append((col_idx, row_idx))
                    elif char in "abcdefghijklmnopqrstuvwxyz":
                        tile_row.append("item")
                        items_positions[(col_idx, row_idx)] = char
                    elif char == ".":
                        tile_row.append("decoration")
                    elif char == "_" or char == " " or char == "":
                        tile_row.append("floor")
                    else:
                        tile_row.append("floor")

                # Pad row to MAP_WIDTH with floor tiles
                while len(tile_row) < constants.MAP_WIDTH:
                    tile_row.append("floor")
                # Truncate if longer than MAP_WIDTH
                tile_row = tile_row[: constants.MAP_WIDTH]

                tiles.append(tile_row)

            # Pad rows to MAP_HEIGHT with wall rows
            while len(tiles) < constants.MAP_HEIGHT:
                tiles.append(["wall"] * constants.MAP_WIDTH)
            # Truncate if more rows than MAP_HEIGHT
            tiles = tiles[: constants.MAP_HEIGHT]

        logging.info(f"Loaded map level {level_number}: {len(tiles[0])}x{len(tiles)}")

    except Exception as e:
        logging.error(f"Error loading map {map_path}: {e}")
        return _create_empty_map()

    return {
        "tiles": tiles,
        "start_pos": start_pos,
        "exit_pos": exit_pos,
        "doors": doors,
        "enemies_positions": enemies_positions,
        "items_positions": items_positions,
    }


def _create_empty_map() -> Dict:
    """Create an empty map with default values.

    Returns:
        Dictionary with default empty map data.
    """
    tiles = [["floor"] * constants.MAP_WIDTH for _ in range(constants.MAP_HEIGHT)]
    tiles[0] = ["wall"] * constants.MAP_WIDTH
    tiles[-1] = ["wall"] * constants.MAP_WIDTH
    for row in tiles:
        row[0] = "wall"
        row[-1] = "wall"

    return {
        "tiles": tiles,
        "start_pos": (1, 1),
        "exit_pos": [(constants.MAP_WIDTH - 2, constants.MAP_HEIGHT // 2)],
        "doors": [],
        "enemies_positions": [],
        "items_positions": {},
    }

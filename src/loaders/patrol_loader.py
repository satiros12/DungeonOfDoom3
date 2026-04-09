"""Patrol loader for Escape the Dungeon of Doom."""

import json
import logging
from pathlib import Path
from typing import List

import pygame


def load_patrols(level_number: int) -> List[List[pygame.Vector2]]:
    """Load patrol routes for a level.

    Args:
        level_number: The level number to load patrols for.

    Returns:
        List of patrol routes, each route is a list of Vector2 positions.
    """
    file_path = (
        Path(__file__).parent.parent.parent
        / "data"
        / "patrols"
        / f"level_{level_number}.json"
    )

    if not file_path.exists():
        logging.warning(f"Patrol file not found: {file_path}")
        return []

    try:
        with open(file_path, "r") as f:
            data = json.load(f)

        patrols = []
        for patrol_data in data:
            patrol_points = []
            for point in patrol_data:
                # Convert grid coordinates to pixel coordinates (center of tile)
                x = point[0] * 16 + 8  # TILE_SIZE = 16
                y = point[1] * 16 + 8
                patrol_points.append(pygame.Vector2(x, y))

            patrols.append(patrol_points)

        logging.info(f"Loaded {len(patrols)} patrol routes for level {level_number}")
        return patrols

    except (json.JSONDecodeError, IOError) as e:
        logging.error(f"Failed to load patrols: {e}")
        return []

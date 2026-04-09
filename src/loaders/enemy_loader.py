"""Enemy loader for Escape the Dungeon of Doom."""

import json
import logging
from pathlib import Path
from typing import List, Dict, Any

import pygame


def load_enemies(level_number: int) -> List[Dict[str, Any]]:
    """Load enemies for a level.

    Args:
        level_number: The level number to load enemies for.

    Returns:
        List of enemy data dictionaries with position, type, and patrol_id.
    """
    file_path = (
        Path(__file__).parent.parent.parent
        / "data"
        / "enemies"
        / f"level_{level_number}.json"
    )

    if not file_path.exists():
        logging.warning(f"Enemy file not found: {file_path}")
        return []

    try:
        with open(file_path, "r") as f:
            data = json.load(f)

        enemies = []
        for enemy_data in data:
            # Convert grid coordinates to pixel coordinates (center of tile)
            position = pygame.Vector2(
                enemy_data["position"][0] * 16 + 8,  # TILE_SIZE = 16
                enemy_data["position"][1] * 16 + 8,
            )

            enemies.append(
                {
                    "position": position,
                    "type": enemy_data.get("type", "guard"),
                    "patrol_id": enemy_data.get("patrol_id", -1),
                }
            )

        logging.info(f"Loaded {len(enemies)} enemies for level {level_number}")
        return enemies

    except (json.JSONDecodeError, IOError) as e:
        logging.error(f"Failed to load enemies: {e}")
        return []

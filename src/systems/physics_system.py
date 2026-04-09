"""Physics system for collision detection and movement resolution."""

import logging
from typing import List, Optional

import pygame

from src.core import constants
from src.entities.tilemap import TileMap
from src.entities.door import Door


class PhysicsSystem:
    """Handles collision detection and movement resolution."""

    def __init__(self) -> None:
        """Initialize the physics system."""
        self._player_size = constants.TILE_SIZE * 0.8
        self._doors: List[Door] = []
        logging.debug("PhysicsSystem initialized")

    def set_doors(self, doors: List[Door]) -> None:
        """Set the doors for collision detection.

        Args:
            doors: List of door entities.
        """
        self._doors = doors

    def check_collision(self, position: pygame.Vector2, tilemap: TileMap) -> bool:
        """Check if a position collides with walls.

        Args:
            position: The world position to check.
            tilemap: The tilemap to check against.

        Returns:
            True if there's a collision, False otherwise.
        """
        # Check all four corners of the player's bounding box
        half_size = self._player_size / 2
        corners = [
            (position.x - half_size, position.y - half_size),
            (position.x + half_size, position.y - half_size),
            (position.x - half_size, position.y + half_size),
            (position.x + half_size, position.y + half_size),
        ]

        for corner_x, corner_y in corners:
            col = int(corner_x / constants.TILE_SIZE)
            row = int(corner_y / constants.TILE_SIZE)

            if tilemap.is_wall(col, row):
                logging.debug(f"Collision with wall at cell ({col}, {row})")
                return True

            # Check for closed doors
            for door in self._doors:
                if not door.is_open:
                    door_col = int(door.position.x / constants.TILE_SIZE)
                    door_row = int(door.position.y / constants.TILE_SIZE)
                    if door_col == col and door_row == row:
                        logging.debug(
                            f"Collision with closed door at cell ({col}, {row})"
                        )
                        return True

        return False

    def resolve_move(
        self,
        position: pygame.Vector2,
        direction: pygame.Vector2,
        distance: float,
        tilemap: TileMap,
    ) -> pygame.Vector2:
        """Resolve movement with collision detection.

        Args:
            position: Current position.
            direction: Movement direction vector (normalized).
            distance: Distance to move.
            tilemap: The tilemap to check against.

        Returns:
            New position after collision resolution.
        """
        if direction.length() > 0:
            direction = direction.normalize()

        new_position = position + direction * distance

        # Check for collision and slide along walls
        if not self.check_collision(new_position, tilemap):
            return new_position

        # Try sliding along X axis
        slide_x = pygame.Vector2(direction.x, 0) * distance
        if not self.check_collision(position + slide_x, tilemap):
            return position + slide_x

        # Try sliding along Y axis
        slide_y = pygame.Vector2(0, direction.y) * distance
        if not self.check_collision(position + slide_y, tilemap):
            return position + slide_y

        # No movement possible
        return position

    def get_tile_at_position(
        self, position: pygame.Vector2, tilemap: TileMap
    ) -> Optional[str]:
        """Get the tile type at a world position.

        Args:
            position: World position.
            tilemap: The tilemap to query.

        Returns:
            Tile type string, or None if out of bounds.
        """
        col = int(position.x / constants.TILE_SIZE)
        row = int(position.y / constants.TILE_SIZE)

        if not tilemap._is_valid_tile(col, row):
            return None

        return tilemap.get_tile(col, row)

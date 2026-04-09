"""Player entity for Escape the Dungeon of Doom."""

import logging
from typing import Optional

import pygame

from src.core import constants


class Player:
    """Player entity with movement and combat capabilities."""

    def __init__(
        self,
        position: pygame.Vector2,
        rotation: float = 0.0,
        health: int = 100,
    ) -> None:
        """Initialize the player.

        Args:
            position: Initial position in world coordinates.
            rotation: Initial rotation angle in degrees.
            health: Initial health points (default 100).
        """
        self.position = position
        self.rotation = rotation
        self.health = health
        self.weapon: Optional[str] = "fists"
        self.armor: Optional[str] = "none"
        self.speed = constants.TILE_SIZE * 4  # 4 tiles per second
        self._max_health = 100
        logging.info(f"Player initialized at {position} with {health} HP")

    def move(self, direction: pygame.Vector2, dt: float) -> None:
        """Move the player in the given direction.

        Args:
            direction: Normalized direction vector.
            dt: Delta time in seconds.
        """
        if direction.length() > 0:
            direction = direction.normalize()

        speed_modifier = constants.ARMORS.get(self.armor, {}).get(
            "speed_multiplier", 1.0
        )
        actual_speed = self.speed * speed_modifier

        self.position += direction * actual_speed * dt
        logging.debug(f"Player moved to {self.position}")

    def rotate(self, angle: float, dt: float) -> None:
        """Rotate the player's view.

        Args:
            angle: Rotation angle change in degrees (positive = right turn).
            dt: Delta time in seconds.
        """
        self.rotation += angle * dt
        # Normalize rotation to 0-360
        self.rotation %= 360
        logging.debug(f"Player rotation: {self.rotation}")

    def take_damage(self, amount: float) -> None:
        """Apply damage to the player.

        Args:
            amount: Amount of damage to apply.
        """
        armor_reduction = constants.ARMORS.get(self.armor, {}).get(
            "damage_reduction", 1.0
        )
        actual_damage = amount * armor_reduction
        self.health -= actual_damage
        logging.info(f"Player took {actual_damage} damage, HP: {self.health}")

        if self.health <= 0:
            self.health = 0
            logging.warning("Player has died")

    def is_alive(self) -> bool:
        """Check if the player is alive.

        Returns:
            True if player health > 0, False otherwise.
        """
        return self.health > 0

    def get_cell_position(self) -> tuple[int, int]:
        """Get the player's tile cell position.

        Returns:
            Tuple of (column, row) coordinates.
        """
        col = int(self.position.x // constants.TILE_SIZE)
        row = int(self.position.y // constants.TILE_SIZE)
        return (col, row)

"""AI System for Escape the Dungeon of Doom."""

import logging
from typing import List

import pygame

from src.core import constants
from src.entities.enemy import Enemy
from src.entities.player import Player
from src.entities.tilemap import TileMap
from src.entities.door import Door


class AISystem:
    """Manages enemy AI behaviors and state transitions."""

    def __init__(self, level_number: int) -> None:
        """Initialize the AI system.

        Args:
            level_number: The current level number.
        """
        detection_radius = constants.LEVELS.get(level_number, {}).get(
            "detection_radius", 5
        )
        self._detection_radius = float(detection_radius)
        logging.debug(
            f"AISystem initialized with detection radius {self._detection_radius}"
        )

    def update_enemies(
        self,
        enemies: List[Enemy],
        player: Player,
        tilemap: TileMap,
        doors: List[Door],
        dt: float,
    ) -> None:
        """Update all enemies.

        Args:
            enemies: List of enemies to update.
            player: The player entity.
            tilemap: The tilemap for collision and LOS.
            doors: List of doors in the level.
            dt: Delta time in seconds.
        """
        for enemy in enemies:
            if enemy.is_alive():
                # Override detection radius with level-based value
                enemy.detection_radius = self._detection_radius
                enemy.update(dt, player.position, tilemap, doors)

    def check_detection(
        self, enemy: Enemy, player: Player, tilemap: TileMap, doors: List[Door]
    ) -> bool:
        """Check if enemy can detect the player.

        Args:
            enemy: The enemy entity.
            player: The player entity.
            tilemap: The tilemap for LOS checking.
            doors: List of doors in the level.

        Returns:
            True if player is detected, False otherwise.
        """
        dist = enemy.position.distance_to(player.position)

        if dist >= enemy.detection_radius:
            return False

        # Check line of sight
        return self.check_line_of_sight(enemy, player, tilemap, doors)

    def check_line_of_sight(
        self, enemy: Enemy, player: Player, tilemap: TileMap, doors: List[Door]
    ) -> bool:
        """Check if there is line of sight between enemy and player.

        Args:
            enemy: The enemy entity.
            player: The player entity.
            tilemap: The tilemap for wall checking.
            doors: List of doors in the level.

        Returns:
            True if there is line of sight, False otherwise.
        """
        # Direction and distance to player
        direction = player.position - enemy.position
        distance = direction.length()

        if distance == 0:
            return True

        direction = direction.normalize()

        # Raycast: check points along the line
        steps = max(1, int(distance // (constants.TILE_SIZE / 2)))

        for i in range(1, steps + 1):
            check_pos = enemy.position + direction * (distance * i / steps)
            col = int(check_pos.x // constants.TILE_SIZE)
            row = int(check_pos.y // constants.TILE_SIZE)

            # Check wall collision
            if tilemap.is_wall(col, row):
                return False

            # Check closed doors
            for door in doors:
                door_col = int(door.position.x // constants.TILE_SIZE)
                door_row = int(door.position.y // constants.TILE_SIZE)
                if door_col == col and door_row == row and not door.is_open:
                    return False

        return True

    def check_enemy_player_collision(self, enemy: Enemy, player: Player) -> bool:
        """Check if enemy collides with player (within attack range).

        Args:
            enemy: The enemy entity.
            player: The player entity.

        Returns:
            True if collision detected, False otherwise.
        """
        dist = enemy.position.distance_to(player.position)
        attack_range = constants.ENEMY_ATTACK_RANGE * constants.TILE_SIZE

        return dist < attack_range

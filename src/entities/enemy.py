"""Enemy entity with state machine for Escape the Dungeon of Doom."""

import logging
import math
from typing import List, Optional

import pygame

from src.core import constants
from src.entities.armor import Armor, NO_ARMOR


class Enemy:
    """Enemy entity with patrol, chase, and attack states."""

    def __init__(
        self,
        position: pygame.Vector2,
        enemy_type: str = "guard",
        patrol_points: Optional[List[pygame.Vector2]] = None,
        detection_radius: float = 5.0,
    ) -> None:
        """Initialize the enemy.

        Args:
            position: Initial position in world coordinates.
            enemy_type: Type of enemy (e.g., "guard").
            patrol_points: List of patrol waypoints.
            detection_radius: Detection radius in cells.
        """
        self.position = position
        self.rotation = 0.0
        self.enemy_type = enemy_type
        self.state = constants.ENEMY_STATES["PATROL"]
        self.patrol_points = patrol_points or []
        self.current_patrol_index = 0
        self.detection_radius = detection_radius
        self.attack_cooldown = 0.0
        self.health = 100
        self.speed = constants.ENEMY_SPEED * constants.TILE_SIZE
        self._is_alive = True
        self.armor: Armor = NO_ARMOR  # Enemies have no armor by default
        self._last_attack_time = 0.0
        logging.debug(f"Enemy initialized at {position} with type {enemy_type}")

    def update(
        self,
        dt: float,
        player_pos: pygame.Vector2,
        tilemap: "TileMap",
        doors: List["Door"],
    ) -> None:
        """Update enemy behavior based on state machine.

        Args:
            dt: Delta time in seconds.
            player_pos: Player position for detection/chase.
            tilemap: TileMap for collision and line of sight.
            doors: List of doors in the level.
        """
        if not self._is_alive:
            return

        # Update attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt

        # State machine logic
        dist_to_player = self.position.distance_to(player_pos)

        if self.state == constants.ENEMY_STATES["PATROL"]:
            self._update_patrol(dt, tilemap, doors)

            # Transition to chase if player detected
            if dist_to_player < self.detection_radius:
                if self._has_line_of_sight(player_pos, tilemap, doors):
                    self.state = constants.ENEMY_STATES["CHASE"]
                    logging.debug("Enemy detected player, switching to CHASE")

        elif self.state == constants.ENEMY_STATES["CHASE"]:
            self._update_chase(dt, player_pos, tilemap, doors)

            # Transition back to patrol if player out of range
            if dist_to_player > self.detection_radius * 1.5:
                self.state = constants.ENEMY_STATES["PATROL"]
                logging.debug("Player out of range, switching to PATROL")

            # Transition to attack if close enough
            elif dist_to_player < constants.ENEMY_ATTACK_RANGE * constants.TILE_SIZE:
                self.state = constants.ENEMY_STATES["ATTACK"]
                logging.debug("Enemy in range, switching to ATTACK")

        elif self.state == constants.ENEMY_STATES["ATTACK"]:
            self._update_attack(dt, player_pos)

            # After attack, return to chase
            if self.attack_cooldown <= 0:
                self.state = constants.ENEMY_STATES["CHASE"]

    def _update_patrol(
        self, dt: float, tilemap: "TileMap", doors: List["Door"]
    ) -> None:
        """Update patrol behavior.

        Args:
            dt: Delta time in seconds.
            tilemap: TileMap for collision.
            doors: List of doors.
        """
        if not self.patrol_points:
            return

        target = self.patrol_points[self.current_patrol_index]
        direction = target - self.position

        if direction.length() < constants.TILE_SIZE:
            # Reached waypoint, move to next
            self.current_patrol_index = (self.current_patrol_index + 1) % len(
                self.patrol_points
            )
        else:
            # Move towards waypoint
            direction = direction.normalize()
            self._move_in_direction(direction, dt, tilemap, doors)

        # Update rotation to face movement direction
        if direction.length() > 0:
            self.rotation = math.degrees(math.atan2(direction.y, direction.x))

    def _update_chase(
        self,
        dt: float,
        player_pos: pygame.Vector2,
        tilemap: "TileMap",
        doors: List["Door"],
    ) -> None:
        """Update chase behavior.

        Args:
            dt: Delta time in seconds.
            player_pos: Player position to chase.
            tilemap: TileMap for collision.
            doors: List of doors.
        """
        direction = player_pos - self.position
        if direction.length() > 0:
            direction = direction.normalize()
            self._move_in_direction(direction, dt, tilemap, doors)

            # Update rotation to face player
            self.rotation = math.degrees(math.atan2(direction.y, direction.x))

    def _update_attack(self, dt: float, player_pos: pygame.Vector2) -> None:
        """Update attack behavior.

        Args:
            dt: Delta time in seconds.
            player_pos: Player position to attack.
        """
        # Attack is handled externally via get_damage and is_attacking
        # This is just for cooldown management
        pass

    def _move_in_direction(
        self,
        direction: pygame.Vector2,
        dt: float,
        tilemap: "TileMap",
        doors: List["Door"],
    ) -> None:
        """Move enemy in direction with collision detection.

        Args:
            direction: Normalized direction vector.
            dt: Delta time in seconds.
            tilemap: TileMap for collision.
            doors: List of doors.
        """
        distance = self.speed * dt
        new_pos = self.position + direction * distance

        # Simple collision check against walls
        col = int(new_pos.x // constants.TILE_SIZE)
        row = int(new_pos.y // constants.TILE_SIZE)

        # Check if movement is valid
        if not tilemap.is_wall(col, row):
            # Check door collision
            can_pass = True
            for door in doors:
                door_col = int(door.position.x // constants.TILE_SIZE)
                door_row = int(door.position.y // constants.TILE_SIZE)
                if door_col == col and door_row == row and not door.is_open:
                    can_pass = False
                    break

            if can_pass:
                self.position = new_pos

    def _has_line_of_sight(
        self, target_pos: pygame.Vector2, tilemap: "TileMap", doors: List["Door"]
    ) -> bool:
        """Check if there is line of sight to target.

        Args:
            target_pos: Target position to check.
            tilemap: TileMap for wall checking.
            doors: List of doors.

        Returns:
            True if there is line of sight, False otherwise.
        """
        # Simple raycast - check points along the line
        direction = target_pos - self.position
        distance = direction.length()

        if distance == 0:
            return True

        direction = direction.normalize()
        steps = int(distance // (constants.TILE_SIZE / 2))

        for i in range(1, steps + 1):
            check_pos = self.position + direction * (distance * i / steps)
            col = int(check_pos.x // constants.TILE_SIZE)
            row = int(check_pos.y // constants.TILE_SIZE)

            if tilemap.is_wall(col, row):
                return False

            # Check closed doors
            for door in doors:
                door_col = int(door.position.x // constants.TILE_SIZE)
                door_row = int(door.position.y // constants.TILE_SIZE)
                if door_col == col and door_row == row and not door.is_open:
                    return False

        return True

    def take_damage(self, amount: float) -> None:
        """Apply damage to the enemy.

        Args:
            amount: Amount of damage to apply.
        """
        self.health -= amount
        logging.debug(f"Enemy took {amount} damage, HP: {self.health}")

        if self.health <= 0:
            self.health = 0
            self._is_alive = False
            logging.info("Enemy defeated")

    def is_alive(self) -> bool:
        """Check if the enemy is alive.

        Returns:
            True if enemy is alive, False otherwise.
        """
        return self._is_alive

    def get_damage(self) -> float:
        """Get the damage this enemy deals to player.

        Returns:
            Damage amount (10% of player max health).
        """
        return constants.ENEMY_DAMAGE_TO_PLAYER * 100

    def can_attack(self) -> bool:
        """Check if enemy can attack (cooldown ready).

        Returns:
            True if attack is ready, False otherwise.
        """
        return self.attack_cooldown <= 0

    def attack(self) -> None:
        """Trigger attack cooldown."""
        self.attack_cooldown = constants.ENEMY_ATTACK_COOLDOWN
        logging.debug("Enemy attacked player")

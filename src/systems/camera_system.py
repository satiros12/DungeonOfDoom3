"""Camera system for viewport management."""

import logging

import pygame

from src.core import constants


class CameraSystem:
    """Manages camera position and coordinate transformations."""

    def __init__(self, screen_width: int, screen_height: int) -> None:
        """Initialize the camera system.

        Args:
            screen_width: Width of the screen in pixels.
            screen_height: Height of the screen in pixels.
        """
        self.offset = pygame.Vector2(0, 0)
        self.screen_width = screen_width
        self.screen_height = screen_height
        logging.debug("CameraSystem initialized")

    def world_to_screen(self, world_pos: pygame.Vector2) -> pygame.Vector2:
        """Convert world coordinates to screen coordinates.

        Args:
            world_pos: Position in world coordinates.

        Returns:
            Position in screen coordinates.
        """
        return world_pos - self.offset

    def screen_to_world(self, screen_pos: pygame.Vector2) -> pygame.Vector2:
        """Convert screen coordinates to world coordinates.

        Args:
            screen_pos: Position in screen coordinates.

        Returns:
            Position in world coordinates.
        """
        return screen_pos + self.offset

    def follow(self, target_position: pygame.Vector2) -> None:
        """Update camera to follow a target position.

        Args:
            target_position: The position to center the camera on.
        """
        # Center the camera on the target
        self.offset.x = target_position.x - self.screen_width // 2
        self.offset.y = target_position.y - self.screen_height // 2

        # Clamp to map bounds
        max_offset_x = constants.MAP_WIDTH * constants.TILE_SIZE - self.screen_width
        max_offset_y = constants.MAP_HEIGHT * constants.TILE_SIZE - self.screen_height

        self.offset.x = max(0, min(self.offset.x, max_offset_x))
        self.offset.y = max(0, min(self.offset.y, max_offset_y))

        logging.debug(f"Camera following: {target_position}, offset: {self.offset}")

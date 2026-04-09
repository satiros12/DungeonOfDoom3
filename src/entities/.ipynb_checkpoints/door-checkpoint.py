"""Door entity for dungeon exploration."""

import pygame

from src.core import constants


class Door:
    """Represents a door in the dungeon that can be opened or closed."""

    def __init__(
        self,
        position: pygame.Vector2,
        is_locked: bool = False,
    ) -> None:
        """Initialize a door.

        Args:
            position: The world position of the door.
            is_locked: Whether the door is locked (default False).
        """
        self.position = position
        self._is_open = False
        self._is_locked = is_locked

    @property
    def is_open(self) -> bool:
        """Check if the door is open."""
        return self._is_open

    @property
    def is_locked(self) -> bool:
        """Check if the door is locked."""
        return self._is_locked

    def open(self) -> bool:
        """Open the door.

        Returns:
            True if the door was opened, False if it was locked.
        """
        if self._is_locked:
            return False
        self._is_open = True
        return True

    def close(self) -> None:
        """Close the door."""
        self._is_open = False

    def toggle(self) -> bool:
        """Toggle the door state.

        Returns:
            True if the door state changed, False if locked.
        """
        if self._is_locked:
            return False
        self._is_open = not self._is_open
        return True

    def render(self, screen: pygame.Surface, camera_offset: pygame.Vector2) -> None:
        """Render the door.

        Args:
            screen: The pygame surface to render to.
            camera_offset: The camera offset for positioning.
        """
        screen_pos = camera_offset + self.position
        rect = pygame.Rect(
            int(screen_pos.x),
            int(screen_pos.y),
            constants.TILE_SIZE,
            constants.TILE_SIZE,
        )

        # Color based on state
        if self._is_open:
            color = constants.COLOR_DOOR_OPEN
        else:
            color = constants.COLOR_DOOR

        pygame.draw.rect(screen, color, rect)

        # Draw border
        border_color = constants.UI_COLOR_BORDER
        pygame.draw.rect(screen, border_color, rect, 2)

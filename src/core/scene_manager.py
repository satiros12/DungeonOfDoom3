"""Scene Manager for handling game state transitions."""

from typing import List, Optional

import pygame

from src.core.scene import Scene


class SceneManager:
    """Manages a stack of scenes for the game."""

    def __init__(self) -> None:
        """Initialize the scene manager with an empty stack."""
        self._scenes: List[Scene] = []

    def push(self, scene: Scene) -> None:
        """Push a new scene onto the stack.

        Args:
            scene: The scene to push onto the stack.
        """
        self._scenes.append(scene)

    def pop(self) -> Optional[Scene]:
        """Pop the top scene from the stack.

        Returns:
            The popped scene, or None if the stack is empty.
        """
        if self._scenes:
            return self._scenes.pop()
        return None

    def replace(self, scene: Scene) -> None:
        """Replace the top scene with a new scene.

        Args:
            scene: The new scene to replace with.
        """
        if self._scenes:
            self._scenes.pop()
        self._scenes.append(scene)

    def clear(self) -> None:
        """Clear all scenes from the stack."""
        self._scenes.clear()

    def update(self, dt: float) -> None:
        """Update the current scene.

        Args:
            dt: Delta time since last frame in seconds.
        """
        if self._scenes:
            self._scenes[-1].update(dt)

    def render(self, screen: pygame.Surface) -> None:
        """Render the current scene.

        Args:
            screen: The pygame surface to render to.
        """
        if self._scenes:
            self._scenes[-1].render(screen)

    @property
    def current_scene(self) -> Optional[Scene]:
        """Get the current scene.

        Returns:
            The current scene, or None if the stack is empty.
        """
        if self._scenes:
            return self._scenes[-1]
        return None

    @property
    def is_empty(self) -> bool:
        """Check if the scene stack is empty.

        Returns:
            True if the stack is empty, False otherwise.
        """
        return len(self._scenes) == 0

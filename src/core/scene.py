"""Abstract Scene class for game state management."""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from src.core.game import Game


class Scene(ABC):
    """Abstract base class for all game scenes."""

    def __init__(self, game: "Game") -> None:
        """Initialize the scene with a reference to the game.

        Args:
            game: The main game instance.
        """
        self.game = game

    @abstractmethod
    def update(self, dt: float) -> None:
        """Update the scene logic.

        Args:
            dt: Delta time since last frame in seconds.
        """
        pass

    @abstractmethod
    def render(self, screen: pygame.Surface) -> None:
        """Render the scene to the screen.

        Args:
            screen: The pygame surface to render to.
        """
        pass

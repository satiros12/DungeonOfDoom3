"""Main Game class for Escape the Dungeon of Doom."""

import logging
from typing import Optional

import pygame

from src.core.constants import SCREEN_HEIGHT, SCREEN_WIDTH, SCREEN_TITLE, FPS
from src.core.scene import Scene
from src.core.scene_manager import SceneManager


class Game:
    """Main game class that handles the game loop and scene management."""

    def __init__(self) -> None:
        """Initialize the game with pygame, window, and clock."""
        logging.info("Initializing game...")

        pygame.init()
        self._screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(SCREEN_TITLE)

        self._clock = pygame.time.Clock()
        self._running = False

        self._scene_manager = SceneManager()
        self._current_scene: Optional[Scene] = None
        self._running = True

        logging.info(f"Game initialized: {SCREEN_WIDTH}x{SCREEN_HEIGHT} at {FPS} FPS")

    @property
    def running(self) -> bool:
        """Check if the game is running."""
        return self._running

    @running.setter
    def running(self, value: bool) -> None:
        """Set the game running state."""
        self._running = value

    def change_scene(self, scene: Scene) -> None:
        """Change the current scene.

        Args:
            scene: The new scene to switch to.
        """
        self._scene_manager.clear()
        self._scene_manager.push(scene)
        self._current_scene = scene
        logging.info(f"Scene changed to {scene.__class__.__name__}")

    def update(self, dt: float) -> None:
        """Update the game logic.

        Args:
            dt: Delta time since last frame in seconds.
        """
        self._scene_manager.update(dt)

    def render(self, screen: pygame.Surface) -> None:
        """Render the game to the screen.

        Args:
            screen: The pygame surface to render to.
        """
        screen.fill((0, 0, 0))
        self._scene_manager.render(screen)
        pygame.display.flip()

    def run(self) -> None:
        """Run the main game loop."""
        logging.info("Starting game loop...")
        self._running = True

        while self._running:
            dt = self._clock.tick(FPS) / 1000.0  # Delta time in seconds

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                    logging.info("Quit event received")

            self.update(dt)
            self.render(self._screen)

        pygame.quit()
        logging.info("Game loop ended")

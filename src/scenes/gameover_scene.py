"""Game Over Scene displayed when the player dies."""

import logging

import pygame

from src.core import constants
from src.core.scene import Scene
from src.core.game import Game


class GameOverScene(Scene):
    """Game over screen when player health reaches zero."""

    def __init__(self, game: Game) -> None:
        """Initialize the game over scene.

        Args:
            game: The main game instance.
        """
        super().__init__(game)
        self._timer = 0.0
        self._title_font = pygame.font.Font(None, constants.UI_FONT_TITLE)
        self._subtitle_font = pygame.font.Font(None, constants.UI_FONT_MENU)

        logging.info("GameOverScene initialized")

    def update(self, dt: float) -> None:
        """Update the game over scene.

        Args:
            dt: Delta time since last frame in seconds.
        """
        self._timer += dt

        # After display time, restart from level 1
        if self._timer >= constants.GAMEOVER_DISPLAY_TIME:
            from src.scenes.game_scene import GameScene

            self.game.scene_manager.replace(GameScene(self.game, 1))

    def render(self, screen: pygame.Surface) -> None:
        """Render the game over scene.

        Args:
            screen: The pygame surface to render to.
        """
        # Dark red background
        screen.fill((50, 0, 0))

        # Draw "YOU DIED" text in red
        title = self._title_font.render("YOU DIED", True, constants.UI_COLOR_HEALTH)
        title_rect = title.get_rect(
            center=(constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT // 3)
        )
        screen.blit(title, title_rect)

        # Draw subtitle
        subtitle = self._subtitle_font.render(
            "Restarting...", True, constants.UI_COLOR_TEXT_SECONDARY
        )
        subtitle_rect = subtitle.get_rect(
            center=(constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT // 2)
        )
        screen.blit(subtitle, subtitle_rect)

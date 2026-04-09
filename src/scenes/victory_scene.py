"""Victory Scene displayed when the player completes all levels."""

import logging

import pygame

from src.core import constants
from src.core.scene import Scene
from src.core.game import Game


class VictoryScene(Scene):
    """Victory screen when player completes all levels."""

    def __init__(self, game: Game) -> None:
        """Initialize the victory scene.

        Args:
            game: The main game instance.
        """
        super().__init__(game)
        self._timer = 0.0
        self._title_font = pygame.font.Font(None, constants.UI_FONT_TITLE)
        self._subtitle_font = pygame.font.Font(None, constants.UI_FONT_MENU)

        logging.info("VictoryScene initialized")

    def update(self, dt: float) -> None:
        """Update the victory scene.

        Args:
            dt: Delta time since last frame in seconds.
        """
        self._timer += dt

        # After display time, return to menu
        if self._timer >= constants.VICTORY_DISPLAY_TIME:
            from src.scenes.menu_scene import MenuScene

            self._game.scene_manager.replace(MenuScene(self._game))

    def render(self, screen: pygame.Surface) -> None:
        """Render the victory scene.

        Args:
            screen: The pygame surface to render to.
        """
        screen.fill((0, 0, 0))

        # Draw "VICTORY" text
        title = self._title_font.render(
            "VICTORY!", True, constants.UI_COLOR_TEXT_PRIMARY
        )
        title_rect = title.get_rect(
            center=(constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT // 3)
        )
        screen.blit(title, title_rect)

        # Draw subtitle
        subtitle = self._subtitle_font.render(
            "You escaped the dungeon!", True, constants.UI_COLOR_TEXT_SECONDARY
        )
        subtitle_rect = subtitle.get_rect(
            center=(constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT // 2)
        )
        screen.blit(subtitle, subtitle_rect)

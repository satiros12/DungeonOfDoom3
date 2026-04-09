"""Pause Scene for the game menu."""

import logging

import pygame

from src.core import constants
from src.core.scene import Scene
from src.core.game import Game
from src.scenes.game_scene import GameScene


class PauseScene(Scene):
    """Pause menu scene with resume, options, and exit options."""

    def __init__(self, game: Game, game_scene: GameScene) -> None:
        """Initialize the pause scene.

        Args:
            game: The main game instance.
            game_scene: The game scene to pause.
        """
        super().__init__(game)
        self._game_scene = game_scene
        self._selected_index = 0
        self._options = ["Resume", "Options", "Exit to Menu"]
        self._font = pygame.font.Font(None, constants.UI_FONT_MENU)
        self._title_font = pygame.font.Font(None, constants.UI_FONT_TITLE)

        logging.info("PauseScene initialized")

    def update(self, dt: float) -> None:
        """Update the pause menu.

        Args:
            dt: Delta time since last frame in seconds.
        """
        # Don't update game scene while paused

        # Handle input for menu navigation
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self._selected_index = (self._selected_index - 1) % len(
                        self._options
                    )
                elif event.key == pygame.K_DOWN:
                    self._selected_index = (self._selected_index + 1) % len(
                        self._options
                    )
                elif event.key == pygame.K_RETURN:
                    self._handle_selection()
                elif event.key == pygame.K_ESCAPE:
                    # Resume on ESC
                    self._game.scene_manager.pop()

    def _handle_selection(self) -> None:
        """Handle menu selection."""
        if self._selected_index == 0:  # Resume
            logging.info("Resume selected")
            self._game.scene_manager.pop()
        elif self._selected_index == 1:  # Options
            logging.info("Options selected")
            from src.scenes.options_scene import OptionsScene

            options_scene = OptionsScene(self.game, return_to_menu=False)
            self._game.scene_manager.push(options_scene)
        elif self._selected_index == 2:  # Exit to Menu
            logging.info("Exit to Menu selected")
            from src.scenes.menu_scene import MenuScene

            self._game.scene_manager.clear()
            self._game.scene_manager.push(MenuScene(self._game))

    def render(self, screen: pygame.Surface) -> None:
        """Render the pause menu.

        Args:
            screen: The pygame surface to render to.
        """
        # First render the game scene darkened
        if self._game_scene:
            # Create dark overlay
            overlay = pygame.Surface(
                (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT),
                pygame.SRCALPHA,
            )
            overlay.fill((0, 0, 0, 128))  # Semi-transparent black
            screen.blit(overlay, (0, 0))

        # Render menu title
        title = self._title_font.render("PAUSED", True, constants.UI_COLOR_TEXT_PRIMARY)
        title_rect = title.get_rect(
            center=(constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT // 3)
        )
        screen.blit(title, title_rect)

        # Render menu options
        for i, option in enumerate(self._options):
            if i == self._selected_index:
                color = constants.UI_COLOR_HIGHLIGHT
            else:
                color = constants.UI_COLOR_TEXT_PRIMARY

            text = self._font.render(option, True, color)
            text_rect = text.get_rect(
                center=(
                    constants.SCREEN_WIDTH // 2,
                    constants.SCREEN_HEIGHT // 2 + i * 50,
                )
            )
            screen.blit(text, text_rect)

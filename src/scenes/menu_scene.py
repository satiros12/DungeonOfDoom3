"""Menu Scene for Escape the Dungeon of Doom."""

import logging
from typing import List

import pygame

from src.core import constants
from src.core.scene import Scene
from src.core.game import Game
from src.scenes.game_scene import GameScene


class MenuScene(Scene):
    """Main menu scene with navigation options."""

    def __init__(self, game: Game) -> None:
        """Initialize the menu scene.

        Args:
            game: The main game instance.
        """
        super().__init__(game)
        self._selected_index = 0
        self._options: List[str] = ["START GAME", "OPTIONS", "EXIT"]

        # Initialize fonts
        pygame.font.init()
        self._font_title = pygame.font.Font(None, constants.UI_FONT_TITLE)
        self._font_menu = pygame.font.Font(None, constants.UI_FONT_MENU)

        logging.info("Menu scene initialized")

    def update(self, dt: float) -> None:
        """Update menu input handling.

        Args:
            dt: Delta time since last frame in seconds.
        """
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self._handle_keydown(event.key)

    def _handle_keydown(self, key: int) -> None:
        """Handle key press events.

        Args:
            key: The pygame key code.
        """
        if key == pygame.K_UP:
            self._selected_index = (self._selected_index - 1) % len(self._options)
            logging.debug(f"Menu selection: {self._selected_index}")
        elif key == pygame.K_DOWN:
            self._selected_index = (self._selected_index + 1) % len(self._options)
            logging.debug(f"Menu selection: {self._selected_index}")
        elif key == pygame.K_RETURN:
            self._select_option()

    def _select_option(self) -> None:
        """Handle the selected menu option."""
        option = self._options[self._selected_index]
        logging.info(f"Selected menu option: {option}")

        if option == "START GAME":
            logging.info("Starting game...")
            game_scene = GameScene(self.game, level_number=1)
            self.game.change_scene(game_scene)
        elif option == "OPTIONS":
            logging.info("Opening options...")
            from src.scenes.options_scene import OptionsScene

            options_scene = OptionsScene(self.game, return_to_menu=True)
            self._game.scene_manager.push(options_scene)
        elif option == "EXIT":
            logging.info("Exiting game...")
            self.game.running = False

    def render(self, screen: pygame.Surface) -> None:
        """Render the menu scene.

        Args:
            screen: The pygame surface to render to.
        """
        screen.fill(constants.MENU_BG_COLOR)

        # Render title
        title_text = "ESCAPE THE DUNGEON"
        title_surface = self._font_title.render(
            title_text, True, constants.UI_COLOR_TEXT_PRIMARY
        )
        title_rect = title_surface.get_rect(
            center=(constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT // 2 - 100)
        )
        screen.blit(title_surface, title_rect)

        subtitle_text = "OF DOOM"
        subtitle_surface = self._font_title.render(
            subtitle_text, True, constants.UI_COLOR_TEXT_PRIMARY
        )
        subtitle_rect = subtitle_surface.get_rect(
            center=(constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT // 2 - 50)
        )
        screen.blit(subtitle_surface, subtitle_rect)

        # Render menu options
        for i, option in enumerate(self._options):
            color = (
                constants.UI_COLOR_HIGHLIGHT
                if i == self._selected_index
                else constants.UI_COLOR_TEXT_PRIMARY
            )

            # Scale effect on hover
            scale = 1.05 if i == self._selected_index else 1.0
            font = self._font_menu
            if scale > 1.0:
                # Create a larger font for selection
                font = pygame.font.Font(None, int(constants.UI_FONT_MENU * scale))

            option_surface = font.render(option, True, color)
            option_rect = option_surface.get_rect(
                center=(
                    constants.SCREEN_WIDTH // 2,
                    constants.SCREEN_HEIGHT // 2 + i * 50 + 20,
                )
            )
            screen.blit(option_surface, option_rect)

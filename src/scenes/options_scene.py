"""Options Scene for Escape the Dungeon of Doom."""

import json
import logging
from typing import List

import pygame

from src.core import constants
from src.core.scene import Scene
from src.core.game import Game


class OptionsScene(Scene):
    """Options menu scene for configuring game settings."""

    def __init__(self, game: Game, return_to_menu: bool = True) -> None:
        """Initialize the options scene.

        Args:
            game: The main game instance.
            return_to_menu: If True, back goes to menu; if False, goes to pause.
        """
        super().__init__(game)
        self._selected_index = 0
        self._return_to_menu = return_to_menu
        self._options = self._load_options_from_file()

        # Menu options: Fullscreen, Turn Speed, Music Volume, SFX Volume
        self._menu_options: List[str] = [
            "FULLSCREEN: ON"
            if self._options.get("fullscreen", False)
            else "FULLSCREEN: OFF",
            f"TURN SPEED: {self._options.get('turn_speed', 90)}",
            f"MUSIC: {int(self._options.get('music_volume', 0.7) * 100)}%",
            f"SFX: {int(self._options.get('sfx_volume', 0.5) * 100)}%",
            "BACK",
        ]

        # Initialize fonts
        pygame.font.init()
        self._font_title = pygame.font.Font(None, constants.UI_FONT_TITLE)
        self._font_menu = pygame.font.Font(None, constants.UI_FONT_MENU)

        logging.info("Options scene initialized")

    def _load_options_from_file(self) -> dict:
        """Load options from the config file.

        Returns:
            Dictionary of options.
        """
        try:
            with open("config/options.json", "r") as f:
                return json.load(f)
        except Exception as e:
            logging.warning(f"Could not load options: {e}")
            return {
                "fullscreen": False,
                "turn_speed": 90,
                "music_volume": 0.7,
                "sfx_volume": 0.5,
            }

    def update(self, dt: float) -> None:
        """Update options input handling.

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
            self._selected_index = (self._selected_index - 1) % len(self._menu_options)
            logging.debug(f"Options selection: {self._selected_index}")
        elif key == pygame.K_DOWN:
            self._selected_index = (self._selected_index + 1) % len(self._menu_options)
            logging.debug(f"Options selection: {self._selected_index}")
        elif key == pygame.K_LEFT:
            self._adjust_option(-1)
        elif key == pygame.K_RIGHT:
            self._adjust_option(1)
        elif key == pygame.K_RETURN:
            self._select_option()

    def _adjust_option(self, direction: int) -> None:
        """Adjust the currently selected option.

        Args:
            direction: -1 for left, 1 for right.
        """
        option = self._menu_options[self._selected_index]

        if "FULLSCREEN" in option:
            current = self._options.get("fullscreen", False)
            self._options["fullscreen"] = not current
            self._menu_options[0] = (
                "FULLSCREEN: ON" if self._options["fullscreen"] else "FULLSCREEN: OFF"
            )
            self._apply_fullscreen()
        elif "TURN SPEED" in option:
            current = self._options.get("turn_speed", 90)
            new_speed = max(
                constants.TURN_SPEED_MIN,
                min(
                    constants.TURN_SPEED_MAX,
                    current + direction * constants.TURN_SPEED_STEP,
                ),
            )
            self._options["turn_speed"] = new_speed
            self._menu_options[1] = f"TURN SPEED: {new_speed}"
        elif "MUSIC" in option:
            current = self._options.get("music_volume", 0.7)
            new_vol = max(0.0, min(1.0, current + direction * 0.1))
            self._options["music_volume"] = round(new_vol, 1)
            self._menu_options[2] = (
                f"MUSIC: {int(self._options['music_volume'] * 100)}%"
            )
        elif "SFX" in option:
            current = self._options.get("sfx_volume", 0.5)
            new_vol = max(0.0, min(1.0, current + direction * 0.1))
            self._options["sfx_volume"] = round(new_vol, 1)
            self._menu_options[3] = f"SFX: {int(self._options['sfx_volume'] * 100)}%"

        self._save_options()

    def _apply_fullscreen(self) -> None:
        """Apply fullscreen setting to the display."""
        try:
            screen = pygame.display.get_surface()
            if self._options.get("fullscreen", False):
                pygame.display.set_mode(
                    (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT),
                    pygame.FULLSCREEN,
                )
            else:
                pygame.display.set_mode(
                    (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
                )
            logging.info(f"Fullscreen: {self._options['fullscreen']}")
        except Exception as e:
            logging.warning(f"Could not apply fullscreen: {e}")

    def _save_options(self) -> None:
        """Save options to the config file."""
        try:
            with open("config/options.json", "w") as f:
                json.dump(self._options, f, indent=4)
            logging.debug("Options saved")
        except Exception as e:
            logging.warning(f"Could not save options: {e}")

    def _select_option(self) -> None:
        """Handle the selected menu option."""
        option = self._menu_options[self._selected_index]
        logging.info(f"Selected option: {option}")

        if option == "BACK":
            if self._return_to_menu:
                from src.scenes.menu_scene import MenuScene

                self.game.change_scene(MenuScene(self.game))
            else:
                self._game.scene_manager.pop()

    def render(self, screen: pygame.Surface) -> None:
        """Render the options scene.

        Args:
            screen: The pygame surface to render to.
        """
        screen.fill(constants.MENU_BG_COLOR)

        # Render title
        title_surface = self._font_title.render(
            "OPTIONS", True, constants.UI_COLOR_TEXT_PRIMARY
        )
        title_rect = title_surface.get_rect(
            center=(constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT // 2 - 150)
        )
        screen.blit(title_surface, title_rect)

        # Render instructions
        instructions = [
            "Use UP/DOWN to navigate",
            "Use LEFT/RIGHT to adjust",
            "Press ENTER to select",
        ]
        font_small = pygame.font.Font(None, 24)
        for i, instr in enumerate(instructions):
            instr_surface = font_small.render(
                instr, True, constants.UI_COLOR_TEXT_SECONDARY
            )
            instr_rect = instr_surface.get_rect(
                center=(
                    constants.SCREEN_WIDTH // 2,
                    constants.SCREEN_HEIGHT // 2 - 80 + i * 25,
                )
            )
            screen.blit(instr_surface, instr_rect)

        # Render menu options
        for i, option in enumerate(self._menu_options):
            color = (
                constants.UI_COLOR_HIGHLIGHT
                if i == self._selected_index
                else constants.UI_COLOR_TEXT_PRIMARY
            )

            # Scale effect on hover
            scale = 1.05 if i == self._selected_index else 1.0
            font = self._font_menu
            if scale > 1.0:
                font = pygame.font.Font(None, int(constants.UI_FONT_MENU * scale))

            option_surface = font.render(option, True, color)
            option_rect = option_surface.get_rect(
                center=(
                    constants.SCREEN_WIDTH // 2,
                    constants.SCREEN_HEIGHT // 2 + i * 50,
                )
            )
            screen.blit(option_surface, option_rect)

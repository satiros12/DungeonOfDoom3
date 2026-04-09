"""Level Transition Scene for transitioning between levels."""

import logging
import math

import pygame

from src.core import constants
from src.core.scene import Scene
from src.core.game import Game


class LevelTransitionScene(Scene):
    """Scene that displays a transition when changing levels."""

    def __init__(self, game: Game, level_name: str, target_level: int) -> None:
        """Initialize the level transition scene.

        Args:
            game: The main game instance.
            level_name: The name of the level to display.
            target_level: The level number to transition to.
        """
        super().__init__(game)
        self._level_name = level_name
        self._target_level = target_level
        self._timer = 0.0
        self._phase = "black"  # "black" -> "name" -> "done"

        logging.info(f"LevelTransitionScene: {level_name} (level {target_level})")

    def update(self, dt: float) -> None:
        """Update the transition.

        Args:
            dt: Delta time since last frame in seconds.
        """
        self._timer += dt

        if self._phase == "black":
            if self._timer >= constants.TRANSITION_BLACK_TIME:
                self._phase = "name"
                self._timer = 0.0

        elif self._phase == "name":
            if self._timer >= constants.TRANSITION_NAME_TIME:
                self._phase = "done"

        elif self._phase == "done":
            # Transition to the next level game scene
            from src.scenes.game_scene import GameScene

            self.game.scene_manager.replace(GameScene(self.game, self._target_level))

    def render(self, screen: pygame.Surface) -> None:
        """Render the transition.

        Args:
            screen: The pygame surface to render to.
        """
        screen.fill((0, 0, 0))

        if self._phase == "black":
            # Just black screen
            pass

        elif self._phase == "name":
            # Draw the level name
            self._render_level_name(screen)

        elif self._phase == "done":
            # Fade to black before transitioning
            fade_alpha = min(255, int(255 * (self._timer / 0.5)))
            fade_surface = pygame.Surface((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
            fade_surface.fill((0, 0, 0))
            fade_surface.set_alpha(fade_alpha)
            screen.blit(fade_surface, (0, 0))

    def _render_level_name(self, screen: pygame.Surface) -> None:
        """Render the level name with a retro effect.

        Args:
            screen: The pygame surface to render to.
        """
        font = pygame.font.Font(None, constants.UI_FONT_TITLE)
        text = font.render(self._level_name, True, constants.UI_COLOR_TEXT_PRIMARY)

        # Center the text
        text_rect = text.get_rect(
            center=(constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT // 2)
        )

        # Draw text shadow
        shadow = font.render(self._level_name, True, (0, 0, 0))
        shadow_rect = text_rect.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2
        screen.blit(shadow, shadow_rect)

        # Draw main text
        screen.blit(text, text_rect)

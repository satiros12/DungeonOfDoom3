"""Input system for processing keyboard input."""

import logging
from typing import Dict

import pygame

from src.core import constants


class InputSystem:
    """Processes keyboard input and maps to game actions."""

    def __init__(self) -> None:
        """Initialize the input system."""
        self._keys_pressed: Dict[str, bool] = {}
        self._keys_just_pressed: Dict[str, bool] = {}
        self._keys_just_released: Dict[str, bool] = {}
        self._previous_keys: Dict[str, bool] = {}
        logging.debug("InputSystem initialized")

    def update(self) -> None:
        """Update input state for the current frame."""
        # Get current key states using pygame.key.get_pressed()
        # This doesn't consume events from the queue
        keys = pygame.key.get_pressed()

        key_mapping = {
            pygame.K_w: "forward",
            pygame.K_s: "backward",
            pygame.K_a: "left",
            pygame.K_d: "right",
            pygame.K_LEFT: "rotate_left",
            pygame.K_RIGHT: "rotate_right",
            pygame.K_SPACE: "attack",
            pygame.K_e: "interact",
            pygame.K_i: "drop_weapon",
            pygame.K_j: "drop_armor",
            pygame.K_TAB: "toggle_health",
            pygame.K_ESCAPE: "pause",
            pygame.K_F3: "debug",
        }

        # Clear just pressed/released
        self._keys_just_pressed.clear()
        self._keys_just_released.clear()

        # Update key states
        for pygame_key, action_name in key_mapping.items():
            is_pressed = bool(keys[pygame_key])
            was_pressed = self._previous_keys.get(action_name, False)

            # Update pressed state
            self._keys_pressed[action_name] = is_pressed

            # Detect just pressed (was not pressed, now is)
            if is_pressed and not was_pressed:
                self._keys_just_pressed[action_name] = True

            # Detect just released (was pressed, now is not)
            if not is_pressed and was_pressed:
                self._keys_just_released[action_name] = True

            # Update previous state
            self._previous_keys[action_name] = is_pressed

    def _get_key_name(self, key: int) -> str:
        """Convert pygame key code to action name.

        Args:
            key: Pygame key code.

        Returns:
            Action name string.
        """
        key_mapping = {
            pygame.K_w: "forward",
            pygame.K_s: "backward",
            pygame.K_a: "left",
            pygame.K_d: "right",
            pygame.K_LEFT: "rotate_left",
            pygame.K_RIGHT: "rotate_right",
            pygame.K_SPACE: "attack",
            pygame.K_e: "interact",
            pygame.K_i: "drop_weapon",
            pygame.K_j: "drop_armor",
            pygame.K_TAB: "toggle_health",
            pygame.K_ESCAPE: "pause",
            pygame.K_F3: "debug",
        }
        return key_mapping.get(key, "")

    def get_actions(self) -> Dict[str, bool]:
        """Get current action states.

        Returns:
            Dictionary of action names to their current state.
        """
        return {
            "forward": self._keys_pressed.get("forward", False),
            "backward": self._keys_pressed.get("backward", False),
            "left": self._keys_pressed.get("left", False),
            "right": self._keys_pressed.get("right", False),
            "rotate_left": self._keys_pressed.get("rotate_left", False),
            "rotate_right": self._keys_pressed.get("rotate_right", False),
            "attack": self._keys_just_pressed.get("attack", False),
            "interact": self._keys_just_pressed.get("interact", False),
            "drop_weapon": self._keys_just_pressed.get("drop_weapon", False),
            "drop_armor": self._keys_just_pressed.get("drop_armor", False),
            "toggle_health": self._keys_just_pressed.get("toggle_health", False),
            "pause": self._keys_just_pressed.get("pause", False),
            "debug": self._keys_just_pressed.get("debug", False),
        }

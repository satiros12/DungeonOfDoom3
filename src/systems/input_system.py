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
        logging.debug("InputSystem initialized")

    def update(self) -> None:
        """Update input state for the current frame."""
        # Reset frame-specific states
        self._keys_just_pressed.clear()
        self._keys_just_released.clear()

        # Process all keyboard events
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                key_name = self._get_key_name(event.key)
                if key_name and not self._keys_pressed.get(key_name, False):
                    self._keys_just_pressed[key_name] = True
                self._keys_pressed[key_name] = True
            elif event.type == pygame.KEYUP:
                key_name = self._get_key_name(event.key)
                if key_name:
                    self._keys_pressed[key_name] = False
                    self._keys_just_released[key_name] = True

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

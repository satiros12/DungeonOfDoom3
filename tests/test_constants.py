"""Tests for constants module."""

import pytest
from src.core import constants


class TestConstants:
    """Test suite for constants module."""

    def test_screen_dimensions(self):
        """Test that screen dimensions are valid."""
        assert constants.SCREEN_WIDTH == 800
        assert constants.SCREEN_HEIGHT == 600
        assert constants.SCREEN_WIDTH > 0
        assert constants.SCREEN_HEIGHT > 0

    def test_fps(self):
        """Test that FPS is valid."""
        assert constants.FPS == 60
        assert constants.FPS > 0

    def test_tile_size(self):
        """Test that tile size is valid."""
        assert constants.TILE_SIZE == 16
        assert constants.TILE_SIZE > 0

    def test_map_dimensions(self):
        """Test that map dimensions are valid."""
        assert constants.MAP_WIDTH == 48
        assert constants.MAP_HEIGHT == 48
        assert constants.MAP_WIDTH > 0
        assert constants.MAP_HEIGHT > 0

    def test_turn_speed_bounds(self):
        """Test that turn speed has valid bounds."""
        assert constants.TURN_SPEED_MIN == 60
        assert constants.TURN_SPEED_MAX == 120
        assert constants.TURN_SPEED_DEFAULT == 90
        assert constants.TURN_SPEED_MIN < constants.TURN_SPEED_MAX
        assert (
            constants.TURN_SPEED_MIN
            <= constants.TURN_SPEED_DEFAULT
            <= constants.TURN_SPEED_MAX
        )

    def test_weapons_config(self):
        """Test that weapons are properly configured."""
        assert "fists" in constants.WEAPONS
        assert "sword" in constants.WEAPONS
        assert "axe" in constants.WEAPONS
        assert "hammer" in constants.WEAPONS

        # Check damage percentages
        assert constants.WEAPONS["fists"]["damage_percent"] == 10
        assert constants.WEAPONS["sword"]["damage_percent"] == 25
        assert constants.WEAPONS["axe"]["damage_percent"] == 40
        assert constants.WEAPONS["hammer"]["damage_percent"] == 70

        # Check speed multipliers
        assert constants.WEAPONS["fists"]["speed_multiplier"] == 1.0
        assert constants.WEAPONS["sword"]["speed_multiplier"] == 0.9

    def test_armors_config(self):
        """Test that armors are properly configured."""
        assert "none" in constants.ARMORS
        assert "light" in constants.ARMORS
        assert "medium" in constants.ARMORS
        assert "heavy" in constants.ARMORS

        # Check damage reductions
        assert constants.ARMORS["none"]["damage_reduction"] == 1.0
        assert constants.ARMORS["light"]["damage_reduction"] == 0.75
        assert constants.ARMORS["medium"]["damage_reduction"] == 0.5
        assert constants.ARMORS["heavy"]["damage_reduction"] == 0.25

        # Check speed multipliers
        assert constants.ARMORS["none"]["speed_multiplier"] == 1.0
        assert constants.ARMORS["light"]["speed_multiplier"] == 0.8

    def test_combat_constants(self):
        """Test combat constants are valid."""
        assert constants.BACKSTAB_DAMAGE_BONUS == 0.25
        assert constants.DODGE_WINDOW == 0.3
        assert 0 < constants.BACKSTAB_DAMAGE_BONUS < 1

    def test_enemy_constants(self):
        """Test enemy constants are valid."""
        assert constants.ENEMY_SPEED > 0
        assert 0 < constants.ENEMY_FOV <= 360
        assert constants.ENEMY_ATTACK_RANGE > 0
        assert constants.ENEMY_ATTACK_COOLDOWN > 0

    def test_level_constants(self):
        """Test level configuration."""
        assert len(constants.LEVELS) == 5
        assert len(constants.LEVEL_NAMES) == 5
        assert 1 in constants.LEVELS
        assert 5 in constants.LEVELS

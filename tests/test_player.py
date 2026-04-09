"""Tests for Player entity."""

import pytest
import pygame

from src.entities.player import Player
from src.entities.weapon import FISTS, SWORD, AXE, HAMMER
from src.entities.armor import NO_ARMOR, LIGHT_ARMOR, MEDIUM_ARMOR, HEAVY_ARMOR


class TestPlayer:
    """Test suite for Player class."""

    @pytest.fixture
    def player(self):
        """Create a player instance for testing."""
        return Player(position=pygame.Vector2(100, 100))

    def test_player_initialization(self, player):
        """Test that player is properly initialized."""
        assert player.position == pygame.Vector2(100, 100)
        assert player.rotation == 0.0
        assert player.health == 100
        assert player._max_health == 100
        assert player.weapon == FISTS
        assert player.armor == NO_ARMOR

    def test_player_move(self, player):
        """Test player movement."""
        initial_pos = player.position.copy()
        direction = pygame.Vector2(1, 0)
        dt = 0.5

        player.move(direction, dt)

        # Player should have moved
        assert player.position != initial_pos

    def test_player_rotate(self, player):
        """Test player rotation."""
        initial_rotation = player.rotation
        player.rotate(90, 0.5)

        assert player.rotation == 45.0

    def test_player_rotate_wraps(self, player):
        """Test that rotation wraps around at 360."""
        player.rotation = 350
        player.rotate(20, 1.0)

        assert player.rotation < 360

    def test_equip_weapon(self, player):
        """Test equipping a weapon."""
        player.equip_weapon(SWORD)

        assert player.weapon == SWORD

    def test_equip_armor(self, player):
        """Test equipping armor."""
        player.equip_armor(LIGHT_ARMOR)

        assert player.armor == LIGHT_ARMOR

    def test_drop_weapon(self, player):
        """Test dropping weapon returns to fists."""
        player.equip_weapon(SWORD)
        player.drop_weapon()

        assert player.weapon == FISTS

    def test_drop_armor(self, player):
        """Test dropping armor returns to none."""
        player.equip_armor(HEAVY_ARMOR)
        player.drop_armor()

        assert player.armor == NO_ARMOR

    def test_take_damage(self, player):
        """Test taking damage."""
        initial_health = player.health
        player.take_damage(20)

        assert player.health < initial_health

    def test_take_damage_with_armor(self, player):
        """Test taking damage with armor reduction."""
        player.equip_armor(MEDIUM_ARMOR)
        health_with_armor = player.health

        player.take_damage(20)

        # With 0.5 reduction, should take 10 damage
        assert player.health == health_with_armor - 10

    def test_take_damage_no_negative(self, player):
        """Test that health doesn't go below zero."""
        player.take_damage(200)

        assert player.health == 0

    def test_is_alive(self, player):
        """Test is_alive method."""
        assert player.is_alive() is True

        player.health = 0
        assert player.is_alive() is False

    def test_get_cell_position(self, player):
        """Test getting cell position."""
        player.position = pygame.Vector2(100, 100)

        col, row = player.get_cell_position()

        assert col == 6  # 100 // 16 = 6
        assert row == 6

    def test_health_display(self, player):
        """Test that health is properly displayed."""
        assert player.health == 100

        player.health = 50
        assert player.health == 50

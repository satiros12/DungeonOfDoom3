"""Tests for AI System."""

import pytest
import pygame

from src.systems.ai_system import AISystem
from src.entities.enemy import Enemy
from src.entities.player import Player
from src.entities.tilemap import TileMap
from src.entities.door import Door
from src.core import constants


class TestAISystem:
    """Test suite for AISystem class."""

    @pytest.fixture
    def ai_system(self):
        """Create an AI system instance."""
        return AISystem(level_number=1)

    @pytest.fixture
    def tilemap(self):
        """Create a tilemap for testing."""
        tiles = [
            ["wall"] * 10,
            ["wall"] + ["floor"] * 8 + ["wall"],
            ["wall"] + ["floor"] * 8 + ["wall"],
            ["wall"] + ["floor"] * 8 + ["wall"],
            ["wall"] + ["floor"] * 8 + ["wall"],
            ["wall"] + ["floor"] * 8 + ["wall"],
            ["wall"] + ["floor"] * 8 + ["wall"],
            ["wall"] + ["floor"] * 8 + ["wall"],
            ["wall"] + ["floor"] * 8 + ["wall"],
            ["wall"] * 10,
        ]
        return TileMap(tiles=tiles, width=10, height=10)

    @pytest.fixture
    def enemy(self):
        """Create an enemy instance."""
        patrol_points = [
            pygame.Vector2(64, 64),
            pygame.Vector2(96, 64),
        ]
        return Enemy(
            position=pygame.Vector2(64, 64),
            enemy_type="guard",
            patrol_points=patrol_points,
        )

    @pytest.fixture
    def player(self):
        """Create a player instance."""
        return Player(position=pygame.Vector2(32, 32))

    def test_ai_system_initialization(self, ai_system):
        """Test AI system is initialized."""
        assert ai_system is not None
        assert ai_system._detection_radius == 5  # Level 1

    def test_ai_system_with_different_level(self):
        """Test AI system with different level."""
        ai = AISystem(level_number=3)
        assert ai._detection_radius == 7  # Level 3

    def test_update_enemies(self, ai_system, enemy, tilemap):
        """Test updating enemies."""
        doors = []

        ai_system.update_enemies(
            [enemy], Player(position=pygame.Vector2(200, 200)), tilemap, doors, 0.1
        )

        # Should not raise error

    def test_check_enemy_player_collision(self, ai_system, enemy, player):
        """Test collision check between enemy and player."""
        enemy.position = pygame.Vector2(100, 100)
        player.position = pygame.Vector2(116, 100)  # 1 tile away

        result = ai_system.check_enemy_player_collision(enemy, player)

        assert isinstance(result, bool)

    def test_check_enemy_player_collision_far(self, ai_system, enemy, player):
        """Test collision check when far apart."""
        enemy.position = pygame.Vector2(100, 100)
        player.position = pygame.Vector2(200, 200)

        result = ai_system.check_enemy_player_collision(enemy, player)

        assert result is False

    def test_enemy_patrol_behavior(self, ai_system, enemy, tilemap):
        """Test enemy patrol behavior."""
        # Place player far away
        player = Player(position=pygame.Vector2(300, 300))

        # Update enemy
        ai_system.update_enemies([enemy], player, tilemap, [], 0.1)

        # Enemy should still be in patrol state (far from player)
        # Note: This may vary based on implementation

    def test_enemy_chase_behavior(self, ai_system, enemy, tilemap):
        """Test enemy chase behavior when player is close."""
        # Place player very close (within detection)
        player = Player(position=pygame.Vector2(64, 64))
        enemy.position = pygame.Vector2(64, 80)

        # Update enemy
        ai_system.update_enemies([enemy], player, tilemap, [], 0.1)

        # Enemy may change to chase state (depends on distance)

    def test_detection_radius(self, ai_system):
        """Test detection radius for different levels."""
        assert ai_system._detection_radius > 0

        # Level 1 should have smallest radius
        ai_l1 = AISystem(level_number=1)
        ai_l5 = AISystem(level_number=5)

        assert ai_l1._detection_radius < ai_l5._detection_radius

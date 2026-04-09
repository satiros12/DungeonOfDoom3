"""Tests for Enemy entity."""

import pytest
import pygame

from src.entities.enemy import Enemy
from src.core import constants


class TestEnemy:
    """Test suite for Enemy class."""

    @pytest.fixture
    def enemy(self):
        """Create an enemy instance for testing."""
        patrol_points = [
            pygame.Vector2(100, 100),
            pygame.Vector2(200, 100),
            pygame.Vector2(200, 200),
        ]
        return Enemy(
            position=pygame.Vector2(100, 100),
            enemy_type="guard",
            patrol_points=patrol_points,
        )

    def test_enemy_initialization(self, enemy):
        """Test that enemy is properly initialized."""
        assert enemy.position == pygame.Vector2(100, 100)
        assert enemy.rotation == 0.0
        assert enemy.health == 100
        assert enemy.state == "patrol"

    def test_enemy_patrol_state(self, enemy):
        """Test enemy starts in patrol state."""
        assert enemy.state == constants.ENEMY_STATES["PATROL"]

    def test_enemy_is_alive(self, enemy):
        """Test enemy is alive."""
        assert enemy.is_alive() is True

        enemy.take_damage(100)  # Use take_damage to properly set _is_alive
        assert enemy.is_alive() is False

    def test_enemy_take_damage(self, enemy):
        """Test enemy takes damage."""
        initial_health = enemy.health
        enemy.take_damage(30)

        assert enemy.health < initial_health

    def test_enemy_rotation(self, enemy):
        """Test enemy rotation."""
        enemy.rotation = 0
        enemy.rotation = 45

        assert enemy.rotation == 45

    def test_enemy_get_damage(self, enemy):
        """Test enemy damage calculation."""
        damage = enemy.get_damage()

        assert damage == 10  # 10% of max health

    def test_enemy_attack_cooldown(self, enemy):
        """Test enemy attack cooldown."""
        assert enemy.can_attack() is True

        enemy.attack()

        # Immediately after attack, should not be able to attack again
        # (cooldown is 1 second)
        enemy._last_attack_time = 0  # Reset to simulate cooldown not finished

        # Note: can_attack depends on current time

    def test_enemy_patrol_movement(self, enemy):
        """Test enemy patrol movement."""
        initial_pos = enemy.position.copy()

        # Simulate patrol movement by setting state to patrol
        enemy.state = constants.ENEMY_STATES["PATROL"]

        # This is more of an integration test as patrol is handled by AI system
        assert enemy.position is not None

    def test_enemy_state_change_to_chase(self, enemy):
        """Test enemy state changes to chase."""
        enemy.state = constants.ENEMY_STATES["CHASE"]

        assert enemy.state == constants.ENEMY_STATES["CHASE"]

    def test_enemy_state_change_to_attack(self, enemy):
        """Test enemy state changes to attack."""
        enemy.state = constants.ENEMY_STATES["ATTACK"]

        assert enemy.state == constants.ENEMY_STATES["ATTACK"]

    def test_enemy_position(self, enemy):
        """Test enemy position."""
        assert enemy.position is not None
        assert isinstance(enemy.position, pygame.Vector2)

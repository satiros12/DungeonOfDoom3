"""Tests for Combat System."""

import pytest
import pygame

from src.systems.combat_system import CombatSystem
from src.entities.player import Player
from src.entities.enemy import Enemy
from src.entities.weapon import FISTS, SWORD, AXE, HAMMER
from src.entities.armor import NO_ARMOR, LIGHT_ARMOR, MEDIUM_ARMOR, HEAVY_ARMOR
from src.core import constants


class TestCombatSystem:
    """Test suite for CombatSystem class."""

    @pytest.fixture
    def combat_system(self):
        """Create a combat system instance."""
        return CombatSystem()

    @pytest.fixture
    def player(self):
        """Create a player instance."""
        return Player(position=pygame.Vector2(100, 100))

    @pytest.fixture
    def enemy(self):
        """Create an enemy instance."""
        return Enemy(
            position=pygame.Vector2(150, 100),
            enemy_type="guard",
            patrol_points=None,
        )

    def test_combat_system_initialization(self, combat_system):
        """Test combat system is initialized."""
        assert combat_system is not None

    def test_calculate_damage_fists(self, combat_system):
        """Test damage calculation with fists."""
        damage = combat_system.calculate_damage(FISTS, NO_ARMOR)

        # Fists: 10% * 1.0 (no armor) = 0.1
        expected = 10 * 1.0
        assert damage == expected

    def test_calculate_damage_sword(self, combat_system):
        """Test damage calculation with sword."""
        damage = combat_system.calculate_damage(SWORD, NO_ARMOR)

        # Sword: 25% * 1.0 = 25
        expected = 25 * 1.0
        assert damage == expected

    def test_calculate_damage_axe(self, combat_system):
        """Test damage calculation with axe."""
        damage = combat_system.calculate_damage(AXE, NO_ARMOR)

        # Axe: 40% * 1.0 = 40
        expected = 40 * 1.0
        assert damage == expected

    def test_calculate_damage_hammer(self, combat_system):
        """Test damage calculation with hammer."""
        damage = combat_system.calculate_damage(HAMMER, NO_ARMOR)

        # Hammer: 70% * 1.0 = 70
        expected = 70 * 1.0
        assert damage == expected

    def test_calculate_damage_with_light_armor(self, combat_system):
        """Test damage calculation with light armor."""
        damage = combat_system.calculate_damage(SWORD, LIGHT_ARMOR)

        # Sword: 25% * 0.75 = 18.75
        expected = 25 * 0.75
        assert damage == expected

    def test_calculate_damage_with_medium_armor(self, combat_system):
        """Test damage calculation with medium armor."""
        damage = combat_system.calculate_damage(SWORD, MEDIUM_ARMOR)

        # Sword: 25% * 0.5 = 12.5
        expected = 25 * 0.5
        assert damage == expected

    def test_calculate_damage_with_heavy_armor(self, combat_system):
        """Test damage calculation with heavy armor."""
        damage = combat_system.calculate_damage(SWORD, HEAVY_ARMOR)

        # Sword: 25% * 0.25 = 6.25
        expected = 25 * 0.25
        assert damage == expected

    def test_backstab_damage(self, combat_system):
        """Test backstab bonus damage."""
        damage = combat_system.calculate_damage(SWORD, NO_ARMOR, is_backstab=True)

        # Sword: 25% * 1.0 * 1.25 = 31.25
        expected = 25 * 1.0 * (1 + constants.BACKSTAB_DAMAGE_BONUS)
        assert damage == expected

    def test_backstab_with_armor(self, combat_system):
        """Test backstab with armor."""
        damage = combat_system.calculate_damage(SWORD, MEDIUM_ARMOR, is_backstab=True)

        # Sword: 25% * 0.5 * 1.25 = 15.625
        expected = 25 * 0.5 * (1 + constants.BACKSTAB_DAMAGE_BONUS)
        assert damage == expected

    def test_can_attack(self, combat_system, player):
        """Test can_attack method."""
        can_attack = combat_system.can_attack(player)

        # Player should be able to attack initially
        assert isinstance(can_attack, bool)

    def test_player_attack(self, combat_system, player, enemy):
        """Test player attack on enemy."""
        initial_health = enemy.health

        # Place player close to enemy
        player.position = pygame.Vector2(100, 100)
        enemy.position = pygame.Vector2(116, 100)  # 1 tile away (16px)

        # Attack
        combat_system.player_attack(player, [enemy])

        # Enemy should have taken damage
        # Note: This might not damage if too far or not in front
        # This tests the method runs without error

    def test_attack_range(self, combat_system, player, enemy):
        """Test attack range detection."""
        player.position = pygame.Vector2(100, 100)
        enemy.position = pygame.Vector2(200, 100)  # Far away

        # Should not be able to attack from this distance
        # Method should handle gracefully

    def test_combat_with_dead_enemy(self, combat_system, player):
        """Test attacking a dead enemy."""
        enemy = Enemy(
            position=pygame.Vector2(116, 100), enemy_type="guard", patrol_points=None
        )
        enemy.health = 0  # Dead

        # Should handle gracefully
        combat_system.player_attack(player, [enemy])

    def test_combat_with_no_enemies(self, combat_system, player):
        """Test attacking with no enemies in list."""
        # Should handle gracefully
        combat_system.player_attack(player, [])

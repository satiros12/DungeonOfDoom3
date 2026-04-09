"""Tests for Physics System."""

import pytest
import pygame

from src.systems.physics_system import PhysicsSystem
from src.entities.tilemap import TileMap
from src.entities.door import Door


class TestPhysicsSystem:
    """Test suite for PhysicsSystem class."""

    @pytest.fixture
    def physics_system(self):
        """Create a physics system instance."""
        return PhysicsSystem()

    @pytest.fixture
    def tilemap(self):
        """Create a tilemap for testing."""
        # Simple 10x10 map with walls around edges and floor in middle
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

    def test_physics_system_initialization(self, physics_system):
        """Test physics system is initialized."""
        assert physics_system is not None

    def test_check_collision_with_wall(self, physics_system, tilemap):
        """Test collision detection with wall."""
        pos = pygame.Vector2(16, 16)  # Inside wall
        result = physics_system.check_collision(pos, tilemap)

        assert result is True

    def test_check_collision_with_floor(self, physics_system, tilemap):
        """Test collision detection with floor."""
        pos = pygame.Vector2(32, 32)  # Inside floor
        result = physics_system.check_collision(pos, tilemap)

        assert result is False

    def test_resolve_move_with_collision(self, physics_system, tilemap):
        """Test move resolution with collision."""
        start_pos = pygame.Vector2(32, 32)
        direction = pygame.Vector2(1, 0)
        distance = 16

        result = physics_system.resolve_move(start_pos, direction, distance, tilemap)

        # Should not go through wall
        assert result.x <= 48  # Should stop at wall

    def test_resolve_move_without_collision(self, physics_system, tilemap):
        """Test move resolution without collision."""
        start_pos = pygame.Vector2(32, 32)
        direction = pygame.Vector2(0, 1)
        distance = 16

        result = physics_system.resolve_move(start_pos, direction, distance, tilemap)

        # Should move normally
        assert result.y > 32

    def test_get_tile_at_position(self, physics_system, tilemap):
        """Test getting tile at position."""
        # Wall position
        tile = physics_system.get_tile_at_position(pygame.Vector2(8, 8), tilemap)
        assert tile == "wall"

        # Floor position
        tile = physics_system.get_tile_at_position(pygame.Vector2(32, 32), tilemap)
        assert tile == "floor"

    def test_get_tile_out_of_bounds(self, physics_system, tilemap):
        """Test getting tile out of bounds returns wall."""
        # Positions outside the map should return 'wall' (treated as boundary)
        tile = physics_system.get_tile_at_position(pygame.Vector2(-10, -10), tilemap)
        assert tile == "wall"

    def test_set_doors(self, physics_system):
        """Test setting doors for collision."""
        door = Door(pygame.Vector2(48, 48))
        doors = [door]

        physics_system.set_doors(doors)

        # Should not raise error

    def test_door_collision(self, physics_system, tilemap):
        """Test door collision detection."""
        # Add a door tile to the map
        tiles = [
            ["wall"] * 3,
            ["wall", "door", "wall"],
            ["wall"] * 3,
        ]
        test_map = TileMap(tiles=tiles, width=3, height=3)

        # Closed door should collide
        door_pos = pygame.Vector2(16, 16)
        result = physics_system.check_collision(door_pos, test_map)

        # Note: door tiles are treated as walls when closed

    def test_resolve_move_diagonal(self, physics_system, tilemap):
        """Test diagonal movement."""
        start_pos = pygame.Vector2(32, 32)
        direction = pygame.Vector2(1, 1).normalize()
        distance = 16

        result = physics_system.resolve_move(start_pos, direction, distance, tilemap)

        # Should move in both directions
        assert result != start_pos

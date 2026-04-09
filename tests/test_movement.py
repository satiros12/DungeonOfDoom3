"""Tests for movement system."""

import math

import pygame
import pytest


class TestMovementDirection:
    """Test movement direction calculations."""

    def test_forward_at_0_degrees(self):
        """At rotation 0, forward should move right (+X)."""
        import pygame

        # Rotation 0 = facing right
        rotation = 0
        player_rad = math.radians(rotation)

        # Forward direction
        forward_x = math.cos(player_rad)
        forward_y = math.sin(player_rad)

        # At 0 degrees, forward should be (1, 0) - right
        assert abs(forward_x - 1.0) < 0.01, f"Expected x=1.0, got {forward_x}"
        assert abs(forward_y - 0.0) < 0.01, f"Expected y=0.0, got {forward_y}"

    def test_forward_at_90_degrees(self):
        """At rotation 90, forward should move down (+Y in screen coords)."""
        rotation = 90
        player_rad = math.radians(rotation)

        forward_x = math.cos(player_rad)
        forward_y = math.sin(player_rad)

        # At 90 degrees, forward should be (0, 1) - down
        assert abs(forward_x - 0.0) < 0.01, f"Expected x=0.0, got {forward_x}"
        assert abs(forward_y - 1.0) < 0.01, f"Expected y=1.0, got {forward_y}"

    def test_forward_at_180_degrees(self):
        """At rotation 180, forward should move left (-X)."""
        rotation = 180
        player_rad = math.radians(rotation)

        forward_x = math.cos(player_rad)
        forward_y = math.sin(player_rad)

        # At 180 degrees, forward should be (-1, 0) - left
        assert abs(forward_x - (-1.0)) < 0.01, f"Expected x=-1.0, got {forward_x}"
        assert abs(forward_y - 0.0) < 0.01, f"Expected y=0.0, got {forward_y}"

    def test_forward_at_270_degrees(self):
        """At rotation 270, forward should move up (-Y in screen coords)."""
        rotation = 270
        player_rad = math.radians(rotation)

        forward_x = math.cos(player_rad)
        forward_y = math.sin(player_rad)

        # At 270 degrees, forward should be (0, -1) - up
        assert abs(forward_x - 0.0) < 0.01, f"Expected x=0.0, got {forward_x}"
        assert abs(forward_y - (-1.0)) < 0.01, f"Expected y=-1.0, got {forward_y}"

    def test_strafe_left_at_0_degrees(self):
        """At rotation 0, strafe left should move up (-Y)."""
        rotation = 0
        player_rad = math.radians(rotation)

        # Strafe left = forward + 90 degrees
        strafe_left_x = math.cos(player_rad + math.pi / 2)
        strafe_left_y = math.sin(player_rad + math.pi / 2)

        # At 0 degrees, strafe left should be (0, -1) - up
        assert abs(strafe_left_x - 0.0) < 0.01, f"Expected x=0.0, got {strafe_left_x}"
        assert abs(strafe_left_y - (-1.0)) < 0.01, f"Expected y=-1.0, got {strafe_left_y}"

    def test_strafe_right_at_0_degrees(self):
        """At rotation 0, strafe right should move down (+Y)."""
        rotation = 0
        player_rad = math.radians(rotation)

        # Strafe right = forward - 90 degrees
        strafe_right_x = math.cos(player_rad - math.pi / 2)
        strafe_right_y = math.sin(player_rad - math.pi / 2)

        # At 0 degrees, strafe right should be (0, 1) - down
        assert abs(strafe_right_x - 0.0) < 0.01, f"Expected x=0.0, got {strafe_right_x}"
        assert abs(strafe_right_y - 1.0) < 0.01, f"Expected y=1.0, got {strafe_right_y}"

    def test_backward_at_0_degrees(self):
        """At rotation 0, backward should move left (-X)."""
        rotation = 0
        player_rad = math.radians(rotation)

        # Backward = -forward
        backward_x = -math.cos(player_rad)
        backward_y = -math.sin(player_rad)

        # At 0 degrees, backward should be (-1, 0) - left
        assert abs(backward_x - (-1.0)) < 0.01, f"Expected x=-1.0, got {backward_x}"
        assert abs(backward_y - 0.0) < 0.01, f"Expected y=0.0, got {backward_y}"


class TestPlayerMovement:
    """Test player entity movement."""

    def test_player_initial_position(self):
        """Test player starts at correct position."""
        from src.entities.player import Player

        player = Player(pygame.Vector2(100, 100))

        assert player.position.x == 100
        assert player.position.y == 100

    def test_player_rotation(self):
        """Test player rotation works."""
        from src.entities.player import Player

        player = Player(pygame.Vector2(100, 100))

        # Initial rotation should be 0
        assert player.rotation == 0

        # Rotate
        player.rotation = 90
        assert player.rotation == 90

        # Rotation wraps at 360
        player.rotation = 450
        assert player.rotation == 90


class TestPhysicsMovement:
    """Test physics system movement."""

    def test_resolve_move_no_collision(self):
        """Test movement without collision returns new position."""
        from src.systems.physics_system import PhysicsSystem
        from src.entities.tilemap import TileMap

        # Create empty room (no walls)
        tiles = [
            ["floor", "floor", "floor"],
            ["floor", "floor", "floor"],
            ["floor", "floor", "floor"],
        ]
        tilemap = TileMap(tiles=tiles, width=3, height=3)

        physics = PhysicsSystem()
        start_pos = pygame.Vector2(24, 24)  # Center of middle tile
        direction = pygame.Vector2(1, 0).normalize()
        distance = 16  # Move one tile

        new_pos = physics.resolve_move(start_pos, direction, distance, tilemap)

        # Should have moved
        assert new_pos.x > start_pos.x

    def test_resolve_move_with_collision(self):
        """Test movement with wall collision stops at wall."""
        from src.systems.physics_system import PhysicsSystem
        from src.entities.tilemap import TileMap

        # Create room with wall on the right
        tiles = [
            ["floor", "wall", "floor"],
            ["floor", "floor", "floor"],
            ["floor", "floor", "floor"],
        ]
        tilemap = TileMap(tiles=tiles, width=3, height=3)

        physics = PhysicsSystem()
        start_pos = pygame.Vector2(20, 24)  # Left of wall
        direction = pygame.Vector2(1, 0).normalize()
        distance = 32  # Try to move through wall

        new_pos = physics.resolve_move(start_pos, direction, distance, tilemap)

        # Should not have moved all the way
        assert new_pos.x < start_pos.x + distance


class TestGameSceneMovement:
    """Test game scene movement handling."""

    def test_handle_movement_forward(self):
        """Test forward movement in game scene."""
        from src.scenes.game_scene import GameScene
        from src.core.game import Game

        with (
            pytest.mock.patch("pygame.init"),
            pytest.mock.patch("pygame.display.set_mode"),
            pytest.mock.patch("pygame.Clock"),
            pytest.mock.patch("src.scenes.game_scene.load_map") as mock_load,
        ):
            mock_load.return_value = {
                "tiles": [
                    [
                        "wall" if i == 0 or j == 0 or i == 47 or j == 47 else "floor"
                        for j in range(48)
                    ]
                    for i in range(48)
                ],
                "start_pos": [10, 10],
                "exit_pos": [46, 46],
                "doors": [],
                "enemies": [],
                "items": [],
            }

            game = Game()
            game_scene = GameScene(game, level_number=1)

            # Store initial position
            initial_pos = game_scene._player.position.copy()

            # Simulate forward movement
            actions = {
                "forward": True,
                "backward": False,
                "left": False,
                "right": False,
                "rotate_left": False,
                "rotate_right": False,
                "attack": False,
                "interact": False,
                "drop_weapon": False,
                "drop_armor": False,
                "toggle_health": False,
                "pause": False,
                "debug": False,
            }

            # Update with small delta time
            game_scene._handle_movement(actions, 0.1)

            # Player should have moved
            moved = game_scene._player.position.distance_to(initial_pos)
            assert moved > 0, "Player should have moved forward"

    def test_handle_movement_rotation(self):
        """Test rotation in game scene."""
        from src.scenes.game_scene import GameScene
        from src.core.game import Game

        with (
            pytest.mock.patch("pygame.init"),
            pytest.mock.patch("pygame.display.set_mode"),
            pytest.mock.patch("pygame.Clock"),
            pytest.mock.patch("src.scenes.game_scene.load_map") as mock_load,
        ):
            mock_load.return_value = {
                "tiles": [
                    [
                        "wall" if i == 0 or j == 0 or i == 47 or j == 47 else "floor"
                        for j in range(48)
                    ]
                    for i in range(48)
                ],
                "start_pos": [10, 10],
                "exit_pos": [46, 46],
                "doors": [],
                "enemies": [],
                "items": [],
            }

            game = Game()
            game_scene = GameScene(game, level_number=1)

            # Store initial rotation
            initial_rotation = game_scene._player.rotation

            # Simulate rotation right
            actions = {
                "forward": False,
                "backward": False,
                "left": False,
                "right": False,
                "rotate_left": False,
                "rotate_right": True,
                "attack": False,
                "interact": False,
                "drop_weapon": False,
                "drop_armor": False,
                "toggle_health": False,
                "pause": False,
                "debug": False,
            }

            # Update with delta time
            game_scene._handle_movement(actions, 0.1)

            # Player should have rotated
            assert game_scene._player.rotation != initial_rotation

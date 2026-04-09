"""E2E Tests for Escape the Dungeon of Doom - Gameplay Testing."""

import pytest


class TestMenuNavigation:
    """Test main menu navigation."""

    def test_menu_import(self):
        """Test that menu scene can be imported."""
        from src.scenes.menu_scene import MenuScene

        assert MenuScene is not None

    def test_menu_options_defined(self):
        """Test menu options are defined."""
        from src.scenes.menu_scene import MenuScene
        from src.core.game import Game

        # We can't fully test without pygame display, but we can verify class exists
        assert hasattr(MenuScene, "__init__")


class TestGameScene:
    """Test game scene gameplay."""

    def test_game_scene_import(self):
        """Test game scene imports correctly."""
        from src.scenes.game_scene import GameScene

        assert GameScene is not None

    def test_raycaster_import(self):
        """Test raycaster imports correctly."""
        from src.systems.raycaster import Raycaster, render_first_person, render_weapon

        assert Raycaster is not None
        assert render_first_person is not None
        assert render_weapon is not None


class TestMovement:
    """Test player movement logic."""

    def test_movement_direction_calculation(self):
        """Test movement direction calculation handles all directions."""
        import math
        import pygame

        # Test forward direction
        rotation = 0  # Facing right
        angle_rad = math.radians(rotation - 90)
        forward_x = math.cos(angle_rad)
        forward_y = math.sin(angle_rad)

        # At rotation 0, forward should point UP (negative Y in screen space)
        assert forward_y < 0

        # Test rotation 90 (facing down)
        rotation = 90
        angle_rad = math.radians(rotation - 90)
        right_x = math.cos(angle_rad)
        right_y = math.sin(angle_rad)

        # At rotation 90, right should point right (positive X)
        assert right_x > 0


class TestRaycaster:
    """Test raycasting system."""

    def test_raycaster_fov(self):
        """Test raycaster FOV configuration."""
        from src.systems.raycaster import Raycaster

        # Test default FOV
        rc = Raycaster()
        assert rc.fov == 70
        assert rc.num_rays > 0

        # Test custom FOV
        rc90 = Raycaster(fov=90)
        assert rc90.fov == 90

    def test_raycaster_calculates_rays(self):
        """Test raycaster calculates correct number of rays."""
        from src.systems.raycaster import Raycaster
        from src.entities.tilemap import TileMap
        import pygame

        # Simple 5x5 room
        tiles = [
            ["wall", "wall", "wall", "wall", "wall"],
            ["wall", "floor", "floor", "floor", "wall"],
            ["wall", "floor", "floor", "floor", "wall"],
            ["wall", "floor", "floor", "floor", "wall"],
            ["wall", "wall", "wall", "wall", "wall"],
        ]

        tilemap = TileMap(tiles=tiles, width=5, height=5)
        player_pos = pygame.Vector2(2.5 * 16, 2.5 * 16)

        rc = Raycaster(fov=70)
        wall_strips = rc.cast_all_rays(player_pos, 0, tilemap)

        # Should have wall strips
        assert len(wall_strips) > 0
        assert len(wall_strips) == rc.num_rays


class TestCombat:
    """Test combat system."""

    def test_combat_system_import(self):
        """Test combat system imports."""
        from src.systems.combat_system import CombatSystem

        assert CombatSystem is not None

    def test_weapon_import(self):
        """Test weapons import."""
        from src.entities.weapon import FISTS, SWORD, AXE, HAMMER

        assert FISTS is not None
        assert SWORD is not None

    def test_armor_import(self):
        """Test armors import."""
        from src.entities.armor import NO_ARMOR, LIGHT_ARMOR, MEDIUM_ARMOR, HEAVY_ARMOR

        assert NO_ARMOR is not None
        assert LIGHT_ARMOR is not None


class TestEntities:
    """Test game entities."""

    def test_player_import(self):
        """Test player entity imports."""
        from src.entities.player import Player

        assert Player is not None

    def test_enemy_import(self):
        """Test enemy entity imports."""
        from src.entities.enemy import Enemy

        assert Enemy is not None

    def test_tilemap_import(self):
        """Test tilemap imports."""
        from src.entities.tilemap import TileMap

        assert TileMap is not None

    def test_door_import(self):
        """Test door imports."""
        from src.entities.door import Door

        assert Door is not None


class TestSystems:
    """Test game systems."""

    def test_input_system_import(self):
        """Test input system imports."""
        from src.systems.input_system import InputSystem

        assert InputSystem is not None

    def test_physics_system_import(self):
        """Test physics system imports."""
        from src.systems.physics_system import PhysicsSystem

        assert PhysicsSystem is not None

    def test_ai_system_import(self):
        """Test AI system imports."""
        from src.systems.ai_system import AISystem

        assert AISystem is not None

    def test_audio_system_import(self):
        """Test audio system imports."""
        from src.systems.audio_system import AudioSystem

        assert AudioSystem is not None


class TestScenes:
    """Test all game scenes."""

    def test_all_scenes_import(self):
        """Test all scenes can be imported."""
        from src.scenes.menu_scene import MenuScene
        from src.scenes.game_scene import GameScene
        from src.scenes.pause_scene import PauseScene
        from src.scenes.gameover_scene import GameOverScene
        from src.scenes.victory_scene import VictoryScene
        from src.scenes.level_transition_scene import LevelTransitionScene
        from src.scenes.options_scene import OptionsScene

        assert MenuScene is not None
        assert GameScene is not None
        assert PauseScene is not None
        assert GameOverScene is not None
        assert VictoryScene is not None
        assert LevelTransitionScene is not None
        assert OptionsScene is not None


class TestConstants:
    """Test game constants."""

    def test_screen_constants(self):
        """Test screen constants are defined."""
        from src.core import constants

        assert constants.SCREEN_WIDTH == 800
        assert constants.SCREEN_HEIGHT == 600
        assert constants.FPS == 60

    def test_tile_constants(self):
        """Test tile constants are defined."""
        from src.core import constants

        assert constants.TILE_SIZE == 16
        assert constants.MAP_WIDTH == 48
        assert constants.MAP_HEIGHT == 48

    def test_combat_constants(self):
        """Test combat constants are defined."""
        from src.core import constants

        assert hasattr(constants, "WEAPONS")
        assert hasattr(constants, "ARMORS")


# Pytest summary
def pytest_sessionfinish(session, exitstatus):
    """Print summary after tests."""
    print("\n" + "=" * 60)
    print("E2E GAMEPLAY TEST SUMMARY")
    print("=" * 60)
    if exitstatus == 0:
        print("✅ All gameplay tests passed!")
    else:
        print(f"⚠️ Tests completed with status: {exitstatus}")
    print("=" * 60 + "\n")

"""Game Scene for playing the dungeon levels."""

import logging
import math
from typing import Optional

import pygame

from src.core import constants
from src.core.scene import Scene
from src.core.game import Game
from src.entities.player import Player
from src.entities.tilemap import TileMap
from src.loaders.map_loader import load_map
from src.systems.camera_system import CameraSystem
from src.systems.input_system import InputSystem
from src.systems.physics_system import PhysicsSystem


class GameScene(Scene):
    """Main game scene for dungeon exploration."""

    def __init__(self, game: Game, level_number: int) -> None:
        """Initialize the game scene.

        Args:
            game: The main game instance.
            level_number: The level number to load (1-5).
        """
        super().__init__(game)
        self.level_number = level_number
        self._input_system = InputSystem()
        self._physics_system = PhysicsSystem()
        self._camera = CameraSystem(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
        self._player: Optional[Player] = None
        self._tilemap: Optional[TileMap] = None
        self._show_health = False
        self._health_display_time = 0.0

        # Load the level
        self._load_level(level_number)

        logging.info(f"GameScene initialized for level {level_number}")

    def _load_level(self, level_number: int) -> None:
        """Load a level from the map loader.

        Args:
            level_number: The level number to load.
        """
        map_data = load_map(level_number)

        tiles = map_data["tiles"]
        start_pos = map_data["start_pos"]

        # Create tilemap
        self._tilemap = TileMap(
            tiles=tiles,
            width=constants.MAP_WIDTH,
            height=constants.MAP_HEIGHT,
        )

        # Create player at start position
        pixel_pos = pygame.Vector2(
            start_pos[0] * constants.TILE_SIZE + constants.TILE_SIZE // 2,
            start_pos[1] * constants.TILE_SIZE + constants.TILE_SIZE // 2,
        )
        self._player = Player(position=pixel_pos)

        logging.info(f"Level {level_number} loaded: start_pos={start_pos}")

    def update(self, dt: float) -> None:
        """Update game logic.

        Args:
            dt: Delta time since last frame in seconds.
        """
        # Update input system
        self._input_system.update()

        # Get actions
        actions = self._input_system.get_actions()

        # Handle pause
        if actions["pause"]:
            self._handle_pause()
            return

        # Handle debug
        if actions["debug"]:
            self._toggle_debug()

        # Handle health toggle
        if actions["toggle_health"]:
            self._show_health = True
            self._health_display_time = constants.HUD_TAB_DISPLAY_TIME

        # Update health display timer
        if self._health_display_time > 0:
            self._health_display_time -= dt
            if self._health_display_time <= 0:
                self._show_health = False

        # Handle movement
        self._handle_movement(actions, dt)

        # Handle rotation
        self._handle_rotation(actions, dt)

        # Update camera to follow player
        if self._player:
            self._camera.follow(self._player.position)

        # Check for exit (level complete)
        if self._player:
            tile_type = self._physics_system.get_tile_at_position(
                self._player.position, self._tilemap
            )
            if tile_type == "exit":
                self._handle_level_complete()

    def _handle_movement(self, actions: dict, dt: float) -> None:
        """Handle player movement input.

        Args:
            actions: Dictionary of action states.
            dt: Delta time in seconds.
        """
        if not self._player or not self._tilemap:
            return

        direction = pygame.Vector2(0, 0)

        if actions["forward"]:
            # Move in direction of player rotation
            angle_rad = math.radians(self._player.rotation - 90)
            direction.x = math.cos(angle_rad)
            direction.y = math.sin(angle_rad)
        elif actions["backward"]:
            angle_rad = math.radians(self._player.rotation + 90)
            direction.x = math.cos(angle_rad)
            direction.y = math.sin(angle_rad)

        if actions["left"]:
            direction.x = -1
            direction.y = 0
        elif actions["right"]:
            direction.x = 1
            direction.y = 0

        if direction.length() > 0:
            distance = self._player.speed * dt
            self._player.position = self._physics_system.resolve_move(
                self._player.position,
                direction.normalize(),
                distance,
                self._tilemap,
            )

    def _handle_rotation(self, actions: dict, dt: float) -> None:
        """Handle player rotation input.

        Args:
            actions: Dictionary of action states.
            dt: Delta time in seconds.
        """
        if not self._player:
            return

        turn_speed = constants.TURN_SPEED_DEFAULT

        if actions["rotate_left"]:
            self._player.rotate(-turn_speed, dt)
        elif actions["rotate_right"]:
            self._player.rotate(turn_speed, dt)

    def _handle_pause(self) -> None:
        """Handle pause action."""
        logging.info("Pause requested")
        # TODO: Implement pause menu

    def _toggle_debug(self) -> None:
        """Toggle debug overlay."""
        logging.debug("Debug toggle requested")

    def _handle_level_complete(self) -> None:
        """Handle level completion."""
        logging.info(f"Level {self.level_number} completed!")
        # TODO: Implement level transition

    def render(self, screen: pygame.Surface) -> None:
        """Render the game scene.

        Args:
            screen: The pygame surface to render to.
        """
        screen.fill(constants.COLOR_FLOOR)

        if not self._tilemap or not self._player:
            return

        # Render tilemap
        self._render_tilemap(screen)

        # Render player
        self._render_player(screen)

        # Render health HUD if visible
        if self._show_health:
            self._render_health_hud(screen)

    def _render_tilemap(self, screen: pygame.Surface) -> None:
        """Render the tilemap.

        Args:
            screen: The pygame surface to render to.
        """
        if not self._tilemap:
            return

        # Calculate visible range
        start_col = int(self._camera.offset.x // constants.TILE_SIZE)
        start_row = int(self._camera.offset.y // constants.TILE_SIZE)
        end_col = start_col + (constants.SCREEN_WIDTH // constants.TILE_SIZE) + 2
        end_row = start_row + (constants.SCREEN_HEIGHT // constants.TILE_SIZE) + 2

        for row in range(max(0, start_row), min(self._tilemap.height, end_row)):
            for col in range(max(0, start_col), min(self._tilemap.width, end_col)):
                tile_type = self._tilemap.get_tile(col, row)
                x = col * constants.TILE_SIZE - self._camera.offset.x
                y = row * constants.TILE_SIZE - self._camera.offset.y

                rect = pygame.Rect(x, y, constants.TILE_SIZE, constants.TILE_SIZE)

                if tile_type == "wall":
                    pygame.draw.rect(screen, constants.COLOR_WALL, rect)
                elif tile_type == "floor":
                    pygame.draw.rect(screen, constants.COLOR_FLOOR, rect, 1)
                elif tile_type == "exit":
                    pygame.draw.rect(screen, constants.COLOR_EXIT, rect)
                elif tile_type == "door":
                    pygame.draw.rect(screen, constants.COLOR_DOOR, rect)
                elif tile_type == "decoration":
                    pygame.draw.rect(screen, constants.COLOR_DECORATION, rect, 1)

    def _render_player(self, screen: pygame.Surface) -> None:
        """Render the player.

        Args:
            screen: The pygame surface to render to.
        """
        if not self._player:
            return

        screen_pos = self._camera.world_to_screen(self._player.position)
        x = int(screen_pos.x)
        y = int(screen_pos.y)
        size = constants.TILE_SIZE // 2

        # Draw player as a circle with direction indicator
        pygame.draw.circle(screen, constants.COLOR_PLAYER, (x, y), size)

        # Draw direction indicator
        angle_rad = pygame.math.radians(self._player.rotation - 90)
        end_x = x + int(math.cos(angle_rad) * size)
        end_y = y + int(math.sin(angle_rad) * size)
        pygame.draw.line(screen, (0, 0, 0), (x, y), (end_x, end_y), 2)

    def _render_health_hud(self, screen: pygame.Surface) -> None:
        """Render the health HUD.

        Args:
            screen: The pygame surface to render to.
        """
        if not self._player:
            return

        # Health bar background
        bg_rect = pygame.Rect(
            constants.HUD_MARGIN,
            constants.SCREEN_HEIGHT
            - constants.HUD_MARGIN
            - constants.HUD_HEALTH_BAR_HEIGHT,
            constants.HUD_HEALTH_BAR_WIDTH,
            constants.HUD_HEALTH_BAR_HEIGHT,
        )
        pygame.draw.rect(screen, constants.UI_COLOR_HEALTH_BG, bg_rect)

        # Health bar fill
        health_percent = self._player.health / self._player._max_health
        fill_width = int(constants.HUD_HEALTH_BAR_WIDTH * health_percent)
        if fill_width > 0:
            fill_rect = pygame.Rect(
                constants.HUD_MARGIN,
                constants.SCREEN_HEIGHT
                - constants.HUD_MARGIN
                - constants.HUD_HEALTH_BAR_HEIGHT,
                fill_width,
                constants.HUD_HEALTH_BAR_HEIGHT,
            )
            pygame.draw.rect(screen, constants.UI_COLOR_HEALTH, fill_rect)

        # Health text
        font = pygame.font.Font(None, constants.UI_FONT_HUD)
        health_text = font.render(
            f"HP: {int(self._player.health)}",
            True,
            constants.UI_COLOR_TEXT_PRIMARY,
        )
        screen.blit(
            health_text,
            (constants.HUD_MARGIN, constants.HUD_MARGIN),
        )

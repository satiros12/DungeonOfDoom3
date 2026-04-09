"""Game Scene for playing the dungeon levels."""

import json
import logging
import math
from typing import Optional, List

import pygame

from src.core import constants
from src.core.scene import Scene
from src.core.game import Game
from src.entities.player import Player
from src.entities.tilemap import TileMap
from src.entities.door import Door
from src.entities.enemy import Enemy
from src.entities.item import Item, ItemType
from src.loaders.map_loader import load_map
from src.loaders.patrol_loader import load_patrols
from src.loaders.enemy_loader import load_enemies
from src.loaders.item_loader import load_items
from src.systems.camera_system import CameraSystem
from src.systems.input_system import InputSystem
from src.systems.physics_system import PhysicsSystem
from src.systems.ai_system import AISystem
from src.systems.combat_system import CombatSystem
from src.systems.audio_system import AudioSystem
from src.systems.raycaster import Raycaster, render_first_person, render_weapon


def load_options() -> dict:
    """Load game options from config file."""
    try:
        with open("config/options.json", "r") as f:
            return json.load(f)
    except Exception:
        return {
            "fullscreen": False,
            "turn_speed": 90,
            "music_volume": 0.7,
            "sfx_volume": 0.5,
        }


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
        self._ai_system = AISystem(level_number)
        self._combat_system = CombatSystem()
        self._audio_system = AudioSystem()
        self._raycaster = Raycaster(fov=70)
        self._player: Optional[Player] = None
        self._tilemap: Optional[TileMap] = None
        self._doors: List[Door] = []
        self._enemies: List[Enemy] = []
        self._items: List[Item] = []
        self._show_health = False
        self._health_display_time = 0.0
        self._show_debug = False
        self._attack_animation = 0.0  # Weapon attack animation progress
        self._options = load_options()
        self._turn_speed = self._options.get("turn_speed", constants.TURN_SPEED_DEFAULT)

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

        # Find and create doors from the tilemap
        self._doors = []
        for row in range(len(tiles)):
            for col in range(len(tiles[row])):
                if tiles[row][col] == "door":
                    door_pos = pygame.Vector2(
                        col * constants.TILE_SIZE,
                        row * constants.TILE_SIZE,
                    )
                    self._doors.append(Door(door_pos))

        # Pass doors to physics system for collision detection
        self._physics_system.set_doors(self._doors)

        # Load enemies
        self._enemies = []
        patrols = load_patrols(level_number)
        enemies_data = load_enemies(level_number)

        for enemy_data in enemies_data:
            patrol_id = enemy_data.get("patrol_id", -1)
            patrol_points = patrols[patrol_id] if 0 <= patrol_id < len(patrols) else None

            enemy = Enemy(
                position=enemy_data["position"],
                enemy_type=enemy_data.get("type", "guard"),
                patrol_points=patrol_points,
            )
            self._enemies.append(enemy)

        # Load items
        self._items = load_items(level_number)

        logging.info(
            f"Level {level_number} loaded: start_pos={start_pos}, "
            f"enemies={len(self._enemies)}, items={len(self._items)}"
        )

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

        # Handle item interaction (E key)
        if actions["interact"]:
            self._handle_item_interaction()

        # Handle drop weapon (I key)
        if actions.get("drop_weapon", False):
            self._handle_drop_weapon()

        # Handle drop armor (J key)
        if actions.get("drop_armor", False):
            self._handle_drop_armor()

        # Handle attack (Space key)
        if actions["attack"]:
            self._handle_attack()

        # Update enemies AI
        if self._player and self._tilemap:
            self._ai_system.update_enemies(
                self._enemies, self._player, self._tilemap, self._doors, dt
            )

        # Check enemy-player collision
        for enemy in self._enemies:
            if enemy.is_alive() and self._ai_system.check_enemy_player_collision(
                enemy, self._player
            ):
                if enemy.can_attack():
                    enemy.attack()
                    player_damage = enemy.get_damage()
                    self._player.take_damage(player_damage)
                    logging.info(f"Player hit by enemy, damage: {player_damage}")

        # Check for player death
        if self._player and self._player.health <= 0:
            self._handle_player_death()
            return

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
        rotation_direction = 0

        # Get player rotation in radians (0 = facing right, 90 = facing down)
        # In screen coordinates: right=+X, down=+Y
        player_rad = math.radians(self._player.rotation)

        # Forward - move in direction player is facing
        if actions["forward"]:
            direction.x += math.cos(player_rad)
            direction.y += math.sin(player_rad)

        # Backward - move opposite to facing direction
        if actions["backward"]:
            direction.x -= math.cos(player_rad)
            direction.y -= math.sin(player_rad)

        # Strafe left - perpendicular to facing direction (90 degrees left)
        if actions["left"]:
            direction.x += math.cos(player_rad - math.pi / 2)
            direction.y += math.sin(player_rad - math.pi / 2)

        # Strafe right - perpendicular to facing direction (90 degrees right)
        if actions["right"]:
            direction.x += math.cos(player_rad + math.pi / 2)
            direction.y += math.sin(player_rad + math.pi / 2)

        # Rotation with arrow keys (separate from movement)
        if actions["rotate_left"]:
            rotation_direction = -1
        if actions["rotate_right"]:
            rotation_direction = 1

        # Apply rotation
        if rotation_direction != 0:
            self._player.rotation += self._turn_speed * rotation_direction * dt
            self._player.rotation = self._player.rotation % 360

        if direction.length() > 0:
            # Use armor speed modifier
            speed_modifier = self._player.armor.speed_multiplier
            distance = self._player.speed * speed_modifier * dt
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

        turn_speed = self._turn_speed

        if actions["rotate_left"]:
            self._player.rotate(-turn_speed, dt)
        elif actions["rotate_right"]:
            self._player.rotate(turn_speed, dt)

    def _handle_item_interaction(self) -> None:
        """Handle item pickup with E key."""
        if not self._player or not self._items:
            return

        player_pos = self._player.position
        pickup_range = constants.TILE_SIZE * 1.5  # 1.5 tiles range

        for item in self._items:
            distance = player_pos.distance_to(item.position)
            if distance <= pickup_range:
                # Equip the item
                item.equip(self._player)
                # Remove item from world
                self._items.remove(item)
                logging.info(f"Picked up item: {item.get_name()}")
                break

    def _handle_drop_weapon(self) -> None:
        """Handle dropping weapon with I key."""
        if self._player:
            self._player.drop_weapon()

    def _handle_drop_armor(self) -> None:
        """Handle dropping armor with J key."""
        if self._player:
            self._player.drop_armor()

    def _handle_attack(self) -> None:
        """Handle player attack with Space key."""
        if not self._player:
            return

        # Use combat system to process attack
        self._combat_system.player_attack(self._player, self._enemies)

    def _handle_pause(self) -> None:
        """Handle pause action."""
        logging.info("Pause requested")
        from src.scenes.pause_scene import PauseScene

        self.game.scene_manager.push(PauseScene(self.game, self))

    def _handle_door_interaction(self) -> None:
        """Handle door interaction (E key)."""
        if not self._player or not self._tilemap:
            return

        # Check if player is near a door tile
        player_col = int(self._player.position.x // constants.TILE_SIZE)
        player_row = int(self._player.position.y // constants.TILE_SIZE)

        # Check adjacent tiles for doors
        nearby_door = None
        for door in self._doors:
            door_col = int(door.position.x // constants.TILE_SIZE)
            door_row = int(door.position.y // constants.TILE_SIZE)

            # Check if adjacent (within 1 tile)
            if abs(door_col - player_col) <= 1 and abs(door_row - player_row) <= 1:
                nearby_door = door
                break

        if nearby_door:
            nearby_door.toggle()
            logging.info(f"Door toggled: open={nearby_door.is_open}")

    def _toggle_debug(self) -> None:
        """Toggle debug overlay."""
        self._show_debug = not self._show_debug
        logging.debug(f"Debug overlay: {self._show_debug}")

    def _handle_level_complete(self) -> None:
        """Handle level completion."""
        logging.info(f"Level {self.level_number} completed!")

        # Determine next level
        next_level = self.level_number + 1
        if next_level > 5:
            # Victory - all levels complete
            from src.scenes.victory_scene import VictoryScene

            self.game.scene_manager.replace(VictoryScene(self.game))
        else:
            # Transition to next level
            level_name = constants.LEVEL_NAMES.get(next_level, "Unknown")
            from src.scenes.level_transition_scene import LevelTransitionScene

            self.game.scene_manager.replace(LevelTransitionScene(self.game, level_name, next_level))

    def _handle_player_death(self) -> None:
        """Handle player death."""
        logging.info("Player died!")
        from src.scenes.gameover_scene import GameOverScene

        self.game.scene_manager.replace(GameOverScene(self.game))

    def render(self, screen: pygame.Surface) -> None:
        """Render the game scene in first-person view.

        Args:
            screen: The pygame surface to render to.
        """
        screen.fill(constants.COLOR_FLOOR)

        if not self._tilemap or not self._player:
            return

        # Cast rays and render first-person view
        wall_strips = self._raycaster.cast_all_rays(
            self._player.position,
            self._player.rotation,
            self._tilemap,
        )
        render_first_person(screen, wall_strips)

        # Render weapon at bottom
        weapon_name = self._player.weapon.name if self._player.weapon else "Fists"
        render_weapon(screen, weapon_name, self._attack_animation)

        # Render health HUD if visible
        if self._show_health:
            self._render_health_hud(screen)

        # Render debug overlay if visible
        if self._show_debug:
            self._render_debug_overlay(screen)

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

    def _render_items(self, screen: pygame.Surface) -> None:
        """Render items on the ground.

        Args:
            screen: The pygame surface to render to.
        """
        for item in self._items:
            screen_pos = self._camera.world_to_screen(item.position)
            x = int(screen_pos.x)
            y = int(screen_pos.y)
            size = constants.TILE_SIZE // 3

            # Draw item as a small square (yellow/different color based on type)
            if item.item_type == ItemType.WEAPON:
                color = (255, 165, 0)  # Orange for weapons
            else:
                color = (0, 191, 255)  # Light blue for armor

            rect = pygame.Rect(x - size, y - size, size * 2, size * 2)
            pygame.draw.rect(screen, color, rect)

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
        angle_rad = math.radians(self._player.rotation - 90)
        end_x = x + int(math.cos(angle_rad) * size)
        end_y = y + int(math.sin(angle_rad) * size)
        pygame.draw.line(screen, (0, 0, 0), (x, y), (end_x, end_y), 2)

    def _render_enemies(self, screen: pygame.Surface) -> None:
        """Render enemies.

        Args:
            screen: The pygame surface to render to.
        """
        for enemy in self._enemies:
            if not enemy.is_alive():
                continue

            screen_pos = self._camera.world_to_screen(enemy.position)
            x = int(screen_pos.x)
            y = int(screen_pos.y)
            size = constants.TILE_SIZE // 2

            # Draw enemy as a circle (red) with direction indicator
            pygame.draw.circle(screen, constants.COLOR_ENEMY, (x, y), size)

            # Draw direction indicator
            angle_rad = math.radians(enemy.rotation - 90)
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
            constants.SCREEN_HEIGHT - constants.HUD_MARGIN - constants.HUD_HEALTH_BAR_HEIGHT,
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
                constants.SCREEN_HEIGHT - constants.HUD_MARGIN - constants.HUD_HEALTH_BAR_HEIGHT,
                fill_width,
                constants.HUD_HEALTH_BAR_HEIGHT,
            )
            pygame.draw.rect(screen, constants.UI_COLOR_HEALTH, fill_rect)

        # Health text with weapon/armor info
        font = pygame.font.Font(None, constants.UI_FONT_HUD)
        health_text = font.render(
            f"HP: {int(self._player.health)} | {self._player.weapon.name} | {self._player.armor.name}",
            True,
            constants.UI_COLOR_TEXT_PRIMARY,
        )
        screen.blit(
            health_text,
            (constants.HUD_MARGIN, constants.HUD_MARGIN),
        )

    def _render_debug_overlay(self, screen: pygame.Surface) -> None:
        """Render the debug overlay with game information.

        Args:
            screen: The pygame surface to render to.
        """
        if not self._player:
            return

        # Get FPS from game clock (approximate)
        fps = 60  # This would need to be passed from Game

        # Calculate alive enemies
        alive_enemies = sum(1 for e in self._enemies if e.is_alive())

        # Debug information
        debug_info = [
            f"FPS: {fps}",
            f"Player Pos: ({int(self._player.position.x)}, {int(self._player.position.y)})",
            f"Player Rotation: {int(self._player.rotation)}°",
            f"Current State: {'Alive' if self._player.is_alive() else 'Dead'}",
            f"Level: {self.level_number}",
            f"Enemies Alive: {alive_enemies}",
            f"Weapon: {self._player.weapon.name}",
            f"Armor: {self._player.armor.name}",
            f"Turn Speed: {self._turn_speed}°/s",
        ]

        # Render debug background
        font = pygame.font.Font(None, constants.UI_FONT_DEBUG)
        line_height = 18
        padding = 10

        # Calculate background dimensions
        max_width = max(font.size(line)[0] for line in debug_info)
        bg_rect = pygame.Rect(
            10, 10, max_width + padding * 2, len(debug_info) * line_height + padding * 2
        )

        # Draw semi-transparent background
        bg_surface = pygame.Surface((bg_rect.width, bg_rect.height))
        bg_surface.set_alpha(180)
        bg_surface.fill((0, 0, 0))
        screen.blit(bg_surface, bg_rect.topleft)

        # Render debug text
        for i, line in enumerate(debug_info):
            text = font.render(line, True, (0, 255, 0))
            screen.blit(text, (bg_rect.x + padding, bg_rect.y + padding + i * line_height))

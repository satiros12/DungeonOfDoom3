"""Simplified raycasting engine for first-person DOOM-style rendering."""

import logging
import math
from typing import List, Tuple

import pygame

from src.core import constants


class WallStrip:
    """Represents a rendered wall strip."""

    def __init__(self, x: int, height: int, color: pygame.Color, is_door: bool = False) -> None:
        self.x = x
        self.height = height
        self.color = color
        self.is_door = is_door


class Raycaster:
    """First-person raycasting engine like Classic DOOM."""

    def __init__(self, fov: int = 70) -> None:
        """Initialize the raycaster.

        Args:
            fov: Field of view in degrees.
        """
        self.fov = fov
        self.fov_rad = math.radians(fov)
        self.half_fov = self.fov_rad / 2
        self.num_rays = constants.SCREEN_WIDTH // 2  # Ray every 2 pixels
        self.delta_angle = self.fov_rad / self.num_rays
        self.max_depth = constants.MAP_WIDTH * constants.TILE_SIZE * 2
        self.wall_strips: List[WallStrip] = []

    def cast_all_rays(
        self,
        player_pos: pygame.Vector2,
        player_rotation: float,
        tilemap,
    ) -> List[WallStrip]:
        """Cast rays in a fan pattern to render walls.

        Args:
            player_pos: Player position in pixels.
            player_rotation: Player rotation in degrees.
            tilemap: The tile map to render.

        Returns:
            List of wall strips to render.
        """
        self.wall_strips = []

        # Convert rotation to radians (0 = right, 90 = down in screen coords)
        player_rad = math.radians(player_rotation)

        # Starting angle (leftmost ray)
        start_angle = player_rad - self.half_fov

        for i in range(self.num_rays):
            # Calculate ray angle
            ray_angle = start_angle + i * self.delta_angle

            # Ray direction in screen coordinates
            # X increases right, Y increases down
            ray_dir_x = math.cos(ray_angle)
            ray_dir_y = -math.sin(ray_angle)  # Negate because Y is inverted in screen

            # Cast ray and get distance
            distance, hit_tile, hit_side = self._cast_ray_simple(
                player_pos.x, player_pos.y, ray_dir_x, ray_dir_y, tilemap
            )

            if distance > 0:
                # Prevent division by zero
                distance = max(1.0, distance)

                # Fix fisheye effect
                angle_diff = ray_angle - player_rad
                distance = distance * math.cos(angle_diff)

                # Calculate wall height based on distance
                # Closer walls are taller, farther walls are shorter
                # Adjust the divisor to change the "lens" effect
                wall_height = int(constants.SCREEN_HEIGHT / (distance / 50))

                # Clamp wall height
                wall_height = max(10, min(wall_height, constants.SCREEN_HEIGHT))

                # Get wall color with shading
                color = self._get_wall_color(hit_tile, hit_side, distance)

                strip = WallStrip(
                    x=i * 2,  # Every 2 pixels
                    height=wall_height,
                    color=color,
                    is_door=(hit_tile == "door"),
                )
                self.wall_strips.append(strip)

        return self.wall_strips

    def _cast_ray_simple(
        self,
        start_x: float,
        start_y: float,
        dir_x: float,
        dir_y: float,
        tilemap,
    ) -> Tuple[float, str, int]:
        """Simple ray casting using step method.

        Args:
            start_x: Starting X position in pixels.
            start_y: Starting Y position in pixels.
            dir_x: Ray direction X.
            dir_y: Ray direction Y.
            tilemap: The tile map.

        Returns:
            Tuple of (distance, tile_type, side).
        """
        # Normalize direction
        length = math.sqrt(dir_x * dir_x + dir_y * dir_y)
        if length == 0:
            return 1.0, "wall", 0

        dir_x /= length
        dir_y /= length

        # Start from player position
        x = start_x
        y = start_y

        # Step size (smaller = more accurate but slower)
        step_size = 2.0  # pixels

        distance = 0.0
        max_distance = self.max_depth

        side = 0  # 0 = hit vertical side, 1 = hit horizontal side

        while distance < max_distance:
            # Move along ray
            x += dir_x * step_size
            y += dir_y * step_size
            distance += step_size

            # Convert to map coordinates
            map_x = int(x / constants.TILE_SIZE)
            map_y = int(y / constants.TILE_SIZE)

            # Check bounds
            if map_x < 0 or map_x >= tilemap.width or map_y < 0 or map_y >= tilemap.height:
                return distance, "wall", side

            # Check for wall
            tile = tilemap.get_tile(map_x, map_y)
            if tile == "wall" or tile == "door":
                # Determine which side was hit
                prev_map_x = int((x - dir_x * step_size) / constants.TILE_SIZE)
                prev_map_y = int((y - dir_y * step_size) / constants.TILE_SIZE)

                if prev_map_x != map_x:
                    side = 0  # Hit vertical side
                else:
                    side = 1  # Hit horizontal side

                return distance, tile, side

        return max_distance, "wall", 0

    def _get_wall_color(self, tile: str, side: int, distance: float) -> pygame.Color:
        """Get wall color with shading based on distance and side.

        Args:
            tile: Tile type.
            side: Which side was hit (0 = vertical, 1 = horizontal).
            distance: Distance to wall.

        Returns:
            Color with shading applied.
        """
        # Base colors
        base_colors = {
            "wall": (120, 120, 120),  # Gray walls
            "door": (100, 100, 200),  # Blue doors
        }

        base_color = base_colors.get(tile, (120, 120, 120))

        # Apply side shading (horizontal side is darker)
        if side == 1:
            base_color = tuple(max(0, c - 40) for c in base_color)

        # Apply distance shading (farther = darker)
        max_dist = self.max_depth
        shade_factor = max(0.2, 1.0 - (distance / max_dist) * 0.8)
        shaded_color = tuple(int(c * shade_factor) for c in base_color)

        return pygame.Color(*shaded_color)


def render_first_person(
    screen: pygame.Surface,
    wall_strips: List[WallStrip],
) -> None:
    """Render first-person view using wall strips.

    Args:
        screen: Pygame surface to render to.
        wall_strips: List of wall strips to render.
    """
    # Draw ceiling (dark gray)
    ceiling_color = (30, 30, 30)
    ceiling_rect = pygame.Rect(0, 0, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT // 2)
    pygame.draw.rect(screen, ceiling_color, ceiling_rect)

    # Draw floor (slightly lighter gray)
    floor_color = (40, 40, 40)
    floor_rect = pygame.Rect(
        0, constants.SCREEN_HEIGHT // 2, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT // 2
    )
    pygame.draw.rect(screen, floor_color, floor_rect)

    # Draw floor line (horizon)
    pygame.draw.line(
        screen,
        (60, 60, 60),
        (0, constants.SCREEN_HEIGHT // 2),
        (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT // 2),
        2,
    )

    # Draw wall strips
    for strip in wall_strips:
        # Calculate vertical position (center the wall)
        wall_top = (constants.SCREEN_HEIGHT - strip.height) // 2
        wall_bottom = wall_top + strip.height

        # Draw the wall strip
        rect = pygame.Rect(strip.x, wall_top, 2, strip.height)
        pygame.draw.rect(screen, strip.color, rect)


def render_weapon(screen: pygame.Surface, weapon_name: str, attack_animation: float = 0.0) -> None:
    """Render the weapon at bottom of screen.

    Args:
        screen: Pygame surface to render to.
        weapon_name: Name of the equipped weapon.
        attack_animation: Animation progress (0.0 to 1.0).
    """
    # Weapon position at bottom center
    weapon_width = 120
    weapon_height = 160
    weapon_x = (constants.SCREEN_WIDTH - weapon_width) // 2
    weapon_y = constants.SCREEN_HEIGHT - weapon_height

    # Weapon colors based on type
    weapon_colors = {
        "Fists": (200, 150, 100),
        "Sword": (150, 150, 200),
        "Axe": (150, 100, 50),
        "Hammer": (100, 100, 120),
    }

    color = weapon_colors.get(weapon_name, (150, 150, 150))

    # Apply attack animation offset
    if attack_animation > 0:
        offset_y = int(attack_animation * 30)
        weapon_y += offset_y

    # Draw weapon as a simple shape
    weapon_rect = pygame.Rect(weapon_x + 20, weapon_y + 40, weapon_width - 40, weapon_height - 80)
    pygame.draw.rect(screen, color, weapon_rect, border_radius=5)

    # Draw weapon handle
    handle_rect = pygame.Rect(weapon_x + 45, weapon_y + weapon_height - 60, 30, 40)
    pygame.draw.rect(screen, (80, 60, 40), handle_rect, border_radius=3)

    # Draw weapon name below
    font = pygame.font.Font(None, 24)
    text = font.render(weapon_name.upper(), True, (200, 200, 200))
    text_rect = text.get_rect(center=(constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT - 15))
    screen.blit(text, text_rect)

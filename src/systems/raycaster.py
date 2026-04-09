"""Raycasting engine for first-person DOOM-style rendering."""

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
        self.num_rays = constants.SCREEN_WIDTH // 2  # Ray every 2 pixels for performance
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
        player_rad = math.radians(player_rotation)
        start_angle = player_rad - self.half_fov

        for i in range(self.num_rays):
            angle = start_angle + i * self.delta_angle
            # In screen coordinates: X increases right, Y increases down
            # So we need to negate sin to match screen coords
            ray_dir_x = math.cos(angle)
            ray_dir_y = -math.sin(angle)  # Negate for screen coordinate system

            # Cast ray
            distance, hit_tile, hit_side = self._cast_ray(
                player_pos.x, player_pos.y, ray_dir_x, ray_dir_y, tilemap
            )

            if distance > 0:
                # Prevent division by zero
                distance = max(0.1, distance)

                # Fix fisheye effect - use raw angle for correction
                # Need to account for the negated Y
                fisheye_angle = angle - player_rad
                distance *= math.cos(fisheye_angle)

                # Calculate wall height (closer = taller)
                # Scale factor adjusted for screen coordinates
                wall_height = int((constants.SCREEN_HEIGHT * 32) / distance)

                # Limit wall height to prevent overflow
                wall_height = min(wall_height * 2, constants.SCREEN_HEIGHT * 2)

                # Determine color based on tile type
                color = self._get_wall_color(hit_tile, hit_side, distance)

                strip = WallStrip(
                    x=i * 2,  # Every 2 pixels
                    height=wall_height,
                    color=color,
                    is_door=(hit_tile == "door"),
                )
                self.wall_strips.append(strip)

        return self.wall_strips

    def _cast_ray(
        self,
        start_x: float,
        start_y: float,
        dir_x: float,
        dir_y: float,
        tilemap,
    ) -> Tuple[float, str, int]:
        """Cast a single ray and find wall hit.

        Args:
            start_x: Starting X position.
            start_y: Starting Y position.
            dir_x: Ray direction X.
            dir_y: Ray direction Y.
            tilemap: The tile map.

        Returns:
            Tuple of (distance, tile_type, side).
        """
        # DDA algorithm for raycasting
        map_x = int(start_x / constants.TILE_SIZE)
        map_y = int(start_y / constants.TILE_SIZE)

        # Length of ray from one x or y-side to next x or y-side
        if dir_x == 0:
            delta_dist_x = 1e30
        else:
            delta_dist_x = abs(1 / dir_x)

        if dir_y == 0:
            delta_dist_y = 1e30
        else:
            delta_dist_y = abs(1 / dir_y)

        # Step direction and initial side distances
        step_x = 1 if dir_x >= 0 else -1
        if dir_x >= 0:
            if dir_x == 0:
                side_dist_x = 1e30
            else:
                side_dist_x = ((map_x + 1) * constants.TILE_SIZE - start_x) / dir_x
        else:
            side_dist_x = (
                (start_x - map_x * constants.TILE_SIZE) / abs(dir_x) if dir_x != 0 else 1e30
            )

        step_y = 1 if dir_y >= 0 else -1
        if dir_y >= 0:
            if dir_y == 0:
                side_dist_y = 1e30
            else:
                # Moving down (increasing Y) - next row is map_y + 1
                side_dist_y = ((map_y + 1) * constants.TILE_SIZE - start_y) / dir_y
        else:
            # Moving up (decreasing Y in screen) - next row is map_y
            side_dist_y = (
                (start_y - map_y * constants.TILE_SIZE) / abs(dir_y) if dir_y != 0 else 1e30
            )

        # DDA loop
        hit = False
        side = 0
        while not hit:
            # Jump to next map square
            if side_dist_x < side_dist_y:
                side_dist_x += delta_dist_x
                map_x += step_x
                side = 0
            else:
                side_dist_y += delta_dist_y
                map_y += step_y
                side = 1

            # Check bounds
            if map_x < 0 or map_x >= tilemap.width or map_y < 0 or map_y >= tilemap.height:
                hit = True
                continue

            # Check if we hit a wall
            tile = tilemap.get_tile(map_x, map_y)
            if tile == "wall" or tile == "door":
                hit = True

        # Calculate distance
        if side == 0:
            distance = (map_x - start_x / constants.TILE_SIZE + (1 - step_x) / 2) / dir_x
        else:
            distance = (map_y - start_y / constants.TILE_SIZE + (1 - step_y) / 2) / dir_y

        distance *= constants.TILE_SIZE

        # Get tile type
        if map_x >= 0 and map_x < tilemap.width and map_y >= 0 and map_y < tilemap.height:
            tile = tilemap.get_tile(map_x, map_y)
        else:
            tile = "wall"

        return distance, tile, side

    def _get_wall_color(self, tile: str, side: int, distance: float) -> pygame.Color:
        """Get wall color with shading based on distance and side.

        Args:
            tile: Tile type.
            side: Which side was hit (0 = x, 1 = y).
            distance: Distance to wall.

        Returns:
            Color with shading applied.
        """
        # Base colors
        base_colors = {
            "wall": (100, 100, 100),  # Gray walls
            "door": (100, 100, 200),  # Blue doors
        }

        base_color = base_colors.get(tile, (100, 100, 100))

        # Apply side shading (y-side is darker)
        if side == 1:
            base_color = tuple(max(0, c - 30) for c in base_color)

        # Apply distance shading (farther = darker)
        max_dist = self.max_depth
        shade_factor = max(0.3, 1.0 - (distance / max_dist) * 0.7)
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
    # Draw ceiling (dark gray gradient)
    ceiling_color = (30, 30, 30)
    ceiling_rect = pygame.Rect(0, 0, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT // 2)
    pygame.draw.rect(screen, ceiling_color, ceiling_rect)

    # Draw floor (darker with gradient effect)
    floor_color = (20, 20, 20)
    floor_rect = pygame.Rect(
        0, constants.SCREEN_HEIGHT // 2, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT // 2
    )
    pygame.draw.rect(screen, floor_color, floor_rect)

    # Draw floor line
    pygame.draw.line(
        screen,
        (40, 40, 40),
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

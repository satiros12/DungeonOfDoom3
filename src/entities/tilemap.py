"""TileMap entity for managing the game world grid."""

import logging
from typing import List

from src.core import constants


class TileMap:
    """Manages the tile grid for collision and rendering."""

    def __init__(self, tiles: List[List[str]], width: int, height: int) -> None:
        """Initialize the tilemap.

        Args:
            tiles: 2D list of tile types.
            width: Number of columns in the map.
            height: Number of rows in the map.
        """
        self.tiles = tiles
        self.width = width
        self.height = height
        logging.debug(f"TileMap initialized: {width}x{height}")

    def is_wall(self, col: int, row: int) -> bool:
        """Check if a tile is a wall.

        Args:
            col: Column index.
            row: Row index.

        Returns:
            True if the tile is a wall, False otherwise.
        """
        if not self._is_valid_tile(col, row):
            return True  # Out of bounds is considered a wall
        return self.tiles[row][col] == "wall"

    def is_empty(self, col: int, row: int) -> bool:
        """Check if a tile is empty (floor).

        Args:
            col: Column index.
            row: Row index.

        Returns:
            True if the tile is empty/floor, False otherwise.
        """
        if not self._is_valid_tile(col, row):
            return False
        tile_type = self.tiles[row][col]
        return tile_type in ("floor", "decoration")

    def get_tile(self, col: int, row: int) -> str:
        """Get the tile type at the given position.

        Args:
            col: Column index.
            row: Row index.

        Returns:
            The tile type string.
        """
        if not self._is_valid_tile(col, row):
            return "wall"
        return self.tiles[row][col]

    def _is_valid_tile(self, col: int, row: int) -> bool:
        """Check if the coordinates are within map bounds.

        Args:
            col: Column index.
            row: Row index.

        Returns:
            True if the coordinates are valid, False otherwise.
        """
        return 0 <= col < self.width and 0 <= row < self.height

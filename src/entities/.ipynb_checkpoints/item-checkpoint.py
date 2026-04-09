"""Item entities for Escape the Dungeon of Doom."""

import logging
from dataclasses import dataclass
from enum import Enum
from typing import Optional

import pygame

from src.entities.weapon import Weapon
from src.entities.armor import Armor


class ItemType(Enum):
    """Types of items that can be picked up."""

    WEAPON = "weapon"
    ARMOR = "armor"


@dataclass
class Item:
    """Item that can be picked up or dropped.

    Attributes:
        item_type: Type of item (WEAPON or ARMOR).
        position: Position in world coordinates.
        weapon: Weapon instance (if type is WEAPON).
        armor: Armor instance (if type is ARMOR).
    """

    item_type: ItemType
    position: pygame.Vector2
    weapon: Optional[Weapon] = None
    armor: Optional[Armor] = None

    def __init__(
        self,
        item_type: ItemType,
        position: pygame.Vector2,
        weapon: Optional[Weapon] = None,
        armor: Optional[Armor] = None,
    ) -> None:
        """Initialize an item.

        Args:
            item_type: Type of item.
            position: Position in world coordinates.
            weapon: Weapon instance (if item_type is WEAPON).
            armor: Armor instance (if item_type is ARMOR).
        """
        self.item_type = item_type
        self.position = position
        self.weapon = weapon
        self.armor = armor

        item_name = self.get_name()
        logging.debug(f"Item created: {item_name} at {position}")

    def get_name(self) -> str:
        """Get the display name of the item.

        Returns:
            Name of the item.
        """
        if self.item_type == ItemType.WEAPON and self.weapon:
            return self.weapon.name
        elif self.item_type == ItemType.ARMOR and self.armor:
            return self.armor.name
        return "Unknown Item"

    def equip(self, player: "Player") -> None:
        """Equip the item to a player.

        Args:
            player: The player to equip the item to.
        """
        if self.item_type == ItemType.WEAPON and self.weapon:
            player.equip_weapon(self.weapon)
            logging.info(f"Equipped weapon: {self.weapon.name}")
        elif self.item_type == ItemType.ARMOR and self.armor:
            player.equip_armor(self.armor)
            logging.info(f"Equipped armor: {self.armor.name}")

    def drop(self) -> None:
        """Drop the item (simply logs the action)."""
        logging.info(f"Dropped item: {self.get_name()}")


# Forward reference for type hint
from src.entities.player import Player

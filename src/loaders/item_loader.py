"""Item loader for Escape the Dungeon of Doom."""

import json
import logging
from pathlib import Path
from typing import List

import pygame

from src.entities.item import Item, ItemType
from src.entities.weapon import Weapon
from src.entities.armor import Armor


def load_items(level_number: int) -> List[Item]:
    """Load items for a specific level from JSON file.

    Args:
        level_number: The level number to load items for (1-5).

    Returns:
        List of Item instances for the level.
    """
    items = []
    data_path = Path("data/items")

    # Try to load level-specific items
    level_file = data_path / f"level_{level_number}.json"

    if not level_file.exists():
        logging.debug(f"No items file found for level {level_number}")
        return items

    try:
        with open(level_file, "r") as f:
            data = json.load(f)

        for item_data in data:
            position = pygame.Vector2(
                item_data["position"][0] * 16,  # TILE_SIZE
                item_data["position"][1] * 16,
            )
            item_type = item_data.get("type", "weapon")

            if item_type == "weapon":
                weapon_type = item_data.get("weapon", "fists")
                weapon = Weapon.create_weapon(weapon_type)
                item = Item(
                    item_type=ItemType.WEAPON,
                    position=position,
                    weapon=weapon,
                )
                items.append(item)
                logging.debug(f"Loaded weapon item: {weapon_type}")

            elif item_type == "armor":
                armor_type = item_data.get("armor", "none")
                armor = Armor.create_armor(armor_type)
                item = Item(
                    item_type=ItemType.ARMOR,
                    position=position,
                    armor=armor,
                )
                items.append(item)
                logging.debug(f"Loaded armor item: {armor_type}")

        logging.info(f"Loaded {len(items)} items for level {level_number}")

    except (json.JSONDecodeError, KeyError) as e:
        logging.error(f"Error loading items from {level_file}: {e}")

    return items

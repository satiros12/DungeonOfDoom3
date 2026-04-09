"""Armor entities for Escape the Dungeon of Doom."""

import logging
from dataclasses import dataclass

from src.core import constants


@dataclass
class Armor:
    """Armor with damage reduction and speed characteristics.

    Attributes:
        name: Display name of the armor.
        damage_reduction: Damage multiplier (1.0=no reduction, 0.5=50% reduction).
        speed_multiplier: Speed modifier for movement.
    """

    name: str
    damage_reduction: float
    speed_multiplier: float

    def __init__(
        self,
        name: str,
        damage_reduction: float,
        speed_multiplier: float,
    ) -> None:
        """Initialize an armor.

        Args:
            name: Display name of the armor.
            damage_reduction: Damage reduction multiplier (0-1).
            speed_multiplier: Speed modifier for movement.
        """
        self.name = name
        self.damage_reduction = damage_reduction
        self.speed_multiplier = speed_multiplier
        logging.debug(
            f"Armor created: {name} (reduction: {damage_reduction}, speed: {speed_multiplier})"
        )

    @staticmethod
    def create_armor(armor_type: str) -> "Armor":
        """Create an armor from a predefined type.

        Args:
            armor_type: Type of armor ("none", "light", "medium", "heavy").

        Returns:
            Armor instance.
        """
        armor_data = constants.ARMORS.get(armor_type, constants.ARMORS["none"])
        display_name = constants.ARMOR_NAMES.get(armor_type, "None")
        return Armor(
            name=display_name,
            damage_reduction=armor_data["damage_reduction"],
            speed_multiplier=armor_data["speed_multiplier"],
        )


# Predefined armors
NO_ARMOR = Armor.create_armor("none")
LIGHT_ARMOR = Armor.create_armor("light")
MEDIUM_ARMOR = Armor.create_armor("medium")
HEAVY_ARMOR = Armor.create_armor("heavy")

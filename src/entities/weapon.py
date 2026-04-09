"""Weapon entities for Escape the Dungeon of Doom."""

import logging
from dataclasses import dataclass
from typing import Optional

from src.core import constants


@dataclass
class Weapon:
    """Weapon with damage and speed characteristics.

    Attributes:
        name: Display name of the weapon.
        damage_percent: Damage multiplier (10=10%, 25=25%, etc.).
        speed_multiplier: Speed modifier for attack cooldown.
    """

    name: str
    damage_percent: float
    speed_multiplier: float

    def __init__(
        self,
        name: str,
        damage_percent: float,
        speed_multiplier: float,
    ) -> None:
        """Initialize a weapon.

        Args:
            name: Display name of the weapon.
            damage_percent: Damage percentage (0-100).
            speed_multiplier: Speed modifier for attacks.
        """
        self.name = name
        self.damage_percent = damage_percent
        self.speed_multiplier = speed_multiplier
        logging.debug(
            f"Weapon created: {name} (damage: {damage_percent}%, speed: {speed_multiplier})"
        )

    @staticmethod
    def create_weapon(weapon_type: str) -> "Weapon":
        """Create a weapon from a predefined type.

        Args:
            weapon_type: Type of weapon ("fists", "sword", "axe", "hammer").

        Returns:
            Weapon instance.
        """
        weapon_data = constants.WEAPONS.get(weapon_type, constants.WEAPONS["fists"])
        display_name = constants.WEAPON_NAMES.get(weapon_type, "Fists")
        return Weapon(
            name=display_name,
            damage_percent=weapon_data["damage_percent"],
            speed_multiplier=weapon_data["speed_multiplier"],
        )


# Predefined weapons
FISTS = Weapon.create_weapon("fists")
SWORD = Weapon.create_weapon("sword")
AXE = Weapon.create_weapon("axe")
HAMMER = Weapon.create_weapon("hammer")

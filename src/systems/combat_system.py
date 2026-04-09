"""Combat system for Escape the Dungeon of Doom."""

import logging
import math
from dataclasses import dataclass, field
from typing import Optional

import pygame

from src.core import constants
from src.entities.weapon import Weapon
from src.entities.armor import Armor
from src.entities.player import Player
from src.entities.enemy import Enemy


@dataclass
class CombatSystem:
    """System for handling combat between player and enemies."""

    def calculate_damage(
        self,
        weapon: Weapon,
        armor: Armor,
        is_backstab: bool = False,
    ) -> float:
        """Calculate damage based on weapon and armor.

        The formula is: damage = damage_weapon * damage_reduction

        Args:
            weapon: The weapon used in the attack.
            armor: The armor being attacked.
            is_backstab: Whether the attack is from behind.

        Returns:
            Calculated damage amount.
        """
        # Base damage from weapon (percentage)
        base_damage = weapon.damage_percent  # Already in percent (10, 25, 40, 70)

        # Armor reduction multiplier (from constants.py)
        # none: 1.0 (100% damage), light: 0.75, medium: 0.5, heavy: 0.25
        reduction = armor.damage_reduction

        # Calculate damage
        damage = base_damage * reduction

        # Add backstab bonus
        if is_backstab:
            damage *= 1.0 + constants.BACKSTAB_DAMAGE_BONUS
            logging.debug(
                f"Backstab bonus applied: {constants.BACKSTAB_DAMAGE_BONUS * 100}%"
            )

        logging.debug(
            f"Calculated damage: {damage} (weapon: {base_damage}, reduction: {reduction})"
        )
        return damage

    def can_attack(self, player: Player) -> bool:
        """Check if player can attack (cooldown).

        Args:
            player: The player attempting to attack.

        Returns:
            True if attack is available, False otherwise.
        """
        if not hasattr(player, "_last_attack_time"):
            player._last_attack_time = 0.0

        import time

        current_time = time.time()

        # Calculate cooldown based on weapon speed
        cooldown = player.weapon.speed_multiplier if player.weapon else 1.0

        # Minimum cooldown between attacks
        min_cooldown = 0.5 / max(cooldown, 0.1)  # At least 0.5s base

        if current_time - player._last_attack_time >= min_cooldown:
            return True
        return False

    def is_backstab(self, player: Player, enemy: Enemy) -> bool:
        """Check if attack is a backstab (from behind).

        Args:
            player: The player attacking.
            enemy: The enemy being attacked.

        Returns:
            True if attack is from behind, False otherwise.
        """
        if not player or not enemy:
            return False

        # Get angle from player to enemy
        direction = enemy.position - player.position
        if direction.length() == 0:
            return False

        direction = direction.normalize()

        # Get enemy's facing direction
        enemy_angle_rad = math.radians(enemy.rotation - 90)
        enemy_direction = pygame.Vector2(
            math.cos(enemy_angle_rad),
            math.sin(enemy_angle_rad),
        )

        # Calculate angle between player direction and enemy facing
        # If they're facing opposite directions, it's a backstab
        dot_product = direction.dot(enemy_direction)

        # If enemy is facing away (dot < 0), it's a backstab
        # dot < -0.3 means enemy is mostly facing away
        is_behind = dot_product < -0.3

        logging.debug(f"Backstab check: dot={dot_product}, is_backstab={is_behind}")
        return is_behind

    def dodge_window(self, enemy: Enemy) -> bool:
        """Check if enemy is in dodge window (after attacking).

        Args:
            enemy: The enemy to check.

        Returns:
            True if enemy is in dodge window, False otherwise.
        """
        if not hasattr(enemy, "_last_attack_time"):
            return False

        import time

        current_time = time.time()
        time_since_attack = current_time - enemy._last_attack_time

        # Dodge window is 0.3s after attacking
        in_dodge = time_since_attack < constants.DODGE_WINDOW

        logging.debug(f"Dodge window: {in_dodge} (time: {time_since_attack:.2f}s)")
        return in_dodge

    def player_attack(
        self,
        player: Player,
        enemies: list[Enemy],
    ) -> Optional[Enemy]:
        """Process player attack action.

        Args:
            player: The player attacking.
            enemies: List of enemies to check for hits.

        Returns:
            The enemy hit by the attack, or None if no hit.
        """
        if not self.can_attack(player):
            return None

        # Find closest enemy in range
        closest_enemy = None
        closest_distance = float("inf")

        for enemy in enemies:
            if not enemy.is_alive():
                continue

            distance = (enemy.position - player.position).length()
            if distance <= constants.TILE_SIZE:  # 1 tile range
                if distance < closest_distance:
                    closest_distance = distance
                    closest_enemy = enemy

        if closest_enemy:
            # Calculate damage
            is_backstab = self.is_backstab(player, closest_enemy)
            weapon = player.weapon
            armor = closest_enemy.armor

            damage = self.calculate_damage(weapon, armor, is_backstab)

            # Apply damage
            closest_enemy.take_damage(damage)

            # Update attack time
            import time

            player._last_attack_time = time.time()

            logging.info(
                f"Player attacked {closest_enemy.enemy_type}: "
                f"damage={damage:.1f}, backstab={is_backstab}"
            )

            return closest_enemy

        return None

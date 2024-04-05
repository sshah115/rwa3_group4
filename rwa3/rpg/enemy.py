from abc import ABC, abstractmethod
import rpg.player 
"""
This file contains the Enemy class.

Author: Sajjadul Yasin
Email: yasin@umd.edu
"""

class Enemy(ABC):
    """
    A class representing an enemy in the game.

    Attributes:
        name (str): The name of the enemy.
        health (int): The health of the enemy.
    """

    def __init__(self, position, name, health, attack_power = 20): # ToDo: Attack power shall be dynamic with the YAML file
        self._position = position
        self._name = name
        self._health = health
        self._attack_power = attack_power
        
    @abstractmethod
    def attack(self, player: rpg.player.Player, damage):
        """
        Attack the player.

        Args:
            player (Player): The player to attack.
            damage (int): The amount of damage to deal.
        """
        pass

    @abstractmethod
    def take_damage(self, damage):
        """
        Take damage from the player.

        Args:
            damage (int): The amount of damage to take.
        """
        pass




class Skeleton(Enemy):
    """
    A class representing a skeleton enemy in the game. All skeletons have a shield power. The health of a skeleton is 50.
    
    Attributes:
        shield_power (int): The power of the skeleton's shield.
    """

    def __init__(self, name, health, position, shield_power):
        super().__init__(name=name, health=health, position=position)
        self._shield_power = shield_power


    def attack(self, player: rpg.player.Player, damage):
        """
        Attack the player.

        Args:
            player (Player): The player to attack.
            damage (int): The amount of damage to deal.
        """
        print(f"🧟🗡️ {self._name} attacks {player.name}!")
        player.take_damage(damage)

    def take_damage(self, damage):
        """
        Take damage from the player.

        Args:
            damage (int): The amount of damage to take.
        """
        # super().take_damage(damage - self._shield_power)

        # Shield power reduces total damage
        damage -= self._shield_power
        self._health -= damage
        if self._health <= 0:
            print(f"🧟💀 {self._name} has been defeated!")
        else:
            print(f"🧟💜 {self._name} has {self._health} health left.")
        
class Dragon(Enemy):
    """
    A class representing a dragon enemy in the game. All dragons have a fire breath power. The health of a dragon is 200.
    
    Attributes:
        fire_breath_power (int): The power of the dragon's fire breath.
    """

    def __init__(self, name, health, position, fire_breath_power):
        super().__init__(name=name, health=health, position=position)
        self._fire_breath_power = fire_breath_power


    def attack(self, player: rpg.player.Player, damage):
        """
        Attack the player.

        Args:
            player (Player): The player to attack.
            damage (int): The amount of damage to deal.
        """
        print(f"🧟🗡️ {self._name} attacks {player.name}!")
        player.take_damage(damage + self._fire_breath_power)

    def take_damage(self, damage):
        """
        Take damage from the player.

        Args:
            damage (int): The amount of damage to take.
        """
        self._health -= damage
        if self._health <= 0:
            print(f"🧟💀 {self._name} has been defeated!")
        else:
            print(f"🧟💜 {self._name} has {self._health} health left.")
 
        
if __name__ == "__main__":
    print("Creating an enemy:")
    enemy = Enemy()
    enemy.attack(rpg.player.Player(), 10)
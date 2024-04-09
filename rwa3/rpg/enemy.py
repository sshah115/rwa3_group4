import yaml
import random

from rpg.maze import file_path
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

    @property
    def attack_power(self):
        return self._attack_power
    
    @property
    def position(self):
        return self._position
        
    @abstractmethod
    def attack(self, player, damage):
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

    def extract_enemy(self, position):
        """
        Extract enemy data from the YAML file.

        Args:
            position (list): positional index of enemy
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


    def attack(self, player, damage):
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


    def extract_enemy(self, position):
        """
        Extract enemy data from the YAML file.
        """

        with open(file_path, "r") as file:
            try:
                data = yaml.safe_load(file)
                # Retrieve the enemies: dragons
                for enemy_data in data["maze"]["enemies"]["skeletons"]:
                    if position == enemy_data["skeleton"]["position"]:
                        return Skeleton(enemy_data["skeleton"]["health"], enemy_data["skeleton"]["position"],enemy_data["skeleton"]["shield_power"])
                
            except yaml.YAMLError as e:
                print(f"Error parsing YAML file: {e}")
        pass
        
class Dragon(Enemy):
    """
    A class representing a dragon enemy in the game. All dragons have a fire breath power. The health of a dragon is 200.
    
    Attributes:
        fire_breath_power (int): The power of the dragon's fire breath.
    """

    def __init__(self, name, health, position, fire_breath_power):
        super().__init__(name=name, health=health, position=position)
        self._fire_breath_power = fire_breath_power


    def attack(self, player, damage):
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

    def extract_enemy(self, position):
        """
        Extract enemy data from the YAML file.
        """

        with open(file_path, "r") as file:
            try:
                data = yaml.safe_load(file)
                # Retrieve the enemies: dragons
                for enemy_data in data["maze"]["enemies"]["dragons"]:
                    if position == enemy_data["dragon"]["position"]:
                        return Skeleton(enemy_data["dragon"]["health"], enemy_data["dragon"]["position"],enemy_data["dragon"]["fire_power"])
                
            except yaml.YAMLError as e:
                print(f"Error parsing YAML file: {e}")
        pass








 
    # Tagged for removal.
    # def extract_enemies(self, file_path):
    #     """
    #     Extract enemy data from the YAML file.
    #     """
    #     _file_path = file_path
        
    #     # Following two dictionaries needs to be global. Set to local as temp.
    #     dragons_dict = {} 
    #     skeletons_dict = {}

    #     with open(self._file_path, "r") as file:
    #         try:
    #             data = yaml.safe_load(file)
    #             # Retrieve the enemies: dragons
    #             for dragon_data in data["maze"]["enemies"]["dragons"]:
    #                 position = tuple(dragon_data["dragon"]["position"])
    #                 # Add following line in maze.extract_enemies
    #                 dragons_dict[position] = Dragon(dragon_data["dragon"]["health"], dragon_data["dragon"]["position"], dragon_data["dragon"]["fire_power"])

    #             # Retrieve the enemies: skeletons
    #             for skeleton_data in data["maze"]["enemies"]["skeletons"]:
    #                 position = tuple(skeleton_data["skeleton"]["position"])
    #                 # Add following line in maze.extract_enemies
    #                 skeletons_dict[position] = Skeleton(skeleton_data["skeleton"]["health"], skeleton_data["skeleton"]["position"],skeleton_data["skeleton"]["shield_power"])
                    
    #         except yaml.YAMLError as e:
    #             print(f"Error parsing YAML file: {e}")

    # New implementation for enemy extraction




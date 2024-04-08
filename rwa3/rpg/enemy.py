
import sys
import os.path
import random
folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(folder)
file_path = os.path.join(folder, "rpg", "config.yaml")
import yaml
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
 
    # Recommend this in the maze.extract_enemies() method to prevent duplicate codes and code complexities. Design level issue.
    def extract_enemies(self, file_path):
        """
        Extract enemy data from the YAML file.
        """
        _file_path = file_path
        
        # Following two dictionaries needs to be global. Set to local as temp.
        dragons_dict = {} 
        skeletons_dict = {}

        with open(self._file_path, "r") as file:
            try:
                data = yaml.safe_load(file)
                # Retrieve the enemies: dragons
                for dragon_data in data["maze"]["enemies"]["dragons"]:
                    position = tuple(dragon_data["dragon"]["position"])
                    # Add following line in maze.extract_enemies
                    dragons_dict[position] = Dragon(dragon_data["dragon"]["health"], dragon_data["dragon"]["position"], dragon_data["dragon"]["fire_power"])

                # Retrieve the enemies: skeletons
                for skeleton_data in data["maze"]["enemies"]["skeletons"]:
                    position = tuple(skeleton_data["skeleton"]["position"])
                    # Add following line in maze.extract_enemies
                    skeletons_dict[position] = Skeleton(skeleton_data["skeleton"]["health"], skeleton_data["skeleton"]["position"],skeleton_data["skeleton"]["shield_power"])
                    
            except yaml.YAMLError as e:
                print(f"Error parsing YAML file: {e}")


    # Recommended this in Player class. Design issue
    def combat(self, player: rpg.player.Player, enemy:rpg.enemy.Enemy):
        game_action = [player.attack, enemy.attack]
        
        while player.health > 0 or enemy.health > 0:
            action = random.choice(game_action)
            if action == player.attack:
                action(enemy, player.attack_power) # Player class needs to have attack power as property / Provide getter method
                if enemy.health <= 0: 
                    # Instead of changing the values in YAML file I want to update following variables in maze.py so that maze will remove the defeated enemy postion
                    # if isinstance(enemy, Dragon):
                    #     self._dragon_positions.remove(tuple(enemy.position))
                    # elif isinstance(enemy, Skeleton):
                    #     self._skeleton_positions.remove(tuple(enemy.position))

                    print("Enemy was defeated.")
            elif action == enemy.attack:
                action(player, enemy.attack_power)
                if player.health <= 0:
                    print("Player was defeated. Game Over!")
                    # Don't know if i should remove the player from the maze as well??
                    exit()
            else:
                print("Invalid action")
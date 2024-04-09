"""
This file contains the Player class.

Author  : Shail Kiritkumar Shah
Email   : sshah115@umd.edu
"""

import random
# # For testing
# import sys
# import os.path

# Importing reqired modules
import yaml
# from rpg.item import Item
import rpg.enemy
import rpg.item as item
from rpg.maze import file_path  # noqa: E402
from enum import Enum, auto
# folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# sys.path.append(folder)
# file_path = os.path.join(folder, "rpg", "config.yaml")

class Direction(Enum):
    
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"
    

class Player:
    """
    _summary_
    """

    # Sajjad
    def __init__(self, name, health, position, direction: Direction, attack_power, inventory={}):
        """_summary_

        Args:
            name (_type_): _description_
            health (_type_): _description_
            inventory (_type_): _description_
            position (_type_): _description_
            direction (_type_): _description_
            attack_power (_type_): _description_
        """

        self._name = name
        self._health = health
        self._inventory = inventory
        self._position = position
        self._direction = direction
        self._attack_power = attack_power
    
    # Sajjad
    @classmethod
    def extract_player(cls):
        """
        to load the default values from yaml file to class attributes
        """
        with open(file_path, "r") as file:
            try:
                data = yaml.safe_load(file)
                player = data["maze"]["player"]
                return Player(player["name"],player["health"], player["position"], Direction(player["direction"]), player["attack_power"])
            except yaml.YAMLError as e:
                print(f"Error parsing YAML file: {e}")

    # Sajjad
    @classmethod
    def start(cls, player, maze):

        print("*"*34 + "\n*** Welcome to the Maze Game! ***")
        while True:
            print("*"*34 + "\nw - move forward \
                                    \ns - move backward \
                                    \nd - rotate right \
                                    \na - rotate left \
                                    \ni - print inventory \
                                    \nk - use arrow \
                                    \np - print status of the player \
                                    \nq - quit")
            action = input("*"*34 + "\nEnter a command: ")
            
            # Ctrl-c to stop the program
            if action == "p":
                print(f"🤴 Arthur has {self._health} health.")
            elif action == "i":
                print("*"*45 + f"\nArthur's inventory: {maze.key_emoji} x {player._inventory.get([item.Category.KEY], 0)}, {maze.arrow_emoji} x {player._inventory.get([item.Category.ARROW], 0)}, {maze.gem_emoji} x {player._inventory.get([item.Category.GEM], 0)}\n" + "*"*45)
                maze.print_maze()
            elif action in  ('w', 's', 'd', 'a'):
                player.move(action)
                maze.print_maze()
            else:
                print(f"Invalid command, please try again.")

        pass

    def print_inventory(self):
        """
        _summary_
        """
        print(f"{self._name}'s inventory: {self._inventory}")

        
    def move(self, action):
        """
        _summary_
        """
        if action == "w":
            if self._direction == Direction.up:
                self.maze._grid[self.maze._player_position[0]][self.maze._player_position[1]] = "  "
                self.maze._player_position = (self.maze._player_position[0]-1, self.maze._player_position[1])
                self.maze.spawn_player()
            elif self._direction == Direction.left:
                self.maze._grid[self.maze._player_position[0]][self.maze._player_position[1]] = "  "
                self.maze._player_position = (self.maze._player_position[0], self.maze._player_position[1]-1)
                self.maze.spawn_player()
            elif self._direction == Direction.down:
                self.maze._grid[self.maze._player_position[0]][self.maze._player_position[1]] = "  "
                self.maze._player_position = (self.maze._player_position[0]+1, self.maze._player_position[1])
                self.maze.spawn_player()
            else:
                self.maze._grid[self.maze._player_position[0]][self.maze._player_position[1]] = "  "
                self.maze._player_position = (self.maze._player_position[0], self.maze._player_position[1]+1)
                self.maze.spawn_player()
        if action == "s":
            if self._direction == Direction.up:
                self.maze._grid[self.maze._player_position[0]][self.maze._player_position[1]] = "  "
                self.maze._player_position = (self.maze._player_position[0]+1, self.maze._player_position[1])
                self.maze.spawn_player()
            elif self._direction == Direction.left:
                self.maze._grid[self.maze._player_position[0]][self.maze._player_position[1]] = "  "
                self.maze._player_position = (self.maze._player_position[0], self.maze._player_position[1]+1)
                self.maze.spawn_player()
            elif self._direction == Direction.down:
                self.maze._grid[self.maze._player_position[0]][self.maze._player_position[1]] = "  "
                self.maze._player_position = (self.maze._player_position[0]-1, self.maze._player_position[1])
                self.maze.spawn_player()
            else:
                self.maze._grid[self.maze._player_position[0]][self.maze._player_position[1]] = "  "
                self.maze._player_position = (self.maze._player_position[0], self.maze._player_position[1]-1)
                self.maze.spawn_player()                                   
        elif action == "a":
            self.rotate("left")
            self.maze.spawn_player()
        elif action == "d":
            self.rotate("right")
            self.maze.spawn_player()
            
                
        # elif action == "s":
        #     move_backward()
        # elif action == "a":
        #     turn_left()
        # elif action == "d":
        #     turn_right()
        # # In case user decides to quit the maze game.
        # elif action == "q":
        #     print("Quitting the maze game!!!")
        # # In case user inputs invalid action keyword.
        # else:
        #     print("Invalid action! Please enter a valid action")
        
    def rotate(self, direction):
        if direction == "left":
            if self._direction == Direction.up:
                self._direction = Direction.left
                # print(self._emoji["left"])
                self.maze._player_emoji = self._emoji["left"]
                
            elif self._direction == Direction.left:
                self._direction = Direction.down
                self.maze._player_emoji = self._emoji["down"]
                
            elif self._direction == Direction.down:
                self._direction = Direction.right
                self.maze._player_emoji = self._emoji["right"]
                
            elif self._direction == Direction.right:
                self._direction = Direction.up
                self.maze._player_emoji = self._emoji["up"]
                
        elif direction == "right":  
            if self._direction == Direction.up:
                self._direction = Direction.right
                self.maze._player_emoji = self._emoji["right"]
                
            elif self._direction == Direction.right:
                self._direction = Direction.down
                self.maze._player_emoji = self._emoji["down"]
                
            elif self._direction == Direction.down:
                self._direction = Direction.left
                self.maze._player_emoji = self._emoji["left"]
                
            elif self._direction == Direction.left:
                self._direction = Direction.up
                self.maze._player_emoji = self._emoji["up"]            


    # Sajjad
    def attack(self, enemy: rpg.enemy.Enemy, damage: int):
        """
        Attack the enemy.

        Args:
            enemy (Enemy): The enemy to attack.
            damage (int): The amount of damage to deal.
        """
        print(f"🤴🗡️ {self.name} attacks {enemy.name}!")
        enemy.take_damage(damage)

    # Sajjad
    def defend(self):
        """
        Defend against an attack.
        """
        print(f"🤴🛡️ {self.name} defends!")

    #Sajjad
    def take_damage(self, damage):
        """
        Take damage from an attack.

        Use random to determine if the player will defend or take damage.
        50% chance to defend, 50% chance to take damage.


        Args:
            damage (int): The amount of damage to take.
        """
        
        if random.random() > 0.5:
            self.defend()
        else:
            self.health -= damage
            if self.health <= 0:
                print(f"🤴💀 {self.name} has been defeated!")
            else:
                print(f"🤴💚 {self.name} has {self.health} health left.")


    # Sajjad - If next moving block is non-empty call this function
    def perform_action(self, position):
        """
        Perform an action for next moving block

        Args:
            position (list): Next moving block index. e.g [2, 6]
        """
        if position in self.maze.obstacle_positions:
            pass
        elif position in self.maze.dragon_positions:
            self.combat(self, rpg.enemy.Dragon.extract_enemy(position))
        elif position in self.maze.skeleton_positions:
            self.combat(self, rpg.enemy.Skeleton.extract_enemy(position))
        elif position in self.maze.gem_positions or position in self.maze.key_positions or position in self.maze.arrow_positions or position in self.maze.heart_positions:
            self.pick_up_item(position)
        elif position in self.maze.padlock_positions:
            if self._inventory.get([item.Category.KEY], 0) == 0:
                print("No keys to open lock")
            elif self._inventory.get([item.Category.KEY], 0) > 0:

                #Unlock the padlock
                pass

    # Sajjad
    def pick_up_item(self, position):

        item_emoji = self.maze.grid()[position[0]][position[1]]

        if item_emoji == self.maze.gem_emoji:
            self._inventory[item.Category.GEM] = self._inventory.get([item.Category.GEM], 0) + 1
        elif item_emoji == self.maze.key_emoji:
            self._inventory[item.Category.KEY] = self._inventory.get([item.Category.KEY], 0) + 1
        elif item_emoji == self.maze.arrow_emoji:
            self._inventory[item.Category.ARROW] = self._inventory.get([item.Category.ARROW],0) + 1
        elif item_emoji == self.maze.heart_emoji:
            self._health += item.health_boost


    def open_padlock(self, position):
        pass

    # Sajjad
    def combat(self, player, enemy):
        game_action = [player.attack, enemy.attack]
        
        while player.health > 0 and enemy.health > 0:
            action = random.choice(game_action)
            if action == player.attack:
                action(enemy, player.attack_power) # Player class needs to have attack power as property / Provide getter method
                if enemy.health <= 0: 
                    if isinstance(enemy, Dragon):
                        self.maze.remove_dragon_position(tuple(enemy.position))                        
                    elif isinstance(enemy, Skeleton):
                        self.maze.remove_skeleton_position(tuple(enemy.position))
                    print("Enemy was defeated.")
            elif action == enemy.attack:
                action(player, enemy.attack_power)
                if player.health <= 0:
                    print("Player was defeated. Game Over!")
                    # Don't know if i should remove the player from the maze as well??
                    exit()
            else:
                print("Invalid action")

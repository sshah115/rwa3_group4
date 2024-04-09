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
    _emoji = {}
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
    
    @property
    def name(self):
        return self._name

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
                cls._emoji["up"] = player["emoji_up"]
                cls._emoji["down"] = player["emoji_down"]
                cls._emoji["left"] = player["emoji_left"]
                cls._emoji["right"] = player["emoji_right"]
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
                print("*"*45 + f"\nArthur's inventory: {maze.key_emoji} x {player._inventory.get(item.Category.KEY, 0)}, {maze.arrow_emoji} x {player._inventory.get(item.Category.ARROW, 0)}, {maze.gem_emoji} x {player._inventory.get(item.Category.GEM, 0)}\n" + "*"*45)
                maze.print_maze()
            elif action in  ('w', 's', 'd', 'a'):
                player.move(action, maze)
                maze.print_maze()
            elif action == "k":
                player.use_arrow(maze)
                maze.print_maze()
            else:
                print(f"Invalid command, please try again.")

        pass

    def print_inventory(self):
        """
        _summary_
        """
        print(f"{self._name}'s inventory: {self._inventory}")

        
    def move(self, action, maze):
        """
        _summary_
        """
        if action == "w":
            maze._grid[maze._player_position[0]][maze._player_position[1]] = "  "
            if self._direction == Direction.UP:
                maze._player_position = (maze._player_position[0]-1, maze._player_position[1])
            elif self._direction == Direction.LEFT:
                maze._player_position = (maze._player_position[0], maze._player_position[1]-1)
            elif self._direction == Direction.DOWN:
                maze._player_position = (maze._player_position[0]+1, maze._player_position[1])
            else:
                maze._player_position = (maze._player_position[0], maze._player_position[1]+1)
            maze.spawn_player()
        if action == "s":
            maze._grid[maze._player_position[0]][maze._player_position[1]] = "  "
            if self._direction == Direction.UP:
                maze._player_position = (maze._player_position[0]+1, maze._player_position[1])
            elif self._direction == Direction.LEFT:
                maze._player_position = (maze._player_position[0], maze._player_position[1]+1)
            elif self._direction == Direction.DOWN:
                maze._player_position = (maze._player_position[0]-1, maze._player_position[1])
            else:
                maze._player_position = (maze._player_position[0], maze._player_position[1]-1)
            maze.spawn_player()                                   
        elif action == "a":
            self.rotate("left", maze)
            maze.spawn_player()
        elif action == "d":
            self.rotate("right", maze)
            maze.spawn_player()
            
                
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
        
    def rotate(self, direction, maze):
        if direction == "left":
            if self._direction == Direction.UP:
                self._direction = Direction.LEFT
                # print(self._emoji["left"])
                maze._player_emoji = self._emoji["left"]
                
            elif self._direction == Direction.LEFT:
                self._direction = Direction.DOWN
                maze._player_emoji = self._emoji["down"]
                
            elif self._direction == Direction.DOWN:
                self._direction = Direction.RIGHT
                maze._player_emoji = self._emoji["right"]
                
            elif self._direction == Direction.RIGHT:
                self._direction = Direction.UP
                maze._player_emoji = self._emoji["up"]
                
        elif direction == "right":  
            if self._direction == Direction.UP:
                self._direction = Direction.RIGHT
                maze._player_emoji = self._emoji["right"]
                
            elif self._direction == Direction.RIGHT:
                self._direction = Direction.down
                maze._player_emoji = self._emoji["down"]
                
            elif self._direction == Direction.DOWN:
                self._direction = Direction.LEFT
                maze._player_emoji = self._emoji["left"]
                
            elif self._direction == Direction.LEFT:
                self._direction = Direction.UP
                maze._player_emoji = self._emoji["up"]            


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

    # Carissa 
    # def use_arrow(self,arrows,maze):
    #     """
    #     If player has atleast 1 arrow in inventory,
    #     arrow can be used to shoot up to 3 spaces away.
    #     if an enemy is encountered within 3 spaces of the player, 
    #     enemy will take damage and the arrow will be removed from inventory.  
    #     if no enemy is encountered, arrow is removed from inventory.

    #     Args:
    #         arrows (item class): the arrow item from item.py
    #         maze (maze class): maze containing enemy locations
    #     """
    #     # must have atleast 1 arrow in inventory to use an arrow
    #     # print("qty of arrows: ",self._inventory.get([item.Category.ARROW], 0))
    #     if self._inventory.get([item.Category.ARROW], 0) > 0:
    #         # Assign coeffs for identifying 3 positions arrow will reach
    #         if self._direction == Direction.UP:
    #             i = 0
    #             j = -1
    #         elif self._direction == Direction.DOWN:
    #             i = 0
    #             j = 1
    #         elif self._direction == Direction.LEFT:
    #             i = -1
    #             j = 0
    #         elif self._direction == Direction.RIGHT:
    #             i = 1
    #             j = 0
    #         # print("players current direction: ",self._direction)
    #         # print("players current position: ",self._position[0],",",self._position[1])
    #         arrow_three_blocks = []
    #         for ctr in range(1,4):
    #             arrow_three_blocks.append(tuple(((self._position[0]+(ctr*i)),(self._position[1]+(ctr*j)))))
    #         # print("3 spaces to check for enemies: ",arrow_three_blocks)

    #         for space in arrow_three_blocks:
    #             if space in maze.skeleton_positions:
    #                 self.attack(enemy.skeleton,arrows.item_value)
                    
    #             elif space in maze.dragon_positions:
    #                 self.attack(enemy.dragon,arrows.item_value)

    #         # whether enemy was encountered or not, arrow gets trashed
    #         print("Arrow has been used!")
    #         self.update_inventory(arrows,"remove")
            
    #     # no arrows in inventory. redirect to main menu
    #     else:
    #         self.print_inventory()
    #         print("No arrows in inventory. Cannot use arrows! Try a different action...")

    

    # Sajjad - If next moving block is non-empty call this function
    def perform_action(self, position, maze):
        """
        Perform an action for next moving block

        Args:
            position (list): Next moving block index. e.g [2, 6]
        """
        if position in maze.obstacle_positions:
            pass
        elif position in maze.dragon_positions:
            self.combat(self, rpg.enemy.Dragon.extract_enemy(position))
        elif position in maze.skeleton_positions:
            self.combat(self, rpg.enemy.Skeleton.extract_enemy(position))
        elif position in maze.gem_positions or position in maze.key_positions or position in maze.arrow_positions or position in maze.heart_positions:
            self.pick_up_item(position)
        elif position in maze.padlock_positions:
            # must have atleast 1 key to open a padlock
            if self._inventory.get([item.Category.KEY], 0) == 0:
                print("No keys in inventory to open lock!")
            elif self._inventory.get([item.Category.KEY], 0) > 0:
                # Unlock the padlock
                print("Key from inventory used to open lock!")
                # subtract 1 key from inventory
                self._inventory[item.Category.ARROW] = self._inventory.get(item.Category.ARROW,0) - 1
                # discard padlock
                self.open_padlock(position, maze)
                

    # Sajjad
    def pick_up_item(self, position, maze):

        item_emoji = maze.grid()[position[0]][position[1]]

        if item_emoji == maze.gem_emoji:
            self._inventory[item.Category.GEM] = self._inventory.get(item.Category.GEM, 0) + 1
        elif item_emoji == maze.key_emoji:
            self._inventory[item.Category.KEY] = self._inventory.get(item.Category.KEY, 0) + 1
        elif item_emoji == maze.arrow_emoji:
            self._inventory[item.Category.ARROW] = self._inventory.get(item.Category.ARROW,0) + 1
        elif item_emoji == maze.heart_emoji:
            self._health += item.health_boost


    def open_padlock(self, position, maze):
      maze.remove_padlock_position(position)
    
    # Sajjad - Carrissa
    def use_arrow(self, maze):
        target_position = self._position
        if self._direction == Direction.UP:
            target_position[0] -= 3
        elif self._direction == Direction.DOWN:
            target_position[0] += 3
        elif self._direction == Direction.LEFT:
            #target_position[1] -= 3
            target_position[1] -= 6 # Testing purpose. Run main() > Enter a > Enter k : Should attack the skull
        elif self._direction == Direction.RIGHT:
            target_position[1] += 3

        #ToDo: Validate target is within boundary
        #
        if maze.grid[target_position[0]][target_position[1]] == maze.dragon_emoji:
            enemy = rpg.enemy.Dragon.extract_enemy(target_position)
            self.attack(enemy, item.arrow_damage())
            if enemy.health <= 0:
                maze.remove_dragon_position(enemy.position)
        elif maze.grid[target_position[0]][target_position[1]] == maze.skeleton_emoji:
            enemy = rpg.enemy.Skeleton.extract_enemy(target_position)
            self.attack(enemy, item.arrow_damage())
            if enemy.health <= 0:
                maze.remove_skeleton_position(enemy.position)
        else:
            print(f"Oops!!! No enemy in the target position. Wasted one {maze.arrow_emoji}.")

        self._inventory[item.Category.ARROW] = self._inventory.get(item.Category.ARROW,0) + 1

    # Sajjad
    def combat(self, player, enemy, maze):
        game_action = [player.attack, enemy.attack]
        
        while player.health > 0 and enemy.health > 0:
            action = random.choice(game_action)
            if action == player.attack:
                action(enemy, player.attack_power) # Player class needs to have attack power as property / Provide getter method
                if enemy.health <= 0: 
                    if isinstance(enemy, Dragon):
                        maze.remove_dragon_position(tuple(enemy.position))                        
                    elif isinstance(enemy, Skeleton):
                        maze.remove_skeleton_position(tuple(enemy.position))
                    print("Enemy was defeated.")
            elif action == enemy.attack:
                action(player, enemy.attack_power)
                if player.health <= 0:
                    print("Player was defeated. Game Over!")
                    # Don't know if i should remove the player from the maze as well??
                    exit()
            else:
                print("Invalid action")
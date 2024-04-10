"""
This file contains the Player class.

Author  : Shail Kiritkumar Shah
Email   : sshah115@umd.edu
"""

import random
import copy
# # For testing
import sys
# import os.path

# Importing reqired modules
from enum import Enum
import yaml
import rpg.enemy
import rpg.item as item
from rpg.maze import file_path  # noqa: E402
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

    @property
    def health(self):
        return self._health

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
        """
        Start the command input loop for the user to enter commands to navigate through the maze game

        Args:
            player (Player class): initialize the Arthur player object
            maze (_type_): _description_
        """

        print("*"*34 + "\n*** Welcome to the Maze Game! ***")
        while True:
            print("*"*34 + "\nw - move forward \
                            \ns - move backward \
                            \nd - rotate right \
                            \na - rotate left \
                            \ni - print inventory \
                            \nk - use arrow \
                            \np - print health status of the player \
                            \nq - quit")
            action = input("*"*34 + "\nEnter a command: ")

            # Determine user input
            # TODO need to use getter for _inventory
            if action == "p":
                print(f"🤴 Arthur has {player.health} health.") 
            elif action == "i":
                print("*"*45 + f"\nArthur's inventory: {maze.key_emoji} x {player._inventory.get(item.Category.KEY, 0)}, {maze.arrow_emoji} x {player._inventory.get(item.Category.ARROW, 0)}, {maze.gem_emoji} x {player._inventory.get(item.Category.GEM, 0)}\n" + "*"*45)
                maze.print_maze()
            elif action in  ('w', 's', 'd', 'a'):
                player.move(action, maze)
                maze.print_maze()
            elif action == "k":
                player.use_arrow(maze)
                maze.print_maze()
            elif action == "q":
                print("Player chose to exit game...")
                sys.exit()
            else:
                print(f"Invalid command entered ({action}), please try again.")

    def print_inventory(self):
        """
        Print the player's current inventory
        """
        print(f"{self._name}'s inventory: {self._inventory}")   

    def move(self, action, maze):
        """
        Take the user's specific move action and choose which function to call to execute the action

        Args:
            action (str): w to move forward, s to move backward, a to rotate left, or d to rotate right
            maze (Maze class): current maze 
        """
        if action == "w":
            self.move_forward(maze)
        elif action == "s":
            self.move_backward(maze)
        elif action == "a":
            self.rotate("left", maze)
        elif action == "d":
            self.rotate("right", maze)
            
        maze.spawn_player()       

    def rotate(self, direction, maze):
        """
        Rotate the player right or left in the maze

        Args:
            direction (str): left or right for which direction to rotate
            maze (Maze class): current maze 
        """
        if direction == "left":
            if self._direction == Direction.UP:
                self._direction = Direction.LEFT
                maze.set_player_emoji(self._emoji["left"]) #carissa: changed all of these to public setters instead of accessing non-public attribute
                
            elif self._direction == Direction.LEFT:
                self._direction = Direction.DOWN
                maze.set_player_emoji(self._emoji["down"])
                
            elif self._direction == Direction.DOWN:
                self._direction = Direction.RIGHT
                maze.set_player_emoji(self._emoji["right"])
                
            elif self._direction == Direction.RIGHT:
                self._direction = Direction.UP
                maze.set_player_emoji(self._emoji["up"])
                
        elif direction == "right":  
            if self._direction == Direction.UP:
                self._direction = Direction.RIGHT
                maze.set_player_emoji(self._emoji["right"])
                
            elif self._direction == Direction.RIGHT:
                self._direction = Direction.DOWN
                maze.set_player_emoji(self._emoji["down"])
                
            elif self._direction == Direction.DOWN:
                self._direction = Direction.LEFT
                maze.set_player_emoji(self._emoji["left"])
                
            elif self._direction == Direction.LEFT:
                self._direction = Direction.UP
                maze.set_player_emoji(self._emoji["up"])         

    def move_forward(self, maze):
        """
        Move the player one space forward in player's current direction

        Args:
            maze (Maze class): current maze 
        """
        # TODO Need to use setter for _grid
        new_position = self.calculate_new_position(self._direction, maze)
        if self.is_within_bounds(new_position, maze) and new_position not in maze.obstacle_positions:
            if new_position not in maze.padlock_positions or self._inventory.get(item.Category.KEY, 0) > 0:
                self.perform_action(new_position, maze)
                maze._grid[maze.player_position[0]][maze.player_position[1]] = "  "   # carissa added a getter to maze and called here instead of accessing non-public attr
                maze.set_player_position(new_position)  # carissa added a setter to maze and called here instead of non-public attr# carissa added a getter to maze and called here instead of accessing non-public attr
                
            else:
                self.perform_action(new_position, maze)

    def move_backward(self, maze):
        """
        Move the player one space backward in player's current direction

        Args:
            maze (Maze class): current maze 
        """
        # TODO need to use setter for _grid
        opposite_direction = self.get_opposite_direction(self._direction)
        new_position = self.calculate_new_position(opposite_direction, maze)
        if self.is_within_bounds(new_position, maze) and new_position not in maze.obstacle_positions:
            if new_position not in maze.padlock_positions or self._inventory.get(item.Category.KEY, 0) > 0:
                self.perform_action(new_position, maze)
                maze._grid[maze.player_position[0]][maze.player_position[1]] = "  " # carissa added a getter to maze and called here instead of accessing non-public attr
                maze.set_player_position(new_position)  # carissa added a setter to maze and called here instead of non-public attr# carissa added a getter to maze and called here instead of accessing non-public attr
            elif new_position in maze.padlock_positions:
                self.perform_action(new_position, maze)

    def calculate_new_position(self, direction, maze):
        """
        Determine player's new [x,y] position in the maze based
        on current position and current direction 

        Args:
            direction (Enum Class): Direction type from Direction Enum class
            maze (Maze class): current maze 

        Returns:
            list: player's new position in the maze
        """
        row, col = maze.player_position   # carissa used getter here instead of non-public
        if direction == Direction.UP:
            return (row - 1, col)
        elif direction == Direction.DOWN:
            return (row + 1, col)
        elif direction == Direction.LEFT:
            return (row, col - 1)
        elif direction == Direction.RIGHT:
            return (row, col + 1)

    def is_within_bounds(self, position, maze):
        """
        boundary validation to ensure the player's new position is within the bounds of the maze

        Args:
            position (list): player's position
            maze (Maze class): current maze 

        Returns:
            True/False: whether or not the player is IN BOUNDS or OUT OF BOUNDS. 
        """
        row, col = position
        return 0 <= row < maze._grid_size and 0 <= col < maze._grid_size

    def get_opposite_direction(self, direction):
        """
        Obtain opposite direction of player's current direction for use in move_X functions

        Args:
            direction (from enum class type): player's current direction based on enum class

        Returns:
            direction (from enum class type) corresponding to the opposite of current direction
        """
        if direction == Direction.UP:
            return Direction.DOWN
        elif direction == Direction.DOWN:
            return Direction.UP
        elif direction == Direction.LEFT:
            return Direction.RIGHT
        elif direction == Direction.RIGHT:
            return Direction.LEFT

    # Sajjad
    def attack(self, enemy: rpg.enemy.Enemy, damage: int):
        """
        Attack the enemy.

        Args:
            enemy (Enemy): The enemy to attack.
            damage (int): The amount of damage to deal.
        """
        print(f"🤴🗡️ {self._name} attacks {enemy.name}!")
        enemy.take_damage(damage)

    # Sajjad
    def defend(self):
        """
        Defend against an attack. This function is only called by the take_damage function or the combat function. 
        """
        print(f"🤴🛡️ {self._name} defends!")

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
            self._health -= damage
            if self._health <= 0:
                print(f"🤴💀 {self.name} has been defeated!")
            else:
                print(f"🤴💚 {self.name} has {self._health} health left.")

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
            self.combat(self, rpg.enemy.Dragon.extract_enemy(position), maze)
        elif position in maze.skeleton_positions:
            self.combat(self, rpg.enemy.Skeleton.extract_enemy(position), maze)
        elif position in maze.gem_positions or position in maze.key_positions or position in maze.arrow_positions or position in maze.heart_positions:
            self.pick_up_item(position,maze)
        elif position in maze.padlock_positions:
            # must have atleast 1 key to open a padlock
            if self._inventory.get(item.Category.KEY, 0) == 0:
                print(f"{maze.padlock_emoji} is blocking the path. {maze.key_emoji} needed.")
            elif self._inventory.get(item.Category.KEY, 0) > 0:
                # Unlock the padlock
                print("Key from inventory used to open lock!")
                # discard padlock
                self.open_padlock(position, maze)
                # subtract 1 key from inventory
                self._inventory[item.Category.KEY] = self._inventory.get(item.Category.KEY,0) - 1
                
    # Sajjad
    def pick_up_item(self, position, maze):
        """
        Pick up applicable items when player lands on them in the maze space

        Args:
            position (list): player's current position in the maze
            maze (Maze class): current maze 
        """
        # emoji of the item to be picked up
        item_emoji = maze.grid[position[0]][position[1]]
        # gems are collected to inventory
        if item_emoji == maze.gem_emoji:
            self._inventory[item.Category.GEM] = self._inventory.get(item.Category.GEM, 0) + 1
            print("Gem added to inventory!")
        # key's are collected to iventory
        elif item_emoji == maze.key_emoji:
            self._inventory[item.Category.KEY] = self._inventory.get(item.Category.KEY, 0) + 1
            print("Key added to inventory!")
        # arrows are collected to inventory
        elif item_emoji == maze.arrow_emoji:
            self._inventory[item.Category.ARROW] = self._inventory.get(item.Category.ARROW,0) + 1
            print("Arrow added to inventory!")
        # hearts are consumed to increase player health
        elif item_emoji == maze.heart_emoji:
            self._health += item.health_boost
            print("Health boosted!")

    def open_padlock(self, position, maze):
        """
        Open padlocks in the maze, which is basically just removing them from the maze padlock positions list

        Args:
            position (list): position of the padlock to be removed
            maze (Maze class): current maze 
        """
        maze.remove_padlock_position(position)
    
    # Sajjad - Carissa
    def use_arrow(self, maze):
        """
        Use 1 arrow from inventory to shoot up to 3 spaces away at a potential enemy in one of those spaces
        If no enemy is present, arrow is still removed from inventory

        Args:
            maze (Maze class): current maze 
        """
        # can only proceed if have atleast 1 arrow in inventory
        if self._inventory.get(item.Category.ARROW, 0) > 0:            
            # Assign coeffs for identifying 3 positions arrow will reach
            if self._direction == Direction.UP:
                col = 0
                row = -1
            elif self._direction == Direction.DOWN:
                col = 0
                row = 1
            elif self._direction == Direction.LEFT:
                col = -1
                row = 0
            elif self._direction == Direction.RIGHT:
                col = 1
                row = 0
            print("players current direction: ",self._direction)
            print("players current position: ",maze.player_position[0],",",maze.player_position[1])
            arrow_three_blocks = []
            for ctr in range(1,4):
                arrow_three_blocks.append(tuple(((maze.player_position[0]+(ctr*row)),(maze.player_position[1]+(ctr*col)))))
            print("3 spaces to check for enemies: ",arrow_three_blocks)

            for space in arrow_three_blocks:
                # confirm space is in bounds
                if 0 <= space[0] < maze._grid_size and 0 <= space[1] < maze._grid_size:
                    # check if dragon enemy found
                    if maze.grid[space[0]][space[1]] == maze.dragon_emoji:
                        # apply damage if found
                        enemy = rpg.enemy.Dragon.extract_enemy(space)
                        print(item.arrow_damage())
                        self.attack(self, enemy, item.arrow_damage()) # TODO something not working when trying to call this method
                        # remove dragon if defeated
                        if enemy.health <= 0:
                            maze.remove_dragon_position(enemy.position)
                        break
                    elif maze.grid[space[0]][space[1]] == maze.skeleton_emoji:
                        # apply damage if found
                        enemy = rpg.enemy.Skeleton.extract_enemy(space)
                        self.attack(self, enemy, item.arrow_damage()) # TODO something not working when trying to call this method
                        # remove skeleton if defeated
                        if enemy.health <= 0:
                            maze.remove_skeleton_position(enemy.position)
                        break

            # whether enemy was encountered or not, arrow gets trashed
            print("Arrow has been used!")    
            self._inventory[item.Category.ARROW] = self._inventory.get(item.Category.ARROW,0) - 1
        else:
            print(f"Must have atleast 1 {maze.arrow_emoji}  in inventory to use_arrow! Try another command...")

    # Sajjad
    def combat(self, player, enemy, maze):
        # TODO attack issue when trying to run in realtime
        """
        Engage in combat with enemy when encountered in the maze. 
        Random sequence of player attack, player defend, and enemy attack
        will occur until either the enemy or player is defeated. 

        Args:
            player (Player class): the current Arthur player object
            enemy (Skeleton or Dragon class): the enemy encountered in the position of the maze
            maze (Maze class): current maze 
        """
        # Player.defend() method is called at random via the enemy.attack() method (via player.take_damage)
        game_action = [player.attack, enemy.attack]
         
        while player.health > 0 and enemy.health > 0:   # carissa used getter health instead of non-public
            action = random.choice(game_action)
            if action == player.attack:
                action(enemy, player._attack_power) # TODO Player class needs to have attack power as property / Provide getter method
                if enemy.health <= 0: 
                    if isinstance(enemy, rpg.enemy.Dragon):
                        maze.remove_dragon_position(enemy.position)                        
                    elif isinstance(enemy, rpg.enemy.Skeleton):
                        maze.remove_skeleton_position(enemy.position)
                    print("Enemy was defeated.")
            elif action == enemy.attack:
                action(player, enemy.attack_power)
                if player._health <= 0:
                    print("Player was defeated. Game Over!")
                    # Don't know if i should remove the player from the maze as well??
                    sys.exit()
            else:
                print("Invalid action")
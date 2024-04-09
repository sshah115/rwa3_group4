"""
This file contains the Player class with methods to 
create the inventory, update inventory, and use arrows. 

Author  : Cariss Arillo
Email   : carillo@umd.edu
"""
import sys
import os.path

# Importing reqired modules
import yaml
import item as Item
from maze import Maze  # noqa: E402

folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(folder)
file_path = os.path.join(folder, "rpg", "config.yaml")


class Player:
    """
    _summary_
    """

    def __init__(self, config_file) -> None:
        """
        _summary_

        Args:
            name (str, optional): _description_. Defaults to "Hero".
            health (int, optional): _description_. Defaults to 100.
        """
        self._config = config_file
        # attributes
        self._name = None
        self._health = None
        self._inventory = {"ARROW":0, "KEY":0, "GEM":0} # CMA initialized the inventory as all zero quantities
        self._position = None
        self._direction = None
        self._attack_power = None

        self.load_config()
        #self.start()  # CMA commented this out to show how to run use_arrows function

    def load_config(self):
        """
        to load the default values from yaml file to class attributes
        """
        with open(self._config, "r") as file:
            try:
                data = yaml.safe_load(file)
                player_data = data["maze"]["player"]
                self._name = player_data["name"]
                self._health = player_data["health"]
                self._position = player_data["position"]
                self._direction = player_data["direction"]
                self._attack_power = player_data["attack_power"]

            except yaml.YAMLError as e:
                print(f"Error parsing YAML file: {e}")

    def print_inventory(self):
        """
        _summary_
        """
        print(f"{self._name}'s inventory: {self._inventory}")
        
    def update_inventory(self,item,action):
        """
        Update inventory by either adding an arrow, gem or key, or
        removing an arrow, gem, or key

        Args:
            Item (item class):  ARROW, GEM, or KEY
            action (str): "add" or "remove" to update inventory
        """
        if action == "add": 
            ctr = 1
            print("Adding ",item.item_type.name," to inventory")
        else:
            ctr = -1
            print("Removing ",item.item_type.name," from inventory")

        self._inventory[item.item_type.name] = self._inventory[item.item_type.name] + ctr
        self.print_inventory()
            
    def attack(self, enemy, damage):
        """
        _summary_

        Args:
            enemy (_type_): _description_
            damage (_type_): _description_
        """
        print(f"{self.name} attacks {enemy.name}!")
        enemy.take_damage(damage)

    def use_arrow(self,arrows,maze):
        """
        If player has atleast 1 arrow in inventory,
        arrow can be used to shoot up to 3 spaces away.
        if an enemy is encountered within 3 spaces of the player, 
        enemy will take damage and the arrow will be removed from inventory.  
        if no enemy is encountered, arrow is removed from inventory.

        Args:
            arrows (item class): the arrow item from item.py
            maze (maze class): maze containing enemy locations
        """
        # must have atleast 1 arrow in inventory to use an arrow
        if self._inventory["ARROW"] > 0:
            if self._direction == "up":
                i = 0
                j = -1
            elif self._direction == "down":
                i = 0
                j = 1
            elif self._direction == "left":
                i = -1
                j = 0
            elif self._direction == "right":
                i = 1
                j = 0
            # print("players current direction: ",self._direction)
            # print("players current position: ",self._position[0],",",self._position[1])
            arrow_three_blocks = []
            for ctr in range(1,4):
                arrow_three_blocks.append(tuple(((self._position[0]+(ctr*i)),(self._position[1]+(ctr*j)))))
            # print("3 spaces to check for enemies: ",arrow_three_blocks)

            for space in arrow_three_blocks:
                if space in maze.skeleton_positions:
                    self.attack(enemy.skeleton,arrows.item_value)
                    
                elif space in maze.dragon_positions:
                    self.attack(enemy.dragon,arrows.item_value)

            # whether enemy was encountered or not, arrow gets trashed
            print("Arrow has been used!")
            self.update_inventory(arrows,"remove")
            
        # no arrows in inventory. redirect to main menu
        else:
            self.print_inventory()
            print("No arrows in inventory. Cannot use arrows! Try a different action...")

if __name__ == "__main__":
    
    # instantiate maze, player, items for the example
    maze = Maze(file_path)
    player = Player(file_path)
    gems, keys, padlocks, arrows, hearts = Item.make_items(maze)
    
    # player has no arrows so cant run use_arrow...gets redirected back to main menu
    player.use_arrow(arrows,maze)
    
    # player has 1 arrow to start
    player.update_inventory(arrows,"add")
    player.use_arrow(arrows,maze)


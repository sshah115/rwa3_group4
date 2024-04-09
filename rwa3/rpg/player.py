"""
This file contains the Player class.

Author  : Shail Kiritkumar Shah
Email   : sshah115@umd.edu
"""

# # For testing
# import sys
# import os.path

# Importing reqired modules
import yaml
# from rpg.item import Item
import rpg.item as item
from rpg.maze import Maze  # noqa: E402
from enum import Enum, auto
# folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# sys.path.append(folder)
# file_path = os.path.join(folder, "rpg", "config.yaml")

class Direction(Enum):
    
    up = auto()
    down = auto()
    left = auto()
    right = auto()
    

class Player:
    """
    _summary_
    """

    def __init__(self, config_file, maze) -> None:
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
        self._inventory = {}
        self._position = None
        self._direction: Direction
        self._attack_power = None
        self._maze = maze
        self._emoji = {}

        self.load_config()
        self.start()
    
    @property    
    def maze(self):
        return self._maze

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
                direction_str = player_data["direction"]
                self._direction = Direction[direction_str]
                self._attack_power = player_data["attack_power"]
                self._emoji = {"up": player_data["emoji_up"],"down": player_data["emoji_down"],
                "left": player_data["emoji_left"], "right": player_data["emoji_right"]}

            except yaml.YAMLError as e:
                print(f"Error parsing YAML file: {e}")

    def print_inventory(self):
        """
        _summary_
        """
        print(f"{self._name}'s inventory: {self._inventory}")
        
    def start(self):
        """
        _summary_
        """
        # maze = Maze(self._config)
        gems, keys, padlocks, arrows, hearts = item.make_items(self.maze)
        # print("GEMS:\n", gems, "\nKEYS:\n", keys, "\nPADLOCKS:\n", padlocks, "\nARROWS:\n", arrows, "\nHEARTS:\n", hearts) 
        
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
                print("*"*45 + f"\nArthur's inventory: {keys.item_emoji} x 0, {arrows.item_emoji} x 0, {gems.item_emoji} x 0\n" + "*"*45)
                self.maze.print_maze()
            elif action in  ('w', 's', 'd', 'a'):
                self.move(action)
                self.maze.print_maze()
            else:
                print(f"Invalid command, please try again.")
                
            # # To continue the prompt if any other character entered
            # elif action not in ["w", "s", "a", "d"]:
            #     continue
            # # Print the maze after each valid action
            # else:
            #     print_maze()

            # # Check for obstacles or reaching the goal
            # if obstacle_check() or goal_check():
                # break
        
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



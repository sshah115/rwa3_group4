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
from rpg.item import Item
# folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# sys.path.append(folder)
# file_path = os.path.join(folder, "rpg", "config.yaml")


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
        self._inventory = {}
        self._position = None
        self._direction = None
        self._attack_power = None

        self.load_config()
        self.start()

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
        
    def start(self):
        """
        _summary_
        """
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
                print()
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
        pass
        # if action == "w":
        #     if self._direction == "up":
                
                
                
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

    def attack(self, enemy, damage):
        """
        _summary_

        Args:
            enemy (_type_): _description_
            damage (_type_): _description_
        """
        print(f"{self.name} attacks {enemy.name}!")
        enemy.take_damage(damage)

    def defend(self):
        """
        _summary_
        """
        print(f"{self.name} defends!")

    def take_damage(self, damage):
        """
        _summary_

        Args:
            damage (_type_): _description_
        """
        self.health -= damage
        if self.health <= 0:
            print(f"{self.name} has been defeated")
        else:
            print(f"{self.name} has {self.health} health left")


# if __name__ == "__main__":
#     # For testing
#     arthur = Player(file_path)

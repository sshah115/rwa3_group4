import yaml

from rpg.maze import file_path
from dataclasses import dataclass
from enum import Enum, auto

# define category/item class per professors instructions
class Category(Enum):
    """
    Enum class for item category. 
    The auto() method assigns numerical values automatically to the class attributes (items) defined below.
    
    In the game, an item is defined by its category, position, and value. 
    There are five distinct categories of items scattered throughout the maze.

    """
    HEART = auto()      #1
    PADLOCK = auto()    #2
    KEY = auto()        #3
    ARROW = auto()      #4
    GEM = auto()        #5

@dataclass(frozen=True) # none of the attributes can be modified after instantiation
class Item:
    """
    Data class for items in the game
    
    Class Attributes:
    item_type: Category - type of the item
    item_position: list of all positions (As tuples) of the item type in the current maze
    item_value: value associated with that item if applicable (hearts = health amount, arrow = damage amount, other = None)
    """
    item_type: Category
    item_position: list 
    item_value: int
  
def health_boost():
    """
    Extract health boost data from the YAML file.
    """

    with open(file_path, "r") as file:
        try:
            data = yaml.safe_load(file)
            return data["maze"]["items"]["hearts"]["health"]
        except yaml.YAMLError as e:
            print(f"Error parsing YAML file: {e}")
    pass

def arrow_damage():
    """
    Extract arrow damage from the YAML file.
    """

    with open(file_path, "r") as file:
        try:
            data = yaml.safe_load(file)
            return data["maze"]["items"]["arrows"]["damage"]
        except yaml.YAMLError as e:
            print(f"Error parsing YAML file: {e}")
    pass
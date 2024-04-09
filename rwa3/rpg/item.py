import yaml

from rpg.maze import file_path
from dataclasses import dataclass
from enum import Enum, auto

"""
This file contains the Item class.

Author: Carissa Arillo
Email: carillo@umd.edu
"""

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

def get_item(self, maze, position, category):
    """
    Get Item Object
    maze: cls - current instantiation of the maze based on the YAML File
    position: list - item's position in the maze
    categoty: Category - item type


    This is intended to be called whenever a new item was picked up and it requires instantiation.
    
    Returns an instantiation of Item class
    """    
    # Value for arrow is damage (YAML), heart is health (YAML), all other items is None
    value = maze._arrow_damage if category == Category.ARROW else (maze._heart_boost if category == Category.HEART else None)

    return Item(category, position, value)
    
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
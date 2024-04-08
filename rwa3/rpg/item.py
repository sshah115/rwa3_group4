#these lines are needed for item class definitions
from dataclasses import dataclass
from enum import Enum, auto

# these lines are needed to extract from config.yaml
import sys
import os.path
folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(folder)
file_path = os.path.join(folder, "rpg", "config.yaml")
import yaml

# imported this just to try scanning the maze for fun
from rpg.maze import Maze  # noqa: E402

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
    item_emoji: string emoji associated with that item as defined in config.yaml    
    """
    item_type: Category
    item_position: list 
    item_value: int
    item_emoji: str
       
def extract_healthboost(file_path):
    """
    Extract the heart health value from the YAML file.
    _file_path: str - path to yaml file

    This is intended to only be called if the item is a heart
    Returns the config.yaml maze-item-heart-health parameter value
    """
    _file_path = file_path

    with open(_file_path, "r") as file:
        try:
            data = yaml.safe_load(file)
            # Retrieve the heart boost amount for heart items
            heart_boost = data["maze"]["items"]["hearts"]["health"]
            return heart_boost
        except yaml.YAMLError as e:
            print(f"Error parsing YAML file: {e}")

def extract_damage(file_path):
    """
    Extract the arrow damage value from the YAML file.
    _file_path: str - path to yaml file

    This is intended to only be called if the item is an arrow
    Returns the config.yaml maze-item-arrow-damage parameter value
    """
    _file_path = file_path
    with open(_file_path, "r") as file:
        try:
            data = yaml.safe_load(file)
            # Retrieve the arrow damage amount for arrow items
            arrow_damage = data["maze"]["items"]["arrows"]["damage"]
            return arrow_damage
        except yaml.YAMLError as e:
            print(f"Error parsing YAML file: {e}")

def qty_gems(maze):
    """
    Determine the quantity of gems remaining in the maze
    maze: cls - current instantiation of the maze based on the YAML File
    
    This is intended to be called any time the maze is updated to ensure
    the latest quantity of gems remaining in the maze is known 
    
    When there are zero gems remaining, the player has won the game.

    Returns and integer quantity of the remaining gems in the maze
    """
    try:
        quantity = len(maze.gem_positions)
    except:
        quantity = 0
    return quantity
     
def make_items(maze):
    """
    Instantiate all items contained in the maze
    maze: cls - current instantiation of the maze based on the YAML File

    This is intended to be called any time the maze is updated to ensure
    the latest list of existing items are accessible in the maze when the
    player accesses a new location in the maze
    
    Returns an instantiation of each item type with all applicable item information:
    - the item category (type)
    - all of the positions where that item exists in the maze
    - the value associated with that item if applicable (if heart or arrow, else None) 
    - the emoji associated with that item as defined in the YAML file. 
    """    
    # Make all items 
    # for Gems: report how many are still remaining in the maze    
    gems = Item(Category.GEM, maze.gem_positions, qty_gems(maze), maze.gem_emoji)
    keys = Item(Category.KEY, maze.key_positions, None, maze.key_emoji)
    padlocks = Item(Category.PADLOCK, maze.padlock_positions, None, maze.padlock_emoji)
    arrows = Item(Category.ARROW, maze.arrow_positions,extract_damage(file_path), maze.arrow_emoji)
    hearts = Item(Category.HEART, maze.heart_positions,extract_healthboost(file_path), maze.heart_emoji)
    return gems, keys, padlocks, arrows, hearts
              
if __name__ == "__main__":
    
    maze = Maze(file_path)       
    gems, keys, padlocks, arrows, hearts = make_items(maze)
    print("GEMS:\n", gems, "\nKEYS:\n", keys, "\nPADLOCKS:\n", padlocks, "\nARROWS:\n", arrows, "\nHEARTS:\n", hearts) 
    
    # Examples of specific details about an item object
    print("\nItem debugging: ")
    print("Heart Item Object: ",hearts)
    print("Heart Item name: ",hearts.item_type.name)
    print("Heart Item position: ",hearts.item_position)
    print("Heart Item value: ",hearts.item_value)
    print("Heart Item emoji: ",hearts.item_emoji)
    
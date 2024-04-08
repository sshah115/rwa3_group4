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

# item descriptions for fun
# heart_desc = "The player gets a health boost when the player occupies the same cell as a heart. Hearts are not added to the player’s inventory and are automatically consumed."
# padlock_desc = "The player can not open a padlock unless at least one key is in the player’s inventory. To open padlocks, the player must be on the same cell as the padlock and in possession of at least one key."
# key_desc = "Keys are collectible items that are stored in the player’s inventory when picked up. To use a key, the player must be on the same cell as a padlock."
# arrow_desc = "Arrows are collectible items that players can store in their inventory. They are used to attack enemies within a three-tile range from the player, aligning with the player’s direction. Each arrow decreases an enemy’s health. Moreover, arrows are capable of passing solely through green blocks."
# gem_desc = "Gems are collectible items that are stored in the player’s inventory. To complete the game, the player has to collect all three gems dispersed throughout the maze."

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
    # name: str  # not needed right now
    item_type: Category
    # item_desc: str  # not needed right now
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
    gems = Item(Category.GEM, maze._gem_positions, len(maze._gem_positions), maze._gem_emoji)
    keys = Item(Category.KEY, maze._key_positions, None, maze._key_emoji)
    padlocks = Item(Category.PADLOCK, maze._padlock_positions, None, maze._padlock_emoji)
    arrows = Item(Category.ARROW, maze._arrow_positions,extract_damage(file_path), maze._arrow_emoji)
    hearts = Item(Category.HEART, maze._heart_positions,extract_healthboost(file_path), maze._heart_emoji)
    return gems, keys, padlocks, arrows, hearts
              
if __name__ == "__main__":
    
    maze = Maze(file_path)       
    gems, keys, padlocks, arrows, hearts = make_items(maze)
    print("GEMS:\n", gems, "\nKEYS:\n", keys, "\nPADLOCKS:\n", padlocks, "\nARROWS:\n", arrows, "\nHEARTS:\n", hearts) 
    
    # Examples of specific details about an item object
    # print("\nItem debugging: ")
    # print("Heart_item: ",heart_item)
    # print("Heart_item name: ",heart_item.name)
    # print("Heart_item type name: ",heart_item.item_type.name)
    # print("Heart_item type value: ",heart_item.item_type.value)
    # print("Heart_item description: ",heart_item.item_desc)
    # print("Health boost for this heart: ",extract_healthboost(file_path))

    # Example of specific details about a Category object
    # print("\nCategory degugging:")
    # print("Category list: ",list(Category))
    # print("Example HEART enum name: ",Category.HEART.name)
    # print("Example HEART enum value: ",Category.HEART.value)

    
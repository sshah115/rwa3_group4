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
heart_desc = "The player gets a health boost when the player occupies the same cell as a heart. Hearts are not added to the player’s inventory and are automatically consumed."
padlock_desc = "The player can not open a padlock unless at least one key is in the player’s inventory. To open padlocks, the player must be on the same cell as the padlock and in possession of at least one key."
key_desc = "Keys are collectible items that are stored in the player’s inventory when picked up. To use a key, the player must be on the same cell as a padlock."
arrow_desc = "Arrows are collectible items that players can store in their inventory. They are used to attack enemies within a three-tile range from the player, aligning with the player’s direction. Each arrow decreases an enemy’s health. Moreover, arrows are capable of passing solely through green blocks."
gem_desc = "Gems are collectible items that are stored in the player’s inventory. To complete the game, the player has to collect all three gems dispersed throughout the maze."

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
    name: str - name of the item
    item_type: Category - type of the item
    item_desc: str - description of the item
    
    """
    name: str
    item_type: Category
    item_desc: str   
       
def extract_healthboost(file_path):
    """
    Extract the maze items from the YAML file.
    _file_path: str - path to yaml file
    
    This is intended to only be called if the item is a heart
    This funciton is designed to only be called by the 'pickup' function
    This function is not designed to be called stand-alone
    Returns the config.yaml value of the heart

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
    Extract the maze items from the YAML file.
    _file_path: str - path to yaml file

    This is intended to only be called if the item is a arrow
    This funciton is designed to only be called by the 'pickup' function
    This function is not designed to be called stand-alone
    Returns the config.yaml value of the arrow
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

def pickup(item):
    """
    Analyze items found in the maze
    Input is the item which must be instantiated by the Item class
    in order to have the necessary class attributes to analyze the item

    Returns the item's name from the Category subclass-attribute of the Item Class 
    Returns the item's value if applicable -- hearts return health values, arrows return
    damage values, other items return no values ('None')
    """
    
    # Get item name from the Category name
    item_name = item.item_type.name
    
    # if item is a heart or arrow, get the health boost amount or arrow damage amount
    if item_name == "HEART":
        item_val = extract_healthboost(file_path)
    elif item_name == "ARROW": 
        item_val = extract_damage(file_path)
    else: # gem, key, padlock items dont have special values
        item_val = None

    return item_name, item_val

def make_item(item):
    try: 
        if item == "Heart":
            return Item("Heart", Category.HEART, heart_desc)
        elif item == "Padlock":
            return Item("Padlock", Category.PADLOCK, padlock_desc)
        elif item == "Key":
            return Item("Key", Category.KEY, key_desc)
        elif item == "Arrow":
            return Item("Arrow", Category.ARROW, arrow_desc)
        elif item == "Gem":
            return Item("Gem", Category.GEM, gem_desc)
    except:
        print("Item name is not valid: ",item)
        return None
 
              
if __name__ == "__main__":
    
    # Option 1: direct usage of Item class to instantiate Items
    # these Examples of the item class will be used by player.py to instantiate items
    heart_item = Item("Heart", Category.HEART, heart_desc)
    padlock_item = Item("Padlock", Category.PADLOCK, padlock_desc)
    key_item = Item("Key", Category.KEY, key_desc)
    arrow_item = Item("Arrow", Category.ARROW, arrow_desc)
    gem_item = Item("Gem", Category.GEM, gem_desc)
    
    # Option 2: use function to instantiate Items
    heart_item = make_item("Heart")
    padlock_item = make_item("Padlock")
    key_item = make_item("Key")
    arrow_item = make_item("Arrow")
    gem_item = make_item("Gem")
    
    # The pickup function will be used by player.py to analyze items
    # This for-loop will print what the pickup function will do for each item type
    item_list = [heart_item, padlock_item, key_item, arrow_item, gem_item]
    for item in item_list:
        item_name, item_val = pickup(item)
        print("Found Item: ",item_name, "with value: ",item_val)
        
    # Example parsing the maze to see if player is on an object (enemy or item)
    inventory = []           # fake inventory just for the example
    maze = Maze(file_path)   # imported maze just for this example
    player_position = (0, 9) # example position -- this would be dynamic based on the user inputs
    arrows = maze.arrow_positions
    keys = maze.key_positions
    hearts = maze.heart_positions
    padlocks = maze.padlock_positions
    gems = maze.gem_positions
    if player_position in arrows:
        inventory.append(make_item("Arrow"))
    elif player_position in keys:
        inventory.append(make_item("Key"))
    elif player_position in hearts:
        pass # would increase the health here
    elif player_position in padlocks:
        inventory.append(make_item("Padlock"))
    elif player_position in gems:
        inventory.append(make_item("Gem"))

    print("\n\nPlayer's inventory: \n",inventory,"\n")
    
    
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

    
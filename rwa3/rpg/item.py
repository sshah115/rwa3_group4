from dataclasses import dataclass
from enum import Enum, auto

import sys
import os.path

folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(folder)
file_path = os.path.join(folder, "rpg", "config.yaml")

import yaml

heart_desc = "The player gets a health boost when the player occupies the same cell as a heart. Hearts are not added to the player’s inventory and are automatically consumed."
padlock_desc = "The player can not open a padlock unless at least one key is in the player’s inventory. To open padlocks, the player must be on the same cell as the padlock and in possession of at least one key."
key_desc = "Keys are collectible items that are stored in the player’s inventory when picked up. To use a key, the player must be on the same cell as a padlock."
arrow_desc = "Arrows are collectible items that players can store in their inventory. They are used to attack enemies within a three-tile range from the player, aligning with the player’s direction. Each arrow decreases an enemy’s health. Moreover, arrows are capable of passing solely through green blocks."
gem_desc = "Gems are collectible items that are stored in the player’s inventory. To complete the game, the player has to collect all three gems dispersed throughout the maze."

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
    
    Instance Attributes -- maybe dont need...
    position: int - location in the maze of the item ... maybe not needed ??
    value: int - ??? TODO 
    """
    name: str
    item_type: Category
    item_desc: str   
        
def extract_healthboost(file_path):
    """
    Extract the maze items from the YAML file.
    _file_path: str - path to yaml file

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

def pickup(self,Player, inventory):
    
    if self.type == "heart":
        if self.description == "super immunity":
            Player = Player + 40
            print("You found a super immunity heart! +40 health has been applied\n")
            print(Player)
        if self.description == "heal":
            Player = Player + 10
            print("You found a healing heart! +10 health has been applied\n")
            print(Player)
        return Player
    
    elif self.type == "key":
        inventory.append(str(self.name))
        print("You found a " + str(self.description) + " key! Adding to inventory. Current inventory: ")
        print(inventory)
        print("")
        return Player

        
    elif self.type == "arrow":
        inventory.append(str(self.name))
        print("You found a " + str(self.description) + " arrow! Adding to inventory. Current inventory: ")
        print(inventory)
        print("")
        return Player

if __name__ == "__main__":
    
    # Examples of creating items
    heart_item = Item("Heart", Category.HEART, heart_desc)
    padlock_item = Item("Padlock", Category.PADLOCK, padlock_desc)
    key_item = Item("Key", Category.KEY, key_desc)
    arrow_item = Item("Arrow", Category.ARROW, arrow_desc)
    gem_item = Item("Gem", Category.GEM, gem_desc)

    # Examples of an item object
    print("\nItem debugging: ")
    print("Heart_item: ",heart_item)
    print("Heart_item name: ",heart_item.name)
    print("Heart_item type name: ",heart_item.item_type.name)
    print("Heart_item type value: ",heart_item.item_type.value)
    print("Heart_item description: ",heart_item.item_desc)
    print("Health boost for this heart: ",extract_healthboost(file_path))

    # Example of a Category object
    print("\nCategory degugging:")
    print("Category list: ",list(Category))
    print("Example HEART enum name: ",Category.HEART.name)
    print("Example HEART enum value: ",Category.HEART.value)

    
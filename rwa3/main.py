import sys
import os.path
import shutil
import rpg.item as item
from rpg.maze import Maze  # noqa: E402

# Locate the config.yaml file
folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(folder)
file_path = os.path.join(folder, "rwa3", "rpg", "config.yaml")

if __name__ == "__main__":
    
    # Create backup of original config.yaml prior to modifying it during the game
    shutil.copy(file_path,file_path + ".original")

    # Print the maze
    maze = Maze(file_path)
    maze.print_maze()
    
    # Import the items in the maze 
    gems, keys, padlocks, arrows, hearts = item.make_items(maze)
    # Examples of accessing details about an item object
    print("\nExample of accessing Item attributes: ")
    print("Heart Item Object: ",hearts)
    print("Heart Item name: ",hearts.item_type.name)
    print("Heart Item position: ",hearts.item_position)
    print("Heart Item value: ",hearts.item_value)
    print("Heart Item emoji: ",hearts.item_emoji)
    
    # when done the game, replace the modified config.yaml with the original copy
    shutil.move(file_path + ".original", file_path)
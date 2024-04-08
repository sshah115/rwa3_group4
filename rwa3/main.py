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
    
    # NOTE: to test these 2 examples below, comment out the last step to move back the original yaml file. 
    # note: only run this once to avoid overwriting the ".original" yaml file with a modified file. 
    
    # Example of how to remove a position in config.yaml after collecting an item, for example a heart
    collected_heart_position = str([0, 0])
    with open(file_path, "r") as f:
        lines = f.readlines()
    with open(file_path, "w") as f:
        for line in lines:
            if collected_heart_position not in line.strip("\n"):
                f.write(line)
        f.close()
        
    # Example of how to overwrite a position in config.yaml after defeating an enemy
    defeated_enemy_position = str([2, 7])
    with open(file_path, "r") as f:
        lines = f.readlines()
    with open(file_path, "w") as f:
        for line in lines:
            if defeated_enemy_position not in line.strip("\n"):
                f.write(line)
            else:
                f.write("          position: \n") # write a position line with no value and the exact same indentation
    f.close()
                
    # when done testing the example code that modifies config.yaml, 
    # replace the modified config.yaml with the original copy (uncomment this line and rerun)
    shutil.move(file_path + ".original", file_path)
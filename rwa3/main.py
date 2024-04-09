import sys
import os.path
from rpg.maze import Maze  # noqa: E402
from rpg.player import Player

# Locate the config.yaml file
folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(folder)
file_path = os.path.join(folder, "rwa3", "rpg", "config.yaml")

if __name__ == "__main__":

    # Print the maze
    maze = Maze(file_path)
    maze.print_maze()
    Player(file_path, maze)
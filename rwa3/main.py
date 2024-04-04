import sys
import os.path

folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(folder)
from rpg.maze import Maze  # noqa: E402

file_path = os.path.join(folder, "rwa3", "rpg", "config.yaml")

if __name__ == "__main__":
    maze = Maze(file_path)
    maze.print_maze()
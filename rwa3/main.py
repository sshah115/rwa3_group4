"""
RWA3 - Group 4

main file to initiate the maze game
"""
from rpg.player import Player
from rpg.maze import Maze  # noqa: E402
from rpg.maze import file_path


if __name__ == "__main__":
    maze = Maze(file_path)
    maze.print_maze()
    # Starting the game loop using the start method of the Player class
    Player.start(Player.extract_player(), maze)
    
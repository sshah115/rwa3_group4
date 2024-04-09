
from rpg.player import Player
from rpg.maze import Maze  # noqa: E402
from rpg.maze import file_path


if __name__ == "__main__":
    maze = Maze(file_path)
    maze.print_maze()
    Player.start(Player.extract_player(), maze)
   

    

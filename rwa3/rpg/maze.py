import yaml

# these lines are needed to extract from config.yaml
import sys
import os.path
folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(folder)
file_path = os.path.join(folder, "rpg", "config.yaml")

class Maze:
    """
    Class to represent the maze.
    """

    _cls_empty = "  "
    _cls_horizontal_wall = "──"
    _cls_vertical_wall = "│"
    _cls_corner = "┼"

    def __init__(self, file_path):
        self._file_path = file_path
        self._grid_size = None
        # obstacles
        self._obstacle_positions = None
        self._obstacle_emoji = None
        # gems
        self._gem_positions = None
        self._gem_emoji = None
        # keys
        self._key_positions = None
        self._key_emoji = None
        # arrows
        self._arrow_positions = None
        self._arrow_emoji = None
        self._arrow_damage = None
        # hearts
        self._heart_positions = None
        self._heart_emoji = None
        self._heart_boost = None
        # padlocks
        self._padlock_positions = None
        self._padlock_emoji = None
        # skeletons
        self._skeleton_positions = []
        self._skeleton_emoji = None
        # dragons
        self._dragon_positions = []
        self._dragon_emoji = None
        # player
        self._player_position = None
        self._player_emoji = None

        self.extract_player()
        self.extract_obstacles()
        self.extract_grid_size()
        self.extract_enemies()
        self.extract_items()

        # Create the grid
        self._grid = [
            [self._cls_empty] * self._grid_size for _ in range(self._grid_size)
        ]

        self.spawn_components()

    def spawn_components(self):
        """
        Spawn the components on the grid.
        """
        self.spawn_obstacles()
        self.spawn_gems()
        self.spawn_enemies()
        self.spawn_padlocks()
        self.spawn_keys()
        self.spawn_arrows()
        self.spawn_hearts()
        self.spawn_player()

    def extract_grid_size(self):
        """
        Extract the grid size from the YAML file.
        """
        with open(self._file_path, "r") as file:
            try:
                data = yaml.safe_load(file)
                if "maze" in data and "grid_size" in data["maze"]:
                    self._grid_size = data["maze"]["grid_size"]
            except yaml.YAMLError as e:
                print(f"Error parsing YAML file: {e}")

    def extract_player(self):
        """
        Extract the player from the YAML file.
        """
        with open(self._file_path, "r") as file:
            try:
                data = yaml.safe_load(file)
                player_data = data["maze"]["player"]
                self._player_position = tuple(player_data["position"])
                player_direction = player_data["direction"]
                if player_direction == "up":
                    self._player_emoji = player_data["emoji_up"]
                elif player_direction == "down":
                    self._player_emoji = player_data["emoji_down"]
                elif player_direction == "left":
                    self._player_emoji = player_data["emoji_left"]
                elif player_direction == "right":
                    self._player_emoji = player_data["emoji_right"]
            except yaml.YAMLError as e:
                print(f"Error parsing YAML file: {e}")

    def extract_obstacles(self):
        """
        Extract the obstacles from the YAML file.
        """
        with open(self._file_path, "r") as file:
            try:
                data = yaml.safe_load(file)
                obstacle_positions = data["maze"]["obstacles"]["position"]
                self._obstacle_positions = [tuple(item) for item in obstacle_positions]
                self._obstacle_emoji = data["maze"]["obstacles"]["emoji"]
            except yaml.YAMLError as e:
                print(f"Error parsing YAML file: {e}")

    def extract_items(self):
        """
        Extract the maze items from the YAML file.
        """
        with open(self._file_path, "r") as file:
            try:
                data = yaml.safe_load(file)
                # Retrieve the gems
                gems_positions = data["maze"]["items"]["gems"]["position"]
                self._gem_positions = [tuple(item) for item in gems_positions]
                self._gem_emoji = data["maze"]["items"]["gems"]["emoji"]

                # Retrieve the keys
                keys_positions = data["maze"]["items"]["keys"]["position"]
                self._key_positions = [tuple(item) for item in keys_positions]
                self._key_emoji = data["maze"]["items"]["keys"]["emoji"]

                # Retrieve the padlocks
                padlock_positions = data["maze"]["items"]["padlocks"]["position"]
                self._padlock_positions = [tuple(item) for item in padlock_positions]
                self._padlock_emoji = data["maze"]["items"]["padlocks"]["emoji"]

                # Retrieve the arrows
                arrow_positions = data["maze"]["items"]["arrows"]["position"]
                self._arrow_positions = [tuple(item) for item in arrow_positions]
                self._arrow_emoji = data["maze"]["items"]["arrows"]["emoji"]
                self._arrow_damage = data["maze"]["items"]["arrows"]["damage"]

                # Retrieve the hearts
                heart_positions = data["maze"]["items"]["hearts"]["position"]
                self._heart_positions = [tuple(item) for item in heart_positions]
                self._heart_emoji = data["maze"]["items"]["hearts"]["emoji"]
                self._heart_boost = data["maze"]["items"]["hearts"]["health"]
            except yaml.YAMLError as e:
                print(f"Error parsing YAML file: {e}")

    def extract_enemies(self):
        """
        Extract enemy data from the YAML file.
        """

        with open(self._file_path, "r") as file:
            try:
                data = yaml.safe_load(file)
                # Retrieve the enemies: dragons
                for dragon_data in data["maze"]["enemies"]["dragons"]:
                    position = tuple(dragon_data["dragon"]["position"])
                    self._dragon_positions.append(position)
                self._dragon_emoji = data["maze"]["enemies"]["dragon_emoji"]

                # Retrieve the enemies: skeletons
                for skeleton_data in data["maze"]["enemies"]["skeletons"]:
                    position = tuple(skeleton_data["skeleton"]["position"])
                    self._skeleton_positions.append(position)
                self._skeleton_emoji = data["maze"]["enemies"]["skeleton_emoji"]
            except yaml.YAMLError as e:
                print(f"Error parsing YAML file: {e}")

    @property
    def cls_empty(self):
        return self._cls_empty

    @property
    def obstacle_positions(self):
        """
        The positions of the obstacles in the maze.
        """
        return self._obstacle_positions

    @property
    def skeleton_positions(self):
        """
        The positions of the skeletons in the maze.
        """
        return self._skeleton_positions
    
    @property
    def skeleton_emoji(self):
        """_
        The emoji of enemy type Skeleton
        """
        return self._skeleton_emoji

    def remove_skeleton_position(self, position):
        """
        Remove a skeleton's position
        
        Args:
            position (tuple): The position of the skeleton to be removed.
        """
        self._grid[position[0]][position[1]] = self._cls_empty
        self._skeleton_positions.remove(tuple(position))
        
    @property
    def dragon_positions(self):
        """
        The positions of the dragons in the maze.
        """
        return self._dragon_positions
    
    def remove_dragon_position(self, position):
        """
        Remove a skeleton's position
        
        Args:
            position (tuple): The position of the dragon to be removed.
        """
        self._grid[position[0]][position[1]] = self._cls_empty
        self._dragon_positions.remove(tuple(position))

    @property
    def dragon_emoji(self):
        """_
        The emoji of enemy type Dragon
        """
        return self._dragon_emoji

    @property
    def grid(self):
        """
        The grid of the maze.
        """
        return self._grid
    
    @property
    def grid_size(self):
        """
        The grid size of the maze.
        """
        return self._grid_size

    @property
    def gem_positions(self):
        """
        The gem stone items.
        """
        return self._gem_positions

    def remove_gem_position(self, position):
        """
        Remove a gem's position
        
        Args:
            position (tuple): The position of the gem to be removed.
        """
        self._gem_positions.remove(position)
    
    @property
    def gem_emoji(self):
        """
        The gem emoji
        """
        return self._gem_emoji

    @property
    def key_positions(self):
        """
        The key items.
        """
        return self._key_positions

    def remove_key_position(self, position):
        """
        Remove a key's position
        
        Args:
            position (tuple): The position of the key to be removed.
        """
        self._key_positions.remove(position)

    @property
    def key_emoji(self):
        """
        The key emoji
        """
        return self._key_emoji

    @property
    def arrow_positions(self):
        """
        The arrow items.
        """
        return self._arrow_positions
    
    def remove_arrow_position(self, position):
        """
        Remove an arrow's position
        
        Args:
            position (tuple): The position of the arrow to be removed.
        """
        self._arrow_positions.remove(position)

    @property
    def arrow_emoji(self):
        """
        The arrow emoji
        """
        return self._arrow_emoji

    @property
    def heart_positions(self):
        """
        The heart items.
        """
        return self._heart_positions
    
    def remove_heart_position(self, position):
        """
        Remove a heart's position
        
        Args:
            position (tuple): The position of the heart to be removed.
        """
        self._heart_positions.remove(position)

    @property
    def heart_emoji(self):
        """
        The heart emoji.
        """
        return self._heart_emoji

    @property
    def padlock_positions(self):
        """
        The padlocks items.
        """
        return self._padlock_positions

    def remove_padlock_position(self, position):
        """
        Remove a padlock's position
        
        Args:
            position (tuple): The position of the padlock to be removed.
        """
        self._padlock_positions.remove(position)

    @property
    def padlock_emoji(self):
        """
        The padlocks emoji.
        """
        return self._padlock_emoji

    @property
    def player_emoji(self):
        """
        The player emoji
        """
        return self._player_emoji

    def set_player_emoji(self, emoji):
        """
        Set a player's emoji
        
        Args:
            emoji (str): The emoji of the player to be used.
        """
        self._player_emoji  = emoji

    @property
    def player_position(self):
        """
        The player position
        """
        return self._player_position

    def set_player_position(self, position):
        """
        Set a player's position

        Args:
            position (list): player's new position
        """
        self._player_position = position
    
    def spawn_player(self):
        """
        Spawn the player on the grid.
        """
        self._grid[self._player_position[0]][self._player_position[1]] = (
            self._player_emoji
        )

    def spawn_obstacles(self):
        """
        Spawn the obstacles on the grid.
        """
        for position in self._obstacle_positions:
            self._grid[position[0]][position[1]] = self._obstacle_emoji

    def spawn_gems(self):
        """
        Spawn the gems on the grid.
        """
        for position in self._gem_positions:
            self._grid[position[0]][position[1]] = self._gem_emoji

    def spawn_enemies(self):
        """
        Spawn the enemies on the grid.
        """
        for skeleton_position in self._skeleton_positions:
            self._grid[skeleton_position[0]][skeleton_position[1]] = (
                self._skeleton_emoji
            )

        for dragon_position in self._dragon_positions:
            self._grid[dragon_position[0]][dragon_position[1]] = self._dragon_emoji

    def spawn_padlocks(self):
        """
        Spawn the padlocks on the grid.
        """
        for position in self._padlock_positions:
            self._grid[position[0]][position[1]] = self._padlock_emoji

    def spawn_keys(self):
        """
        Spawn the keys on the grid.
        """
        for position in self._key_positions:
            self._grid[position[0]][position[1]] = self._key_emoji

    def spawn_arrows(self):
        """
        Spawn the arrows on the grid.
        """
        for position in self._arrow_positions:
            self._grid[position[0]][position[1]] = self._arrow_emoji

    def spawn_hearts(self):
        """
        Spawn the hearts on the grid.
        """
        for position in self._heart_positions:
            self._grid[position[0]][position[1]] = self._heart_emoji

    def print_maze(self):
        """
        Print the maze.
        """

        print("┌" + "─" * (self._grid_size * 3 - 1) + "┐")

        for i, row in enumerate(self._grid):
            # Print left boundary
            print(self._cls_vertical_wall, end="")

            # Print cell contents
            for j, cell in enumerate(row):
                print(cell, end="")
                # Print vertical wall if not in the last column
                if j < self._grid_size - 1:
                    print(self._cls_vertical_wall, end="")

            # Print right boundary
            print(self._cls_vertical_wall)

            # Print horizontal wall between rows (except for the last row)
            if i < self._grid_size - 1:
                print("├" + "─" * (self._grid_size * 3 - 1) + "┤")

        # Print bottom boundary
        print("└" + "─" * (self._grid_size * 3 - 1) + "┘")
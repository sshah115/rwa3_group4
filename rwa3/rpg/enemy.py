import yaml

from rpg.maze import file_path
from abc import ABC, abstractmethod
import rpg.player


class Enemy(ABC):
    """
    A class representing an enemy in the game.

    Attributes:
        name (str): The name of the enemy.
        health (int): The health of the enemy.
    """

    def __init__(
        self, position, name, health, attack_power
    ):
        """
        Initialize the enemy.

        Args:
            position (tuple): The position of the enemy in the maze.
            name (str): The name of the enemy.
            health (int): The health points of the enemy.
            attack_power (int): The attack power of the enemy. 
        """
        self._position = position
        self._name = name
        self._health = health
        self._attack_power = attack_power

    @property
    def attack_power(self):
        """
        The attack power of the enemy.

        """
        return self._attack_power

    @property
    def position(self):
        """
        The position of the enemy in the maze.

        """
        return self._position

    @abstractmethod
    def attack(self, player, damage):
        """
        Attack the player.

        Args:
            player (Player): The player to attack.
            damage (int): The amount of damage to deal.
        """
        pass

    @abstractmethod
    def take_damage(self, damage):
        """
        Take damage from the player.

        Args:
            damage (int): The amount of damage to take.
        """
        pass

    @abstractmethod
    def extract_enemy(cls, position):
        """
        Extract enemy data from the YAML file.

        Args:
            position (list): positional index of enemy
        """

        pass


class Skeleton(Enemy):
    """
    A class representing a skeleton enemy in the game. All skeletons have a shield power. The health of a skeleton is 50.

    Attributes:
        shield_power (int): The power of the skeleton's shield.
    """

    def __init__(self, name, health, position, shield_power, attack_power):
        """
        Initialize the skeleton enemy.

        Args:
            name (str): The name of the skeleton.
            health (int): The health points of the skeleton.
            position (tuple): The position of the skeleton in the maze.
            shield_power (int): The power of the skeleton's shield.
            attack_power (int): The attack power of the enemy. 
        """
        super().__init__(name=name, health=health, position=position, attack_power=attack_power)
        self._shield_power = shield_power

    @property
    def name(self):
        """
        The name of the skeleton.

        """
        return self._name

    @property
    def health(self):
        """
        The health points of the skeleton.

        """
        return self._health

    def attack(self, player, damage):
        """
        Attack the player.

        Args:
            player (Player): The player to attack.
            damage (int): The amount of damage to deal.
        """
        print(f"🧟🗡️ {self._name} attacks {player.name}!")
        player.take_damage(damage)

    def take_damage(self, damage):
        """
        Take damage from the player.

        Args:
            damage (int): The amount of damage to take.
        """
        # super().take_damage(damage - self._shield_power)

        # Shield power reduces total damage
        damage = damage - self._shield_power
        self._health = self._health - damage
        if self._health <= 0:
            print(f"🧟💀 {self._name} has been defeated!")
        else:
            print(f"🧟💜 {self._name} has {self._health} health left.")

    @classmethod
    def extract_enemy(cls, position):
        """
        Extract enemy data from the YAML file.

        Args:
            position (list): Positional index of the skeleton.

        Returns:
            Skeleton: A new instance of Skeleton extracted from the YAML file.
        """

        with open(file_path, "r") as file:
            try:
                data = yaml.safe_load(file)
                # Retrieve the enemies: dragons
                for enemy_data in data["maze"]["enemies"]["skeletons"]:
                    if list(position) == enemy_data["skeleton"]["position"]:
                        return Skeleton(
                            enemy_data["skeleton"]["name"],
                            enemy_data["skeleton"]["health"],
                            enemy_data["skeleton"]["position"],
                            enemy_data["skeleton"]["shield_power"],
                            data["maze"]["enemies"]["attack_power"]
                        )

            except yaml.YAMLError as e:
                print(f"Error parsing YAML file: {e}")
        pass


class Dragon(Enemy):
    """
    A class representing a dragon enemy in the game. All dragons have a fire breath power. The health of a dragon is 200.

    Attributes:
        fire_breath_power (int): The power of the dragon's fire breath.
    """

    def __init__(self, name, health, position, fire_breath_power, attack_power):
        """
        Initialize the dragon enemy.

        Args:
            name (str): The name of the dragon.
            health (int): The health points of the dragon.
            position (tuple): The position of the dragon in the maze.
            fire_breath_power (int): The power of the dragon's fire breath.
            attack_power (int): The attack power of the enemy. 
        """
        super().__init__(name=name, health=health, position=position, attack_power= attack_power)
        self._fire_breath_power = fire_breath_power

    @property
    def name(self):
        """ 
        The name of the dragon.
        """
        return self._name

    @property
    def health(self):
        """
        The health points of the dragon.

        """
        return self._health

    def attack(self, player, damage):
        """
        Attack the player.

        Args:
            player (Player): The player to attack.
            damage (int): The amount of damage to deal.
        """
        print(f"🧟🗡️ {self._name} attacks {player.name}!")
        player.take_damage(damage + self._fire_breath_power)

    def take_damage(self, damage):
        """
        Take damage from the player.

        Args:
            damage (int): The amount of damage to take.
        """
        self._health -= damage
        if self._health <= 0:
            print(f"🧟💀 {self._name} has been defeated!")
        else:
            print(f"🧟💜 {self._name} has {self._health} health left.")

    @classmethod
    def extract_enemy(cls, position):
        """
        Extract enemy data from the YAML file.

        Args:
            position (list): Positional index of the dragon.

        Returns:
            Dragon: A new instance of Dragon extracted from the YAML file.
        """

        with open(file_path, "r") as file:
            try:
                data = yaml.safe_load(file)
                # Retrieve the enemies: dragons
                for enemy_data in data["maze"]["enemies"]["dragons"]:
                    if list(position) == enemy_data["dragon"]["position"]:
                        return Dragon(
                            enemy_data["dragon"]["name"],
                            enemy_data["dragon"]["health"],
                            enemy_data["dragon"]["position"],
                            enemy_data["dragon"]["fire_power"],
                            data["maze"]["enemies"]["attack_power"]
                        )

            except yaml.YAMLError as e:
                print(f"Error parsing YAML file: {e}")
        pass

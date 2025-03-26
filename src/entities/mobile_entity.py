from abc import ABC, abstractmethod
import numpy as np
from src.constants import FOLDER_CONFIG_PATH
from src.entities.entity import Entity
from src.utils import get_config


class MobileEntity(Entity, ABC):
    """ This class will be function as base class for mobile object such as Herbivore and Predator """

    def __init__(self, row: int, col: int) -> None:
        super().__init__(row, col)  # Initialize base constructor
        self.radius_sight = None  # Moves towards the closest Herbivore they can see in a (R_predator_sight)
        self.speed = 1  # speed = 1 means entity moves at normal speed, speed = 2 means moves twice faster

    @property
    @abstractmethod
    def target_object(self):
        """
        Defines the target object that the MobileEntity moves towards.

        This property must be implemented in subclasses to specify
        the type of object the entity should seek (e.g., Herbivores
        for Predators, Plants for Herbivores).

        Returns:
            Type[Entity]: The class reference of the target entity.
        """

    def move(self, grid):
        """ Defines how the entity moves, Each subclass will implement this. """

        # speed means here to moves the same amount of steps as the speed value
        for _ in range(self.speed):
            if not self.is_alive():
                return  # Don't move if the MobileEntity is dead

            # Store the old position before moving
            old_row, old_col = int(self.row), int(self.col)

            nearest_plant = self.find_nearest_target_object(grid, self.target_object)

            if nearest_plant:
                self.move_towards(nearest_plant)

            else:
                self.move_randomly(grid)

            old_pos = (old_row, old_col)
            new_pos = (int(self.row), int(self.col))

            self.update_position_on_grid(grid, old_pos, new_pos)


    def update_position_on_grid(self, grid, old_pos: tuple[int, int], new_pos: tuple[int, int]):
        """
        Updates the entity's position on the grid.

        If the entity reaches a target, appropriate actions are taken.
        This avoids code duplication between Predator, FastPredator, and Herbivore.

        Args:
            grid: The simulation grid.
            old_pos (tuple[int, int]): The entity's previous position (row, col).
            new_pos (tuple[int, int]): The entity's new position (row, col).
        """

        old_row, old_col = old_pos
        new_row, new_col = new_pos

        if new_row != old_row or new_col != old_col:
            target = grid.cells[new_row][new_col]

            if target is not None:
                self.eat(target)

            # Move entity to his new position
            grid.cells[new_row][new_col] = self
            grid.update_empty_cells(new_row, new_col, is_occupied=True)

            # Clear old position
            grid.cells[old_row][old_col] = None
            grid.update_empty_cells(old_row, old_col, is_occupied=False)


    def eat(self, target):
        """
        Defines the eating behavior of the MobileEntity.

        Subclasses must implement this method to define how the entity interacts
        with its target object upon reaching it.

        - Predators consume Herbivores and reset their lifespan.
        - Herbivores consume Plants and increase their lifespan.
        """

        if isinstance(target, self.target_object):
            self.current_lifespan = self.lifespan


    def find_nearest_target_object(self, grid, target_object):
        """ Finds the closest target position within sight radius."""
        closest_target_pos = None
        min_distance = float("inf")

        rows, cols = grid.cells.shape  # Get dimensions from NumPy array

        min_starting_row = max(0, self.row - self.radius_sight)
        max_starting_row = min(rows, self.row + self.radius_sight + 1)

        min_starting_col = max(0, self.col - self.radius_sight)
        max_starting_col = min(cols, self.col + self.radius_sight + 1)


        for row in range(min_starting_row, max_starting_row):
            for col in range(min_starting_col, max_starting_col):

                if isinstance(grid.cells[row][col], target_object):

                    # Manhattan distance is a metric used to determine the distance between
                    # two points in a grid-like path
                    distance = abs(self.row - row) + abs(self.col - col)

                    if distance < min_distance:
                        min_distance = distance
                        closest_target_pos = (row, col)

        return closest_target_pos

    def move_towards(self, target):
        """ Moves one step towards the target object.
            Each subclass will implement this. """
        target_row, target_col = target

        if self.row < target_row:
            self.row += 1

        elif self.row > target_row:
            self.row -= 1

        if self.col < target_col:
            self.col += 1

        elif self.col > target_col:
            self.col -= 1

    def move_randomly(self, grid):
        """ Moves randomly to an empty neighbor cell on the grid. """
        empty_neighbors = grid.get_empty_neighbors(self.row, self.col)

        if empty_neighbors.size > 0:  # Check if there are any empty neighbors
            new_row, new_col = empty_neighbors[np.random.choice(len(empty_neighbors))]
            self.row, self.col = new_row, new_col


    def load_entity_param_from_yaml(self):
        """ Load object's parameters (T_plant_steps, T_herbivore_steps, R_herbivore_sight,
            T_cooldown_steps, T_predator_steps) from .yaml file.
            Each subclass will implement this. """

        try:
            config_data = get_config()

            game_param = config_data.get("game_param", {})

            class_name = self.name()

            t_class_name_steps = "T_" + class_name + "_steps"
            r_class_name_steps = "R_" + class_name + "_sight"

            if class_name not in game_param:
                raise ValueError(f"Missing {class_name} parameters in game_param")

            if t_class_name_steps not in game_param[class_name]:
                raise ValueError(f"Missing t_class_name_steps for {class_name}")

            if r_class_name_steps not in game_param[class_name]:
                raise ValueError(f"Missing {r_class_name_steps} parameters in game_param")


            self.lifespan = game_param[class_name][t_class_name_steps]
            self.current_lifespan = self.lifespan
            self.radius_sight = int(game_param[class_name][r_class_name_steps])

            if self.lifespan <= 0:
                raise ValueError(f"Invalid lifespan: {self.lifespan}, must be > 0")

            if self.radius_sight <= 0:
                raise ValueError(f"Invalid R_FastPredator_sight: {self.radius_sight}, must be > 0")

        except FileNotFoundError as not_found:
            raise ValueError(f"Config file not found at {FOLDER_CONFIG_PATH}") from not_found

        except Exception as e:
            raise ValueError(f"Error loading Predator parameters: {e}") from e

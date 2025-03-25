from abc import ABC, abstractmethod
import numpy as np
from src.entities.entity import Entity


class MobileEntity(Entity, ABC):
    """ This class will be function as base class for mobile object such as Herbivore and Predator """

    def __init__(self, row: int, col: int) -> None:
        super().__init__(row, col)  # Initialize base constructor
        self.__radius_sight = None  # Private member

    @abstractmethod
    def move(self, grid):
        """ Defines how the entity moves, Each subclass will implement this. """
        pass

    def find_nearest_target_object(self, grid, target_object):
        """Finds the closest target within sight radius."""
        closest_target = None
        min_distance = float("inf")

        rows, cols = grid.cells.shape  # Get dimensions from NumPy array

        min_starting_row = max(0, self.row - self.__radius_sight)
        max_starting_row = min(rows, self.row + self.__radius_sight + 1)

        min_starting_col = max(0, self.col - self.__radius_sight)
        max_starting_col = min(cols, self.col + self.__radius_sight + 1)

        for row in range(min_starting_row, max_starting_row):
            for col in range(min_starting_col, max_starting_col):

                if isinstance(grid.cells[row][col], target_object):

                    # Manhattan distance is a metric used to determine the distance between
                    # two points in a grid-like path
                    distance = abs(self.row - row) + abs(self.col - col)

                    if distance < min_distance:
                        min_distance = distance
                        closest_target = (row, col)

        return closest_target

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

    @abstractmethod
    def load_entity_param_from_yaml(self):
        """ Load object's parameters (T_plant_steps, T_herbivore_steps, R_herbivore_sight,
            T_cooldown_steps, T_predator_steps) from .yaml file.
            Each subclass will implement this. """
        pass

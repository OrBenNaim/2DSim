import numpy as np


class Entity:
    """ Base class for all entities in the simulation. """
    def __init__(self, row: int, col: int) -> None:
        self.row = row
        self.col = col
        self.lifespan = None
        self.current_lifespan = 0
        self.load_entity_param_from_yaml()  # Load object's parameters


    def move(self, grid):
        """ Defines how the entity moves, Each subclass (except from Plant) will implement this. """
        pass


    def move_towards(self, target):
        """ Moves one step towards the target object.
            Each subclass (except from Plant) will implement this. """
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


    def is_alive(self):
        """ Checks if the entity still alive. """
        return self.current_lifespan > 0


    def load_entity_param_from_yaml(self):
        """ Load object's parameters (T_plant_steps, T_herbivore_steps, R_herbivore_sight,
            T_cooldown_steps, T_predator_steps) from .yaml file.
            Each subclass will implement this. """
        pass
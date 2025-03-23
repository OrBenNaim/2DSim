import yaml

from src.constant import FOLDER_CONFIG_PATH


class Entity:
    """ Base class for all entities in the simulation. """
    def __init__(self, row: int, col: int) -> None:
        self.row = row
        self.col = col
        self.lifespan = None
        self.current_lifespan = 0


    def load_entity_param_from_yaml(self):
        """ Load object's parameters (T_plant_steps, T_herbivore_steps, R_herbivore_sight,
            T_cooldown_steps, T_predator_steps) from .yaml file.
            Each subclass will implement this. """
        pass


    def move(self, grid):
        """ Defines how the entity moves, Each subclass will implement this. """
        pass

    def reproduce(self, grid):
        """ Defines reproduction behavior, Each subclass will implement this. """
        pass

    def is_alive(self):
        """ Checks if the entity still alive. """
        return self.lifespan > 0


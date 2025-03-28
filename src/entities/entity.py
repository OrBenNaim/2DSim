from abc import ABC
from src.constants import FOLDER_CONFIG_PATH
from src.utils import get_config


class Entity(ABC):
    """ Abstract Base class for all entities in the simulation. """

    def __init__(self, row: int, col: int, emoji: str) -> None:
        self.row = row
        self.col = col
        self.lifespan = 0              # Private member
        self.current_lifespan = 0
        self.emoji = emoji
        self.game_param = get_config().get("game_param", {})

    def is_alive(self):
        """ Checks if the entity still alive. """
        return self.current_lifespan > 0

    def get_current_lifespan(self):
        """ Getter function to the private attribute self.__current_lifespan """
        return self.current_lifespan

    def decrease_current_lifespan(self):
        """ Decrease current_lifespan by one """
        self.current_lifespan -= 1

    def name(self):
        """ Get the object name """
        return self.__class__.__name__

    def load_entity_param_from_yaml(self):
        """ Load object's parameters (T_Object_steps) from .yaml file.
            Each subclass from MobileEntity class will implement this.
            Subclasses which are not belong to Mobile Entity do not need to implement this method. """
        try:
            t_class_name_steps = "T_" + self.name() + "_steps"

            if self.name() not in self.game_param:
                raise ValueError(f"Missing '{self.name()}' parameters in game_param")

            if t_class_name_steps not in self.game_param[self.name()]:
                raise ValueError(f"Missing '{t_class_name_steps}' for {self.name()}")

            # For all classes:
            self.lifespan = self.game_param[self.name()][t_class_name_steps]
            self.current_lifespan = self.lifespan

        except FileNotFoundError as not_found:
            raise ValueError(f"Config file not found at {FOLDER_CONFIG_PATH}") from not_found

        except Exception as e:
            raise ValueError(f"Error loading Predator parameters: {e}") from e

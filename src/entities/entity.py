from abc import ABC, abstractmethod
from src.constants import FOLDER_CONFIG_PATH
from src.utils import get_config


class Entity(ABC):
    """ Abstract Base class for all entities in the simulation. """

    def __init__(self, row: int, col: int) -> None:
        self.row = row
        self.col = col
        self.lifespan = None              # Private member
        self.current_lifespan = None

    @property
    @abstractmethod
    def emoji(self):
        """
        Abstract property that must be implemented by subclasses to return
        the emoji representation of the entity.

        Returns:
            str: A string containing the emoji that represents the entity.
        """

    def is_alive(self):
        """ Checks if the entity still alive. """
        return self.current_lifespan > 0

    def get_current_lifespan(self):
        """ Getter function to the private attribute self.__current_lifespan """
        return self.current_lifespan

    def decrease_current_lifespan(self):
        """ Decrease current_lifespan by one """
        self.current_lifespan -= 1

    def load_entity_param_from_yaml(self):
        """ Load object's parameters (T_Object_steps) from .yaml file.
            Each subclass from MobileEntity class will implement this.
            Subclasses which are not belong to Mobile Entity do not need to implement this method. """
        try:
            config_data = get_config()
            game_param = config_data.get("game_param", {})
            class_name = self.__class__.__name__
            t_class_name_steps = "T_" + class_name + "_steps"

            if class_name not in game_param:
                raise ValueError(f"Missing '{class_name}' parameters in game_param")

            if t_class_name_steps not in game_param[class_name]:
                raise ValueError(f"Missing '{t_class_name_steps}' for {class_name}")

            # For all classes:
            self.lifespan = game_param[class_name][t_class_name_steps]
            self.current_lifespan = self.lifespan

        except FileNotFoundError as not_found:
            raise ValueError(f"Config file not found at {FOLDER_CONFIG_PATH}") from not_found

        except Exception as e:
            raise ValueError(f"Error loading Predator parameters: {e}") from e

    def name(self):
        """ Get the object name """
        return self.__class__.__name__

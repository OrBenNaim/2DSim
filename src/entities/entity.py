from abc import ABC, abstractmethod
import yaml
from src.constants import FOLDER_CONFIG_PATH


class Entity(ABC):
    """ Abstract Base class for all entities in the simulation. """

    def __init__(self, row: int, col: int) -> None:
        self.row = row
        self.col = col
        self.__lifespan = None              # Private member
        self.__current_lifespan = 0
        self.load_entity_param_from_yaml()  # Load object's parameters

    @property
    @abstractmethod
    def emoji(self):
        pass  # Must be implemented in subclasses as a property

    def is_alive(self):
        """ Checks if the entity still alive. """
        return self.__current_lifespan > 0

    def get_current_lifespan(self):
        """ Getter function to the private attribute self.__current_lifespan """
        return self.__current_lifespan

    def decrease_current_lifespan(self):
        self.__current_lifespan -= 1

    def load_entity_param_from_yaml(self):
        """ Load object's parameters (T_Object_steps) from .yaml file.
            Each subclass from MobileEntity class will implement this. """
        try:
            with open(FOLDER_CONFIG_PATH, "r") as file:
                config = yaml.safe_load(file)

            game_param = config.get("game_param", {})
            class_name = self.__class__.__name__
            T_class_name_steps = "T_" + class_name + "_steps"

            if class_name not in game_param:
                raise ValueError(f"Missing '{class_name}' parameters in game_param")

            if T_class_name_steps not in game_param[class_name]:
                raise ValueError(f"Missing '{T_class_name_steps}' for {class_name}")

            # For all classes:
            self.__lifespan = game_param[class_name][T_class_name_steps]
            self.__current_lifespan = self.__lifespan

        except FileNotFoundError:
            raise ValueError(f"Config file not found at {FOLDER_CONFIG_PATH}")

        except Exception as e:
            raise ValueError(f"Error loading Predator parameters: {e}") from e

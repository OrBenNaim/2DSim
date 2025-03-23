import yaml

from entity import Entity
from src.constant import FOLDER_CONFIG_PATH


class Plant(Entity):
    """ Plants don't move, they die after fix steps or after being eaten """
    def __init__(self, row: int, col: int):
        super().__init__(row, col)
        self.load_entity_param_from_yaml()


    def load_entity_param_from_yaml(self):
        """ Load object's parameters (T_plant_steps, T_herbivore_steps, R_herbivore_sight,
            T_cooldown_steps, T_predator_steps) from .yaml file. """
        try:
            # Load configuration settings from a YAML file
            with open(FOLDER_CONFIG_PATH, "r") as file:
                config = yaml.safe_load(file)

            game_param = config.get("game_param", {})

            self.lifespan = game_param['Plant']['T_plant_steps']

        except Exception as e:
            print(f"Error loading file: {e}")
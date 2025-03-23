import yaml
from src.constant import FOLDER_CONFIG_PATH
from src.entities.entity import Entity
from src.entities.plant import Plant


class Predator(Entity):
    """Predators hunt herbivores and extend their lifespan when they eat."""
    def __init__(self, row, col):
        super().__init__(row, col)
        self.predator_sight = None    # Predators move towards the closest Herbivore they can see in R_predator_sight

        self.load_entity_param_from_yaml()  # Load T_predator_steps, R_predator_sight


    def load_entity_param_from_yaml(self):
        """ Load object's parameters (T_plant_steps, T_herbivore_steps, R_herbivore_sight,
            T_cooldown_steps, T_predator_steps) from .yaml file. """
        try:
            # Load configuration settings from a YAML file
            with open(FOLDER_CONFIG_PATH, "r") as file:
                config = yaml.safe_load(file)

            game_param = config.get("game_param", {})

            self.lifespan = game_param['Predator']['T_predator_steps']
            self.predator_sight = game_param['Predator']['R_predator_sight']

        except Exception as e:
            print(f"Error loading file: {e}")


    def move(self, grid):
        """Moves towards the closest herbivore. If none are visible, moves randomly."""
        herbivore = self.find_nearest_herbivore(grid)
        if herbivore:
            self.move_towards(herbivore)
        else:
            self.move_randomly(grid)

        # Kill plant if stepping on one
        if isinstance(grid[self.row][self.col], Plant):
            grid[self.row][self.col] = None


    def move_towards(self, target):
        """Moves one step towards the target herbivore."""


    def find_nearest_herbivore(self, grid):
        """Finds the closest herbivore within sight radius."""
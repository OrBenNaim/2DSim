import yaml

from entity import Entity
from src.constant import FOLDER_CONFIG_PATH


class Herbivore(Entity):
    """ Herbivore move towards plants, eat them and reproduce. """
    def __init__(self, row: int, col: int) -> None:
        super().__init__(row, col)          # Initialize base constructor
        self.herbivore_sight = None         # Herbivores move towards the closest plant they can see
        self.reproduction_cooldown = None   # Cooldown before it can reproduce again
        self.current_cooldown = 0           # Tracks cooldown progress

        self.load_entity_param_from_yaml()  # Load T_herbivore_steps, R_herbivore_sight, T_cooldown_steps


    def load_entity_param_from_yaml(self):
        """ Load object's parameters (T_plant_steps, T_herbivore_steps, R_herbivore_sight,
            T_cooldown_steps, T_predator_steps) from .yaml file. """
        try:
            # Load configuration settings from a YAML file
            with open(FOLDER_CONFIG_PATH, "r") as file:
                config = yaml.safe_load(file)

            game_param = config.get("game_param", {})

            self.lifespan = game_param['Herbivore']['T_herbivore_steps']
            self.herbivore_sight = game_param['Herbivore']['R_herbivore_sight']
            self.reproduction_cooldown = game_param['Herbivore']['T_cooldown_steps']

        except Exception as e:
            print(f"Error loading file: {e}")


    def move(self, grid):
        """ Move towards the closest plant they can see in a (herbivore_sight) radius
            or randomly if none are visible """
        plant = self.find_nearest_plant(grid)
        if plant:
            self.move_towards(plant)

        else:
            self.move_randomly()


    def reproduce(self, grid) -> None:
        """ Staying in the same space and spawning another herbivore
            in a random neighboring cell if cooldown is over """
        if self.current_cooldown > 0:
            self.current_cooldown -= 1
            return

        # else, cooldown is over
        # Create all neighbor indexes
        ref_shifts = [

        ]

        neighbors = grid[self.row - 1 : self.row + 2, self.col - 1 : self.col + 2], (self.row, self.col)








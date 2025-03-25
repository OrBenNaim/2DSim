import yaml
from src.constants import FOLDER_CONFIG_PATH
from src.entities.herbivore import Herbivore
from src.entities.mobile_entity import MobileEntity
from src.entities.plant import Plant


class Predator(MobileEntity):
    """Predators hunt herbivores and extend their lifespan when they eat."""

    def __init__(self, row, col):
        super().__init__(row, col)

    @property
    def emoji(self):
        return "🦊"

    def move(self, grid):
        """ Move towards the closest herbivore they can see in a (herbivore_sight) radius
            or randomly if none are visible """

        if not self.is_alive():
            return  # Don't move if the herbivore is dead

        # Store the old position before moving
        old_row, old_col = self.row, self.col

        nearest_herbivore = self.find_nearest_target_object(grid, Herbivore)
        print(f"nearest_herbivore_position: {nearest_herbivore}")

        if nearest_herbivore:
            self.move_towards(nearest_herbivore)

        else:
            self.move_randomly(grid)

        # Update the grid: vacate old position and occupy new position
        if self.row != old_row or self.col != old_col:

            # Predator reaches Plant
            if isinstance(grid.cells[self.row][self.col], Plant):
                grid.cells[self.row][self.col] = self  # Move predator to his next location on the grid

            # Predator reaches Herbivore
            elif isinstance(grid.cells[self.row][self.col], Herbivore):
                grid.cells[self.row][self.col] = self  # Move predator to his next location on the grid
                self.current_lifespan = self.lifespan  # Refuel lifespan

            # Predator reaches to empty cell
            elif grid.cells[self.row][self.col] is None:
                grid.cells[self.row][self.col] = self  # Move predator to his next location on the grid
                grid.update_empty_cells(self.row, self.col, is_occupied=True)

            # Predator reaches another Predator (do nothing)

            # For all cases -> clear predator's old position on grid.cells
            grid.cells[old_row][old_col] = None
            grid.update_empty_cells(old_row, old_col, is_occupied=False)

    def load_entity_param_from_yaml(self):
        """ Load object's parameters (T_predator_steps, R_predator_sight) from .yaml file. """
        try:
            with open(FOLDER_CONFIG_PATH, "r") as file:
                config = yaml.safe_load(file)

            game_param = config.get("game_param", {})

            if 'Predator' not in game_param:
                raise ValueError("Missing 'Predator' parameters in game_param")

            if 'T_Predator_steps' not in game_param['Predator']:
                raise ValueError("Missing 'T_Predator_steps' for Predator")

            if 'R_Predator_sight' not in game_param['Predator']:
                raise ValueError("Missing 'R_Predator_sight' parameters in game_param")

            self.set_lifespan(game_param['Predator']['T_Predator_steps'])
            self.set_current_lifespan(self.lifespan)
            self.radius_sight = int(game_param['Predator']['R_Predator_sight'])

            if self.radius_sight <= 0:
                raise ValueError(f"Invalid R_Predator_sight: {self.radius_sight}, must be > 0")

        except FileNotFoundError:
            raise ValueError(f"Config file not found at {FOLDER_CONFIG_PATH}")

        except Exception as e:
            raise ValueError(f"Error loading Predator parameters: {e}")

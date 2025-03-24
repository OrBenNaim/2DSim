import yaml
from src.constant import FOLDER_CONFIG_PATH
from src.entities.entity import Entity
from src.entities.herbivore import Herbivore
from src.entities.plant import Plant


class Predator(Entity):
    """Predators hunt herbivores and extend their lifespan when they eat."""
    def __init__(self, row, col):
        super().__init__(row, col)
        #self.predator_sight = 0    # Predators move towards the closest Herbivore they can see in R_predator_sight

    def load_entity_param_from_yaml(self):
        """ Load object's parameters (T_predator_steps, R_predator_sight) from .yaml file. """
        try:
            with open(FOLDER_CONFIG_PATH, "r") as file:
                config = yaml.safe_load(file)
            game_param = config.get("game_param", {})
            if 'Predator' not in game_param:
                raise ValueError("Missing 'Predator' parameters in game_param")
            if 'T_predator_steps' not in game_param['Predator']:
                raise ValueError("Missing 'T_predator_steps' for Predator")
            if 'R_predator_sight' not in game_param['Predator']:
                raise ValueError("Missing 'R_predator_sight' parameters in game_param")
            self.lifespan = game_param['Predator']['T_predator_steps']
            self.current_lifespan = self.lifespan
            self.predator_sight = game_param['Predator']['R_predator_sight']
            print(f"Loaded predator_sight: {self.predator_sight}")  # Debug
            if self.predator_sight <= 0:
                raise ValueError(f"Invalid R_predator_sight: {self.predator_sight}, must be > 0")
        except FileNotFoundError:
            raise ValueError(f"Config file not found at {FOLDER_CONFIG_PATH}")
        except Exception as e:
            raise ValueError(f"Error loading Predator parameters: {e}")

    # def load_entity_param_from_yaml(self):
    #     """ Load object's parameters (T_predator_steps, R_predator_sight) from .yaml file. """
    #     try:
    #         # Load configuration settings from a YAML file
    #         with open(FOLDER_CONFIG_PATH, "r") as file:
    #             config = yaml.safe_load(file)
    #
    #         game_param = config.get("game_param", {})
    #
    #         if 'Predator' not in game_param:
    #             raise ValueError("Missing 'Predator' parameters in game_param")
    #
    #         if 'T_predator_steps' not in game_param['Predator']:
    #             raise ValueError("Missing 'T_predator_steps' for Predator")
    #
    #         if 'R_predator_sight' not in game_param['Predator']:
    #             raise ValueError("Missing 'R_predator_sight' parameters in game_param")
    #
    #         self.lifespan = game_param['Predator']['T_predator_steps']
    #         self.current_lifespan = self.lifespan
    #
    #         self.predator_sight = game_param['Predator']['R_predator_sight']
    #
    #     except FileNotFoundError:
    #         raise ValueError(f"Config file not found at {FOLDER_CONFIG_PATH}")
    #
    #     except Exception as e:
    #         raise ValueError(f"Error loading Predator parameters: {e}")


    def move(self, grid):
        """ Move towards the closest herbivore they can see in a (herbivore_sight) radius
            or randomly if none are visible """
        if not self.is_alive():
            return

        old_row, old_col = self.row, self.col

        nearest_herbivore = self.find_nearest_herbivore(grid)
        print(f"nearest_herbivore_position: {nearest_herbivore}")

        if nearest_herbivore:
            self.move_towards(grid, nearest_herbivore)

        else:
            self.move_randomly(grid)

        # Update the grid: vacate old position and occupy new position
        if self.row != old_row or self.col != old_col:

            # Check if the new position had a plant
            if isinstance(grid.cells[self.row][self.col], Plant):
                grid.cells[self.row][self.col] = None  # Plant dies

            grid.cells[old_row][old_col] = None
            grid.update_empty_cells(old_row, old_col, is_occupied=False)

            grid.cells[self.row][self.col] = self
            grid.update_empty_cells(self.row, self.col, is_occupied=True)


    # def move_towards(self, grid, target):
    #     """ Moves one step towards the target herbivore. """
    #     target_row, target_col = target
    #
    #     if self.row < target_row:
    #         self.row += 1
    #
    #     elif self.row > target_row:
    #         self.row -= 1
    #
    #     if self.col < target_col:
    #         self.col += 1
    #
    #     elif self.col > target_col:
    #         self.col -= 1
    #
    #     # Check if predator reaches a herbivore
    #     if self.row == target_row and self.col == target_col:
    #         grid.cells[target_row][target_col] = None  # Herbivore dies
    #         grid.update_empty_cells(target_row, target_col, is_occupied=False)
    #         self.current_lifespan = self.lifespan  # Refuel lifespan


    # def find_nearest_herbivore(self, grid):
    #     """Finds the closest herbivore within sight radius."""
    #     closest_herbivore = None
    #     min_distance = float("inf")
    #
    #     rows, cols = grid.cells.shape  # Get dimensions from NumPy array
    #
    #     min_starting_row = max(0, self.row - self.predator_sight)
    #     max_starting_row = min(rows, self.row + self.predator_sight + 1)
    #
    #     min_starting_col = max(0, self.col - self.predator_sight)
    #     max_starting_col = min(cols, self.col + self.predator_sight + 1)
    #
    #     for row in range(min_starting_row, max_starting_row):
    #         for col in range(min_starting_col, max_starting_col):
    #
    #             if isinstance(grid.cells[row][col], Herbivore):
    #                 # Manhattan distance is a metric used to determine the distance between
    #                 # two points in a grid-like path
    #                 distance = abs(self.row - row) + abs(self.col - col)
    #
    #                 if distance < min_distance:
    #                     min_distance = distance
    #                     closest_herbivore = (row, col)
    #
    #     return closest_herbivore

    def find_nearest_herbivore(self, grid):
        """Finds the closest herbivore within sight radius."""
        closest_herbivore = None
        min_distance = float("inf")
        rows, cols = grid.cells.shape
        min_starting_row = max(0, self.row - self.predator_sight)
        max_starting_row = min(rows, self.row + self.predator_sight + 1)
        min_starting_col = max(0, self.col - self.predator_sight)
        max_starting_col = min(cols, self.col + self.predator_sight + 1)
        print(f"Predator at ({self.row}, {self.col}), sight: {self.predator_sight}")
        print(
            f"Search area: rows {min_starting_row} to {max_starting_row - 1}, cols {min_starting_col} to {max_starting_col - 1}")
        for row in range(min_starting_row, max_starting_row):
            for col in range(min_starting_col, max_starting_col):
                if isinstance(grid.cells[row][col], Herbivore):
                    distance = abs(self.row - row) + abs(self.col - col)
                    print(f"Found Herbivore at ({row}, {col}), distance: {distance}")
                    if distance < min_distance:
                        min_distance = distance
                        closest_herbivore = (row, col)
        print(f"Closest herbivore: {closest_herbivore}")
        return closest_herbivore
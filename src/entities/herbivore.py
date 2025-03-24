import numpy as np
import yaml
from src.entities.entity import Entity
from src.constant import FOLDER_CONFIG_PATH
from src.entities.plant import Plant


class Herbivore(Entity):
    """ Herbivore move towards plants, eat them and reproduce. """
    def __init__(self, row: int, col: int) -> None:
        super().__init__(row, col)          # Initialize base constructor
        self.herbivore_sight = 0            # Herbivores move towards the closest plant they can see
        self.reproduction_cooldown = 0      # Cooldown before it can reproduce again
        self.current_cooldown = 0           # Tracks cooldown progress


    def load_entity_param_from_yaml(self):
        """ Load object's parameters (T_herbivore_steps, R_herbivore_sight, T_cooldown_steps) from .yaml file. """
        try:
            # Load configuration settings from a YAML file
            with open(FOLDER_CONFIG_PATH, "r") as file:
                config = yaml.safe_load(file)

            game_param = config.get("game_param", {})

            if 'Herbivore' not in game_param:
                raise ValueError("Missing 'Herbivore' parameters in game_param")

            if 'T_herbivore_steps' not in game_param['Herbivore']:
                raise ValueError("Missing 'T_herbivore_steps' for Herbivore")

            if 'R_herbivore_sight' not in game_param['Herbivore']:
                raise ValueError("Missing 'R_herbivore_sight' parameters in game_param")

            if 'T_cooldown_steps' not in game_param['Herbivore']:
                raise ValueError("Missing 'T_cooldown_steps' parameters in game_param")

            self.lifespan = game_param['Herbivore']['T_herbivore_steps']
            self.current_lifespan = self.lifespan

            self.herbivore_sight = game_param['Herbivore']['R_herbivore_sight']
            self.reproduction_cooldown = game_param['Herbivore']['T_cooldown_steps']


        except FileNotFoundError:
            raise ValueError(f"Config file not found at {FOLDER_CONFIG_PATH}")

        except Exception as e:
            raise ValueError(f"Error loading Herbivore parameters: {e}")


    def move(self, grid):
        """ Move towards the closest plant they can see in a (herbivore_sight) radius
            or randomly if none are visible """

        if not self.is_alive():
            return  # Don't move if the herbivore is dead

        # Store the old position before moving
        old_row, old_col = self.row, self.col

        nearest_plant = self.find_nearest_plant(grid)

        if nearest_plant:
            self.move_towards(grid, nearest_plant)

        else:
            self.move_randomly(grid)


        # Check for reproduction only if we moved to a new position with another herbivore
        new_pos_occupied = (
                            (self.row != old_row or self.col != old_col) and
                            isinstance(grid.cells[self.row][self.col], Herbivore) and
                           grid.cells[self.row][self.col] is not self
        )

        if new_pos_occupied:
            self.reproduce(grid)

        # Update the grid: vacate old position and occupy new position
        if self.row != old_row or self.col != old_col:

            grid.cells[old_row][old_col] = None
            grid.update_empty_cells(old_row, old_col, is_occupied=False)

            grid.cells[self.row][self.col] = self
            grid.update_empty_cells(self.row, self.col, is_occupied=True)


    # def move_towards(self, target):
    #     """ Moves one step towards the target plant. """
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
    #     # Check if herbivore reaches a plant
    #     if self.row == target_row and self.col == target_col:
    #         self.current_lifespan = self.lifespan   # refueling the herbivore lifespan
    #


    def find_nearest_plant(self, grid):
        """Finds the closest plant within sight radius."""
        closest_plant = None
        min_distance = float("inf")

        rows, cols = grid.cells.shape  # Get dimensions from NumPy array

        min_starting_row = max(0, self.row - self.herbivore_sight)
        max_starting_row = min(rows, self.row + self.herbivore_sight + 1)

        min_starting_col = max(0, self.col - self.herbivore_sight)
        max_starting_col = min(cols, self.col + self.herbivore_sight + 1)

        for row in range(min_starting_row, max_starting_row):
            for col in range(min_starting_col, max_starting_col):

                if isinstance(grid.cells[row][col], Plant):

                    # Manhattan distance is a metric used to determine the distance between
                    # two points in a grid-like path
                    distance = abs(self.row - row) + abs(self.col - col)

                    if distance < min_distance:
                        min_distance = distance
                        closest_plant = (row, col)

        return closest_plant


    def reproduce(self, grid) -> None:
        """
        Herbivores reproduce when reaching another herbivore,
        staying in the same space and spawning another herbivore in a random empty neighboring cell.
        """

        # If the herbivore is in cooldown, reduce cooldown and return
        if self.current_cooldown > 0:
            self.current_cooldown -= 1
            return None

        empty_neighbors = grid.get_empty_neighbors(self.row, self.col)

        # If there are empty neighbors, choose one randomly and reproduce
        if empty_neighbors.size > 0:
            new_row, new_col = empty_neighbors[np.random.choice(len(empty_neighbors))]

            self.current_cooldown = self.reproduction_cooldown
            grid.cells[new_row, new_col] = Herbivore(new_row, new_col)
            grid.update_empty_cells(new_row, new_col, is_occupied=True)  # Mark cell as occupied
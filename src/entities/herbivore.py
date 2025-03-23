from random import random

import numpy as np
import yaml
from entity import Entity
from src.constant import FOLDER_CONFIG_PATH
from src.entities.plant import Plant


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
            self.current_lifespan = self.lifespan

            self.herbivore_sight = game_param['Herbivore']['R_herbivore_sight']
            self.reproduction_cooldown = game_param['Herbivore']['T_cooldown_steps']

        except Exception as e:
            print(f"Error loading file: {e}")


    def move(self, grid):
        """ Move towards the closest plant they can see in a (herbivore_sight) radius
            or randomly if none are visible """
        nearest_plant = self.find_nearest_plant(grid)
        if nearest_plant:
            self.move_towards(nearest_plant)

        else:
            self.move_randomly(grid)

        # Check if this herbivore reach another herbivore at his new position
        if isinstance(grid.cells[self.row][self.col], Herbivore) and grid.cells[self.row][self.col] is not self:
            self.reproduce(grid)

        grid.cells[self.row][self.col] = self   # Update the new location of this herbivore on the grid


    def find_nearest_plant(self, grid):
        """Finds the closest plant within sight radius."""
        closest_plant = None
        min_distance = float("inf")

        min_starting_row = max(0, self.row - self.herbivore_sight)
        max_starting_row = min(len(grid), self.row + self.herbivore_sight + 1)

        min_starting_col = max(0, self.col - self.herbivore_sight)
        max_starting_col = min(len(grid[0]), self.col + self.herbivore_sight + 1)

        for row in range(min_starting_row, max_starting_row):
            for col in range(min_starting_col, max_starting_col):

                if isinstance(grid[row][col], Plant):
                    distance = abs(self.row - row) + abs(self.col - col)

                    if distance < min_distance:
                        min_distance = distance
                        closest_plant = (row, col)

        return closest_plant


    def move_towards(self, target):
        """ Moves one step towards the target plant. """
        target_row, target_col = target

        if self.row < target_row:
            self.row += 1

        elif self.row > target_row:
            self.row -= 1

        if self.col < target_col:
            self.col += 1

        elif self.col > target_col:
            self.col -= 1

        # Check if herbivore reaches a plant
        if self.row == target_row and self.col == target_col:
            self.current_lifespan = self.lifespan  # refueling its life span


    def move_randomly(self, grid):
        """ Moves randomly to an empty cell on the grid. """
        if np.any(grid.empty_cells):  # Ensure there are still empty cells
            # Get the indices of empty cells
            empty_indices = np.argwhere(grid.empty_cells)

            # Randomly choose one empty cell
            chosen_cell = empty_indices[np.random.choice(len(empty_indices))]

            # Extract the new row and column for the herbivore
            new_row, new_col = chosen_cell[0], chosen_cell[1]

            # Update the empty cell array: mark the old cell as empty
            grid.update_empty_cells(self.row, self.col, is_occupied=False)

            # Move the herbivore to the chosen empty cell
            self.row, self.col = new_row, new_col

            # Update the empty cell array: mark the bew cell as occupied
            grid.update_empty_cells(new_row, new_col, is_occupied=True)

            # Mark the grid cell in the grid array as occupied
            grid.cells[self.row, self.col] = None  # Vacate the old position
            grid.cells[new_row, new_col] = self  # Mark the new position with the herbivore


    def reproduce(self, grid) -> None:
        """
        Herbivores reproduce when reaching another herbivore,
        staying in the same space and spawning another herbivore in a random empty neighboring cell.
        """

        # If the herbivore is in cooldown, reduce cooldown and return
        if self.current_cooldown > 0:
            self.current_cooldown -= 1
            return None

        # Possible movement directions (adjacent cells)
        directions = [
            (-1, -1), (-1, 0), (-1, 1),     # Top-left, Top, Top-right
            (0, -1), (0, 1),                # Left, Right
            (1, -1), (1, 0), (1, 1)         # Bottom-left, Bottom, Bottom-right
        ]

        # Use numpy vectorized operations to find empty neighboring cells
        empty_neighbors = []

        for dr, dc in directions:
            new_row, new_col = self.row + dr, self.col + dc

            # Check if the position is within bounds and the cell is empty
            if 0 <= new_row < len(grid.cells) and 0 <= new_col < len(grid.cells[0]) and grid.empty_cells[
                new_row, new_col]:
                empty_neighbors.append((new_row, new_col))

        # If there are any empty neighbors, randomly select one and create a new herbivore
        if empty_neighbors:
            # Randomly select one of the empty neighboring cells
            chosen_cell = empty_neighbors[np.random.choice(len(empty_neighbors))]
            new_row, new_col = chosen_cell

            # Reset reproduction cooldown
            self.current_cooldown = self.reproduction_cooldown

            # Create a new herbivore in the chosen cell
            grid.cells[new_row][new_col] = Herbivore(new_row, new_col)

            # Update the empty_cells array to reflect the new herbivore's presence
            grid.update_empty_cells(new_row, new_col, is_occupied=False)
from random import random
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
        """Moves randomly in one of the four directions."""
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        random.shuffle(directions)

        for d_row, d_col in directions:
            new_row, new_col = self.row + d_row, self.col + d_col

            if 0 <= new_row < len(grid) and 0 <= new_col < len(grid[0]) and grid[new_row][new_col] is None:
                self.row, self.col = new_row, new_col
                break


    def reproduce(self, grid) -> None:
        """ Staying in the same space and spawning another herbivore
            in a random neighboring cell if cooldown is over """
        if self.current_cooldown > 0:
            self.current_cooldown -= 1
            return None

        neighbors = [(self.row + dr, self.col + dc) for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]]
        random.shuffle(neighbors)

        for new_row, new_col in neighbors:
            if 0 <= new_row < len(grid) and 0 <= new_col < len(grid[0]) and grid[new_row][new_col] is None:

                self.current_cooldown = self.reproduction_cooldown  # Reset cooldown
                return Herbivore(new_row, new_col)
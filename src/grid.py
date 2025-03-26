import pygame
import numpy as np
import yaml
from src.constants import (SCREEN_HEIGHT, SCREEN_WIDTH, CELL_SIZE, FOLDER_CONFIG_PATH,
                           WHITE_COLOR, EMPTY_CELL_COLOR)

from src.entities.herbivore import Herbivore
from src.entities.plant import Plant
from src.entities.predator import Predator
from src.entities.fast_predator import FastPredator


class Grid:
    """ Defines the grid, cell toggling, and pattern handling. """

    def __init__(self) -> None:
        self.rows = SCREEN_HEIGHT // CELL_SIZE
        self.columns = SCREEN_WIDTH // CELL_SIZE
        self.cell_size = CELL_SIZE

        self.cells = np.full((self.rows, self.columns), None, dtype=object)      # grid is 2D numpy array
        self.empty_cells = np.ones((self.rows, self.columns), dtype=bool)   # True for empty cells, False for occupied

        self.font = pygame.font.SysFont('Segoe UI Emoji', self.cell_size // 2)  # Font for emoji

        # Dictionary to store mappings of entity names to their corresponding classes.
        # Keys: Class names as strings (e.g., "Plant", "Herbivore").
        # Values: The class reference (e.g., Plant, Herbivore).
        self.existing_entities = {"FastPredator": FastPredator, "Plant": Plant, "Herbivore": Herbivore,
                                  "Predator": Predator}

    def update_empty_cells(self, row: int, col: int, is_occupied=True):
        """ Update the empty cells array when a cell becomes occupied or empty. """
        self.empty_cells[row, col] = not is_occupied


    def add_object_to_grid(self, obj_name: str, x: int, y: int) -> None:
        """ Places an object at (x, y) in the grid """

        if obj_name not in self.existing_entities:
            raise ValueError(f"Error: Unknown object '{obj_name}' at ({x}, {y})")

        if 0 <= y < self.rows and 0 <= x < self.columns:
            obj_instance = self.existing_entities[obj_name](y, x)     # Create an instance of obj
            obj_instance.load_entity_param_from_yaml()                # Load object's parameters

            self.cells[y][x] = obj_instance                           # Add instance to the grid.cells
            self.update_empty_cells(y, x, is_occupied=True)           # Mark this cell as occupied

        else:
            raise ValueError(f"\n{(x, y)} outside the grid's bounds")

    def load_param_from_yaml(self) -> None:
        """ Loads a seed configuration from a YAML file and initializes the entities in the simulation. """

        try:
            with open(FOLDER_CONFIG_PATH, "r", encoding="utf-8") as file:
                config = yaml.safe_load(file)

            seed = config.get("seed", {})

            for obj_name, position_list in seed.items():
                for pos in position_list:
                    self.add_object_to_grid(obj_name, pos['x'], pos['y'])

        except Exception as e:
            raise ValueError(f"Error loading file: {e}") from e

    def draw(self, screen):
        """ Draws the grid on the provided pygame screen.
            Each cell is drawn as a rectangle,
            with its color depending on whether the cell is empty or occupied. """

        # Create a color array with the shape of the grid and an additional dimension for RGB
        colors = np.zeros((self.rows, self.columns, 3), dtype=np.uint8)

        # Set the color of empty cells (cells containing None) to EMPTY_CELL_COLOR.
        # np.equal(self.cells, None) creates a boolean mask,
        # where each element is True if the corresponding cell is None.
        # This mask is then used to assign EMPTY_CELL_COLOR to the matching positions in the colors array.
        colors[np.equal(self.cells, None)] = EMPTY_CELL_COLOR

        # Draw the grid using the color array
        for row, col in np.ndindex(self.cells.shape):
            pygame.draw.rect(screen, colors[row, col],
                             (col * self.cell_size, row * self.cell_size,
                              self.cell_size - 1, self.cell_size - 1))

            # If the cell is not empty, render the corresponding emoji
            if self.cells[row][col] is not None:
                entity = self.cells[row][col]

                text = self.font.render(entity.emoji, True, WHITE_COLOR)  # White text for emoji
                text_rect = text.get_rect(center=(col * self.cell_size + self.cell_size // 2,
                                                  row * self.cell_size + self.cell_size // 2))
                screen.blit(text, text_rect)

    def get_empty_neighbors(self, ref_row: int, ref_col: int) -> np.ndarray:
        """ Returns empty neighboring cells as a NumPy array """

        # Possible movement directions (adjacent cells)
        directions = np.array([
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ])

        # Compute new positions
        neighbors_positions = directions + np.array([ref_row, ref_col])

        # Ensure positions are within bounds
        rows, cols = self.cells.shape

        # in_bounds is a Boolean NumPy array (mask) that indicates
        # which neighboring positions are within the grid boundaries.
        in_bounds = ((0 <= neighbors_positions[:, 0]) &     # Extracts the row indices of the neighboring positions.
                     (neighbors_positions[:, 0] < rows) &   # Extracts the column indices of the neighboring positions.
                     (0 <= neighbors_positions[:, 1]) &     # Checks if the row indices are within bounds.
                     (neighbors_positions[:, 1] < cols))    # Checks if the column indices are within bounds.

        # Extract only valid positions
        valid_neighbors = neighbors_positions[in_bounds]

        # Extract only empty neighbors into a NumPy array
        empty_neighbors = valid_neighbors[self.empty_cells[valid_neighbors[:, 0], valid_neighbors[:, 1]]]

        return empty_neighbors

    def add_random_plant(self):
        """
        Adds a new Plant object to a random empty cell on the grid.
        The method:
        1. Checks if there are any empty cells.
        2. Finds all empty cell indices.
        3. Selects a random empty cell.
        4. Places a new Plant at that position.
        """

        # Checks if there are any empty cells
        if np.any(self.empty_cells):
            empty_indexes = np.argwhere(self.empty_cells)   # Finds all empty cell indices

            # Select a random empty cell
            new_row, new_col = empty_indexes[np.random.choice(len(empty_indexes))]

            # Places a new Plant at that position
            self.add_object_to_grid("Plant", new_col, new_row)

            # Mark the cell as occupied
            self.empty_cells[new_row, new_col] = False

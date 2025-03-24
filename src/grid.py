import pygame
import numpy as np
import yaml
from src.constant import *
from src.entities.herbivore import Herbivore
from src.entities.plant import Plant
from src.entities.predator import Predator


class Grid:
    """ Defines the grid, cell toggling, and pattern handling. """

    def __init__(self) -> None:
        self.rows = SCREEN_HEIGHT // CELL_SIZE
        self.columns = SCREEN_WIDTH // CELL_SIZE
        self.cell_size = CELL_SIZE

        self.cells = np.full((self.rows, self.columns), None, dtype=object)      # grid is 2D numpy array
        self.empty_cells = np.ones((self.rows, self.columns), dtype=bool)   # True for empty cells, False for occupied

        self.font = pygame.font.SysFont('Segoe UI Emoji', self.cell_size // 2)  # Font for emoji

        # Define emojis for different entities
        self.entity_emojis = {
            "Plant": "🌱",  # Plant emoji
            "Herbivore": "🐔",  # Herbivore emoji (chicken)
            "Predator": "🦊",  # Predator emoji (fox)
        }

        # Define mapping of entity names to classes
        self.entity_classes = {
            "Plant": Plant,
            "Herbivore": Herbivore,
            "Predator": Predator
        }

    def update_empty_cells(self, row, col, is_occupied=True):
        """Update the empty cells array when a cell becomes occupied or free."""
        if is_occupied:
            self.empty_cells[row, col] = False  # Cell is occupied, mark as False

        else:
            self.empty_cells[row, col] = True  # Cell is free, mark as True


    def add_object(self, obj_name: str, x: int, y: int) -> None:
        """ Places an object at (x, y) in the grid """

        if obj_name not in self.entity_classes:
            raise ValueError(f"Error: Unknown object '{obj_name}' at ({x}, {y})")

        if 0 <= y < self.rows and 0 <= x < self.columns:
            obj_instance = self.entity_classes[obj_name](y, x)    # Create an instance of obj

            self.cells[y][x] = obj_instance

            self.update_empty_cells(y, x, is_occupied=True)


    def draw(self, screen):
        """ Draws the grid on the provided pygame screen.
            Each cell is drawn as a rectangle,
            with its color depending on whether the cell is empty or occupied. """

        # Create a color array with the shape of the grid and an additional dimension for RGB
        colors = np.zeros((self.rows, self.columns, 3), dtype=np.uint8)

        # Set the color of empty cells (cells containing None) to EMPTY_CELL_COLOR.
        # np.equal(self.cells, None) creates a boolean mask where each element is True if the corresponding cell is None.
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
                emoji = self.entity_emojis.get(entity.__class__.__name__, "❓")  # Default emoji if no match

                text = self.font.render(emoji, True, WHITE_COLOR)  # White text for emoji
                text_rect = text.get_rect(center=(col * self.cell_size + self.cell_size // 2,
                                                  row * self.cell_size + self.cell_size // 2))
                screen.blit(text, text_rect)


    def clear(self):
        self.cells = np.zeros((self.rows, self.columns), dtype=object)


    def get_empty_neighbors(self, ref_row, ref_col) -> np.ndarray:
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


    def load_seed(self) -> None:
        try:
            with open(FOLDER_CONFIG_PATH, "r") as file:
                config = yaml.safe_load(file)

            seed = config.get("seed", {})

            for obj_name, position_list in seed.items():
                for pos in position_list:

                    self.add_object(obj_name, pos['x'], pos['y'])

        except Exception as e:
            raise ValueError(f"Error loading file: {e}")
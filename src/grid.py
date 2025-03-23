from typing import Type
import pygame
import numpy as np
import yaml
from src.constant import *
from src.entities.entity import Entity

class Grid:
    """ Defines the grid, cell toggling, and pattern handling. """

    def __init__(self) -> None:
        self.rows = SCREEN_HEIGHT // CELL_SIZE
        self.columns = SCREEN_WIDTH // CELL_SIZE
        self.cell_size = CELL_SIZE

        self.cells = np.zeros((self.rows, self.columns), dtype=object)      # grid is 2D numpy array
        self.empty_cells = np.ones((self.rows, self.columns), dtype=bool)   # True for empty cells, False for occupied


    def update_empty_cells(self, row, col, is_occupied=True):
        """Update the empty cells array when a cell becomes occupied or free."""
        if is_occupied:
            self.empty_cells[row, col] = False  # Cell is occupied, mark as False
        else:
            self.empty_cells[row, col] = True  # Cell is free, mark as True


    def load_seed(self) -> None:
        """ Load an initial seed from a .yaml file into the grid.cells """
        try:
            # Load configuration settings from a YAML file
            with open(FOLDER_CONFIG_PATH, "r") as file:
                config = yaml.safe_load(file)

            seed = config.get("seed", {})

            for obj, position_list in seed:
                for pos in position_list:
                    self.add_object(obj, pos['x'], pos['y'])

        except Exception as e:
            print(f"Error loading file: {e}")


    def add_object(self, obj: Type[Entity], x: int, y: int):
        """ Places an object at (x, y) in the grid """
        if 0 <= x < self.columns and 0 <= y < self.rows:
            self.cells[y][x] = obj(y, x)
            self.update_empty_cells(y, x, is_occupied=True)

    def draw(self, screen):
        """ Draws the grid on the provided pygame screen.
            Each cell is drawn as a rectangle,
            with its color depending on whether the cell is alive or dead. """

        # Create a color array with the shape of the grid and an additional dimension for RGB
        colors = np.zeros((self.rows, self.columns, 3), dtype=np.uint8)

        # Set the colors based on the cell values
        colors[self.cells == 1] = (255, 255, 255)  # Live cells
        colors[self.cells == 0] = (30, 30, 30)  # Dead cells

        # Draw the grid using the color array
        for row, col in np.ndindex(self.cells.shape):
            pygame.draw.rect(screen, colors[row, col],
                             (col * self.cell_size, row * self.cell_size,
                              self.cell_size - 1, self.cell_size - 1))


    def fill_random(self):
        # Use numpy random.choice to fill the grid with random values
        # p=[0.25, 0.75] defines the probabilities for selecting 1 or 0
        self.cells = np.random.choice(a=[1, 0], size=(self.rows, self.columns), p=[0.25, 0.75])


    def clear(self):
        self.cells = np.zeros((self.rows, self.columns), dtype=object)


    def toggle_cell_state(self, row, col):
        """ Toggles the state of a cell at the specified row and column.
            If the cell is alive (1), it becomes dead (0), and vice versa. """

        # Validate the cell index to ensure it's within the grid bounds
        if 0 <= row < self.rows and 0 <= col < self.columns:
            self.cells[row][col] = not self.cells[row][col]
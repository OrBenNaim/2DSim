import pygame
import numpy as np
from src.constants import *


class Grid:
    """ Defines the grid, cell toggling, and pattern handling """

    def __init__(self) -> None:
        self.rows = SCREEN_HEIGHT // CELL_SIZE
        self.columns = SCREEN_WIDTH // CELL_SIZE
        self.cell_size = CELL_SIZE

        self.cells = np.zeros((self.rows, self.columns), dtype=np.bool_)  # grid is 2D numpy array

    def draw(self, screen):
        """ Draws the grid on the provided pygame screen.
            Each cell is drawn as a rectangle,
            with its color depending on whether the cell is alive or dead """

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

    def load_from_file(self, filename: str):
        """ Load an initial pattern from a text file and resize the grid if needed, centered. """
        try:
            with open(filename, 'r') as f:
                lines = [line.strip() for line in f.readlines()]  # Save stripped lines in a list

            # Determine the pattern's size
            pattern_rows = len(lines)
            pattern_columns = max(len(line.strip()) for line in lines) if lines else 0  # Use saved list

            # Resize the grid if necessary
            if pattern_rows > self.rows or pattern_columns > self.columns:
                self.rows = pattern_rows
                self.columns = pattern_columns
                self.cells = np.zeros((self.rows, self.columns), dtype=np.bool_)  # Recreate the grid with new size

            else:
                self.clear()  # Clear the grid before loading

            # Calculate the starting position to center the pattern
            start_row = (self.rows - pattern_rows) // 2
            start_col = (self.columns - pattern_columns) // 2

            for row, line in enumerate(lines):

                for col, char in enumerate(line):

                    if char in LIVE_CELL_CHARS:
                        self.cells[row + start_row][col + start_col] = 1

                    elif char in DEAD_CELL_CHARS:
                        self.cells[row + start_row][col + start_col] = 0

        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")

        except Exception as e:
            print(f"Error loading file: {e}")

    def fill_random(self):
        # Use numpy random.choice to fill the grid with random values
        # p=[0.25, 0.75] defines the probabilities for selecting 1 or 0
        self.cells = np.random.choice(a=[1, 0], size=(self.rows, self.columns), p=[0.25, 0.75])

    def clear(self):
        self.cells = np.zeros((self.rows, self.columns), dtype=np.bool_)

    def toggle_cell_state(self, row, col):
        """ Toggles the state of a cell at the specified row and column.
            If the cell is alive (1), it becomes dead (0), and vice versa """

        # Validate the cell index to ensure it's within the grid bounds
        if 0 <= row < self.rows and 0 <= col < self.columns:
            self.cells[row][col] = not self.cells[row][col]

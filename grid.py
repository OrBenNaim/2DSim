import random, pygame
import numpy as np


class Grid:
    """ Defines the grid, cell toggling, and pattern handling """

    def __init__(self, screen_width: int, screen_height: int, cell_size: int) -> None:
        self.rows = screen_height // cell_size
        self.columns = screen_width // cell_size
        self.cell_size = cell_size

        self.cells = np.zeros((self.rows, self.columns), dtype=int)     # grid is 2D numpy array


    def draw(self, screen):
        for row, col in np.ndindex(self.cells.shape):
            color = (255, 255, 255) if self.cells[row][col] else (30, 30, 30)
            pygame.draw.rect(screen, color,
                             (col * self.cell_size, row * self.cell_size,
                              self.cell_size - 1, self.cell_size - 1))


    def load_from_file(self, filename: str):
        """ Load an initial pattern from a text file and resize the grid if needed, centered. """
        try:
            with open(filename, 'r') as f:
                lines = f.readlines()

            # Determine the pattern's size
            pattern_rows = len(lines)
            pattern_columns = max(len(line.strip()) for line in lines)

            # Resize the grid if necessary
            if pattern_rows > self.rows or pattern_columns > self.columns:
                self.rows = pattern_rows
                self.columns = pattern_columns
                self.cells = np.zeros((self.rows, self.columns), dtype=int)  # Recreate the grid with new size

            self.clear()  # Clear the grid before loading

            # Calculate the starting position to center the pattern
            start_row = (self.rows - pattern_rows) // 2
            start_col = (self.columns - pattern_columns) // 2

            for row, line in enumerate(lines):
                line = line.strip()

                for col, char in enumerate(line):

                    if row + start_row < self.rows and col + start_col < self.columns:

                        if char in ('1', 'X', 'O'):  # Interpret live cells
                            self.cells[row + start_row][col + start_col] = 1

                        elif char in ('0', '.', '-'):  # Interpret dead cells
                            self.cells[row + start_row][col + start_col] = 0

        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")

        except Exception as e:
            print(f"Error loading file: {e}")


    def fill_random(self):
        for row in range(self.rows):
            for column in range(self.columns):
                self.cells[row][column] = random.choice([1, 0, 0, 0])

    def clear(self):
        for row, col in np.ndindex(self.cells.shape):
            self.cells[row][col] = 0


    def toggle_cell(self, row, col):

        # Validate the cell index
        if 0 <= row < self.rows and 0 <= col < self.columns:
            self.cells[row][col] = 1 - self.cells[row][col]
import random, pygame
import numpy as np


class Grid:
    """ The class 'Grid' creates the cells, toggle specific cell's state, draw cells on the pygame screen, etc. """

    def __init__(self, width: int, height: int, cell_size: int) -> None:
        self.rows = height // cell_size
        self.columns = width // cell_size
        self.cell_size = cell_size

        self.cells = np.zeros((self.rows, self.columns), dtype=int)     # grid is 2D numpy array


    def draw(self, screen):
        for row, col in np.ndindex(self.cells.shape):
            color = (255, 255, 255) if self.cells[row][col] else (10, 10, 10)
            pygame.draw.rect(screen, color,
                             (col * self.cell_size, row * self.cell_size,
                              self.cell_size - 1, self.cell_size - 1))


    def load_from_file(self, filename: str):
        """ Load an initial pattern from a text file. """
        try:
            with open(filename, 'r') as f:
                lines = f.readlines()

            self.clear()  # Clear the grid before loading
            for row, line in enumerate(lines):
                line = line.strip()
                for col, char in enumerate(line):
                    if row < self.rows and col < self.columns:
                        if char in ('1', 'X', 'O'):  # Interpret live cells
                            self.cells[row][col] = 1
                        elif char in ('0', '.', '-'):  # Interpret dead cells
                            self.cells[row][col] = 0
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
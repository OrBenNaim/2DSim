import sys
import numpy as np
import time
import os
import pygame
from typing import Any


class Simulation:
    """ The Simulation class handles the different states of the game
        and responsible for operating the simulation itself """

    def __init__(self, filename:str, generations: int = 100, delay: int=250):
        """Initialize the game with a grid loaded from a file """
        self.filename = filename
        self.grid = self.load_pattern()   # grid is 2D numpy array
        self.gen = generations
        self.delay = delay
        self.running = True     # This variable store the pygame screen's status

        # Constants
        self.CELL_SIZE = 10  # Size of each cell in pixels
        self.GRID_WIDTH = 80  # Number of columns
        self.GRID_HEIGHT = 60  # Number of rows
        self.SCREEN_WIDTH = self.GRID_WIDTH * self.CELL_SIZE
        self.SCREEN_HEIGHT = self.GRID_HEIGHT * self.CELL_SIZE
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)

        # Initialize Pygame
        pygame.init()
        self.window = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Conway's Game of Life")
        self.clock = pygame.time.Clock()
        self.FPS = 12

    # -----------------------------------------------------------------------------------------------------------------------
    def load_pattern(self) -> np.ndarray:
        """ This function responsible to open the given file and to create the grid as 2D numpy array """
        with open(self.filename, "r") as file:
            lines = file.readlines()

        # For each line in the file, check each cell status (live\die) and create 2D array accordingly
        grid = np.array([[1 if cell == 'O' else 0 for cell in line.strip()] for line in lines])
        return grid

    # -----------------------------------------------------------------------------------------------------------------------
    def display(self) -> None:
        """ This function display the grid at its current state with pygame """
        self.window.fill(self.BLACK)
        rows, cols = self.grid.shape
        for row in range(rows):
            for col in range(cols):
                if self.grid[row][col]:
                    pygame.draw.rect(self.window, self.WHITE, (col * self.CELL_SIZE, row * self.CELL_SIZE,
                                                               self.CELL_SIZE, self.CELL_SIZE))
        pygame.display.update()


    # -----------------------------------------------------------------------------------------------------------------------
    def count_live_neighbors(self, ref_row: int, ref_col: int) -> int:
        """ This function counts how many live neighbors exist for a specific cell """
        counter = 0

        # In reference to the cell itself, the indexes of his neighbors are
        # always constants.
        # if cell is grid[ref_row][ref_col] so:
        # neighbor1 is grid[ref_row - 1][ref_col - 1]   # upper_left
        # neighbor2 is grid[ref_row - 1][ref_col]       # upper_mid
        # and so on.

        neighbors_shifts = [
            (-1, -1), (-1, 0), (-1, 1),  # upper_left, upper_mid, upper_right
            (0, -1), (0, 1),  # mid_left, mid_right
            (1, -1), (1, 0), (1, 1),  # upper_left, upper_mid, upper_right
        ]

        # Get the number of rows and columns
        rows, cols = self.grid.shape

        # Calculate the neighbors indexes for each cell on the grid
        for shift_row, shift_col in neighbors_shifts:
            neighbor_row_idx, neighbor_col_idx = shift_row + ref_row, shift_col + ref_col

            # Check if the neighbor's indexes are valid indexes
            if 0 <= neighbor_row_idx < rows and 0 <= neighbor_col_idx < cols:
                counter += self.grid[neighbor_row_idx, neighbor_col_idx]

        return counter

    # -----------------------------------------------------------------------------------------------------------------------
    def update_grid(self) -> None:
        """ This function calculates and creates the next state of the grid according to the game rules """
        # Get the number of rows and columns
        rows, cols = self.grid.shape

        # Create new grid to the next generation.
        # Changing specific cell on the current grid will damage other cells.
        updated_grid = np.zeros((rows, cols), dtype=int)

        # For each cell, update his status accordingly to his living neighbors and the game rules
        for row in range(rows):  # 0 <= row <= len(rows) - 1
            for col in range(cols):  # 0 <= col <= len(rows) - 1
                cnt_live_neighbors = self.count_live_neighbors(row, col)

                # Live cell
                if self.grid[row][col]:

                    # A case of a live cell that lives to the next generation
                    if cnt_live_neighbors == 2 and cnt_live_neighbors == 3:
                        updated_grid[row][col] = 1

                # Dead cell
                else:
                    if cnt_live_neighbors == 3:
                        updated_grid[row][col] = 1

        self.grid = updated_grid

    # -----------------------------------------------------------------------------------------------------------------------
    def run(self) -> None:
        """ Runs the Game of Life simulation """
        gen = 0

        while self.running and gen < self.gen:

            # 1. Event Handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    sys.exit()

                self.display_window()
                self.update_grid()
                pygame.time.delay(self.delay)
                gen += 1

        pygame.quit()


#-----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    # Display the existing initial patterns and allow the user to select one of them
    selected_file = get_file_from_initial_patterns_folder("initial_patterns")

    game = GameOfLife(selected_file, generations=100000, delay=3000)
    game.run()


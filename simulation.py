import numpy as np
from grid import Grid


class Simulation:
    """ The 'Simulation' class handles the different states of the game
        and updates the grid object accordingly.
        This class functions as pipeline between the main() function and the grid class """

    def __init__(self, width: int, height: int, cell_size: int) -> None:
        """Initialize the game simulation """
        self.grid = Grid(width, height, cell_size)          # Create new grid object for the current simulation
        self.temp_grid = Grid(width, height, cell_size)     # It will be used at the update() function

        self.running = False    # This flag indicates if the simulation running or not

    def draw(self, screen):
        self.grid.draw(screen)


    def update_grid(self) -> None:
        """ This function calculates and creates the next state of the grid according to the game rules """

        if self.is_running():

            # For each cell, update his status accordingly to his living neighbors and the game rules
            for row, col in np.ndindex(self.grid.cells.shape):

                # Count how many neighbors are alive.
                # Keep it mind that the neighbors cell located in the range:
                # (row-1) <= row < row+2, (col-1) <= col < col+2,

                cnt_live_neighbors = np.sum(self.grid.cells[row - 1 : row + 2, col - 1 : col + 2]) - self.grid.cells[row][col]

                cell_value = self.grid.cells[row][col]

                # Live cell
                if cell_value == 1:

                    # A case of a live cell that dying
                    if cnt_live_neighbors > 3 or cnt_live_neighbors < 2:
                        self.temp_grid.cells[row][col] = 0

                    # A case of a live cell that lives to the next generation
                    if cnt_live_neighbors == 2 or cnt_live_neighbors == 3:
                        self.temp_grid.cells[row][col] = 1

                # Dead cell
                else:
                    if cnt_live_neighbors == 3:
                        self.temp_grid.cells[row][col] = 1

                    else:
                        self.temp_grid.cells[row][col] = 0

            self.grid.cells = self.temp_grid.cells.copy()   # Update the original grid.cells at the end of the operation


    def is_running(self):
        return self.running


    def start(self):
        self.running = True


    def stop(self):
        self.running = False


    def clear(self):
        if not self.is_running():
            self.grid.clear()


    def create_random_pattern(self):
        if not self.is_running():
            self.grid.fill_random()


    def load_pattern_from_file(self, filename: str):
        if not self.is_running():
            self.grid.load_from_file(filename)


    def toggle_cell(self, row, col):
        if not self.is_running():
            self.grid.toggle_cell(row, col)

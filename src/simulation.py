import sys
import time
import numpy as np
import pygame
from src.grid import Grid
from src.constants import *
from src.utils import get_file_from_initial_patterns_folder
from scipy.signal import convolve2d


class Simulation:
    """ Manages the game logic, updates the grid, handles user input and events.
        This class functions as a pipeline between the main() function and the grid class. """

    def __init__(self) -> None:
        """Initialize the game simulation """
        self.grid = Grid()          # Create a new grid object for the current simulation
        self.temp_grid = Grid()     # It will be used at the update() function
        self.running = False        # This flag indicates if the simulation running or not

    def count_live_neighbors(self) -> np.ndarray:
        """ Counts how many live neighbors exist for a specific cell """
        kernel = np.array([
            [1, 1, 1],
            [1, 0, 1],
            [1, 0, 1]
        ])

        neighbors_grid = convolve2d(self.grid.cells, kernel, mode='same', boundary='fill', fillvalue=0)
        return neighbors_grid

    def update_grid(self) -> None:
        """ Updates the grid to the next state according to the game rules """
        if self.running:

            neighbors_grid = self.count_live_neighbors()
            cells_values = self.grid.cells

            self.temp_grid.cells = np.where(
                ((cells_values == 1) & ((neighbors_grid == 2) | (neighbors_grid == 3))
                 |
                ((cells_values == 0) | (neighbors_grid == 3)), 1, 0))

            self.grid.cells = self.temp_grid.cells.copy()  # Update the original grid.cells at the end of the operation

    def clear(self):
        if not self.running:
            self.grid.clear()

    def create_random_pattern(self):
        if not self.running:
            self.grid.fill_random()

    def load_pattern_from_file(self, filename: str):
        if not self.running:
            self.grid.load_from_file(filename)

    def toggle_cell_state(self, row, col):
        if not self.running:
            self.grid.toggle_cell_state(row, col)
            
    def get_user_preference(self):
        """ This function allows the user to choose to initialize the pattern with text file or manually """

        while True:
            use_text_file_for_pattern = input(
                "\nDo you want to use text file for the initial pattern? (Press Y/N)\n").lower()

            if use_text_file_for_pattern == 'y' or use_text_file_for_pattern == 'n':
                break
            else:
                print("You entered wrong input. Please try again")

        if use_text_file_for_pattern == 'y':
            file_path = get_file_from_initial_patterns_folder(PATTERN_FOLDER)
            if file_path:
                self.load_pattern_from_file(file_path)
                self.running = True

    def event_handler(self):
        """
        Handles various events in the game, including quitting, mouse clicks, and key presses.

        This method processes user interactions like clicking cells to toggle their state,
        starting and stopping the simulation with the Enter and Space keys, and triggering
        actions for random pattern creation, grid clearing, or loading a pattern from a file
        when specific keys are pressed.

        Handle the following events:
        - QUIT: Closes the pygame window.
        - MOUSEBUTTONDOWN: Toggles the state of the cell that the mouse was clicked on.
        - KEYDOWN:
            - ENTER: Starts the simulation.
            - SPACE: Stops the simulation.
            - R: Generates a random initial pattern.
            - C: Clears the grid.
            - L: Loads a pattern from a file.
        """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # If the user presses on a specific cell with his mouse, change the cell state
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row = pos[1] // self.grid.cell_size
                column = pos[0] // self.grid.cell_size
                self.toggle_cell_state(row, column)

            # If the user presses on the keyboard, check it
            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:  # Start the simulation if the user presses the 'Enter' key
                    self.running = True
                    pygame.display.set_caption("Game of Life is running")

                elif event.key == pygame.K_SPACE:  # Stop the simulation if the user presses the 'Space' key
                    self.running = False
                    pygame.display.set_caption("Game of Life has stopped")

                elif event.key == pygame.K_r:  # Create a random initial pattern if the user presses the 'r' key
                    self.create_random_pattern()

                elif event.key == pygame.K_c:  # Clear the grid if the user presses the 'c' key
                    self.clear()

                elif event.key == pygame.K_l:  # Load pattern (centered)
                    file_path = get_file_from_initial_patterns_folder(PATTERN_FOLDER)
                    if file_path:
                        self.load_pattern_from_file(file_path)
                        self.running = True
    
    def run(self):
        """ This function handles the simulation itself """
        
        # Let the user choose how he would like to initialize the pattern
        self.get_user_preference()
        
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Game of Life")

        # Simulation Loop
        while True:

            # 1. Event Handling
            self.event_handler()

            # 2. Updating the state of the grid
            self.update_grid()

            # 3. Drawing
            screen.fill(BG_COLOR)
            self.grid.draw(screen)

            pygame.display.update()

            time.sleep(DELAY)  # Add DELAY

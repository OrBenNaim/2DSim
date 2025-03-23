import sys
import time
import pygame

from src.entities.herbivore import Herbivore
from src.entities.plant import Plant
from src.entities.predator import Predator
from src.grid import Grid
from src.constant import *


class Simulation:
    """ Manages the game logic, updates the grid, handles user input and events.
        This class functions as a pipeline between the main() function and the grid class. """

    def __init__(self) -> None:
        """Initialize the game simulation """
        self.grid = Grid()          # Create a new grid object for the current simulation
        self.temp_grid = Grid()     # It will be used at the update() function
        self.running = False        # This flag indicates if the simulation running or not


    def update_grid(self) -> None:
        """ Updates the grid to the next state according to the game rules """
        if self.running:

            rows, cols = self.grid.cells.shape

            for row in range(rows):
                for col in range(cols):
                    obj = self.grid.cells[row][col]

                    # obj is plant
                    if isinstance(obj, Plant):
                        obj.lifespan -= 1  # Reduce lifespan
                        if obj.lifespan <= 0:
                            self.temp_grid.cells[row][col] = None  # Plant dies

                    # obj is herbivore
                    elif isinstance(obj, Herbivore):
                        obj.move(self.grid)         # Let the herbivore move

                        obj.lifespan -= 1           # Reduce lifespan
                        if obj.lifespan <= 0:
                            self.temp_grid.cells[row][col] = None  # Herbivore dies

                    # obj is predator
                    elif isinstance(obj, Predator):
                        obj.move(self.grid)         # Let the predator move
                        obj.reproduce(self.grid)    # Check if it can reproduce

                        obj.lifespan -= 1           # Reduce lifespan
                        if obj.lifespan <= 0:
                            self.temp_grid.cells[row][col] = None  # Herbivore dies


            self.grid.cells = self.temp_grid.cells.copy()  # Update the original grid.cells at the end of the operation


    def clear(self):
        if not self.running:
            self.grid.clear()


    def create_random_pattern(self):
        if not self.running:
            self.grid.fill_random()


    def load_seed_from_yaml(self):
        if not self.running:
            self.grid.load_seed()


    def event_handler(self):
        """
        Handles various events in the game, including quitting, mouse clicks, and key presses.

        This method processes user interactions like starting and stopping the simulation with the Enter and Space keys,
        and triggering actions for random pattern creation, grid clearing, or loading a pattern from a file
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


    def run(self):
        """ This function handles the simulation itself """
        self.grid.load_seed()   # Initialize the grid for the first time from .yaml file configuration

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

            time.sleep(DELAY)  # Add time DELAY
import sys
import time
import numpy as np
import pygame
from src.entities.mobile_entity import MobileEntity
from src.events.event_manager import EventsManager
from src.events.event_name import EventName
from src.events.observers import HerbivoreExtinctionAlert, PredatorEatsHerbivoreAlert, PlantsExceedsAlert
from src.grid import Grid
from src.constants import DELAY, BG_COLOR, SCREEN_WIDTH, SCREEN_HEIGHT


class Simulation:
    """ Manages the game logic, updates the grid, handles user input and events.
        This class functions as a pipeline between the main() function and the grid class. """

    def __init__(self) -> None:
        """Initialize the game simulation """
        self.running = False
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Game of Life")

        self.grid = Grid()  # Create a new grid object for the current simulation
        self.temp_grid = Grid()  # It will be used at the update() function

        self.events_manager = EventsManager(self.grid)

    def update_grid(self) -> None:
        """ Updates the grid to the next state according to the game rules """

        if self.running:
            self.temp_grid.cells = self.grid.cells.copy()  # Sync at start

            # The order of operations based on the place in the grid (left to right)
            for row, col in np.ndindex(self.grid.cells.shape):
                obj = self.grid.cells[row][col]

                if obj is None:
                    continue  # Pass for empty cells

                if not obj.is_alive():
                    continue  # Pass for a static object like Tree Or Rock in the future

                obj.decrease_current_lifespan()  # Reduce object's lifespan

                if obj.get_current_lifespan() <= 0:
                    self.temp_grid.cells[row][col] = None  # Object dies

                # obj is herbivore or predator
                if isinstance(obj, MobileEntity):
                    obj.move(self.temp_grid)  # Let the herbivore\predator move

                self.events_manager.check_herbivore_extinction()
                #self.events_manager.check_predator_eats_herbivore()
                self.events_manager.check_plant_overgrowth(overgrown=0.9)

            self.temp_grid.add_random_plant()  # Plants appear randomly at empty spaces

            self.grid.cells = self.temp_grid.cells.copy()  # Update the original grid.cells at the end of the operation

    def run(self):
        """ This function handles the simulation itself """
        self.running = True
        self.grid.load_param_from_yaml()  # Initialize the grid for the first time from .yaml file configuration

        herbivore_extinct_alert = HerbivoreExtinctionAlert(event_name=EventName.HERBIVORE_EXTINCTION,
                                                           msg="All Herbivores are extinct")

        self.events_manager.add_observer(observer=herbivore_extinct_alert)

        predator_eats_herbivore_alert = PredatorEatsHerbivoreAlert(event_name=EventName.PREDATOR_EATS_HERBIVORE,
                                                                   msg="Predator eat Herbivore")

        self.events_manager.add_observer(observer=predator_eats_herbivore_alert)

        plants_exceeds_alert = PlantsExceedsAlert(event_name=EventName.PLANT_OVERGROWTH,
                                                  msg="Plants exceeds 90% of the grid space")

        self.events_manager.add_observer(observer=plants_exceeds_alert)

        # Simulation Loop
        while True:
            # 1. Event Handling
            self.event_handler()

            # 2. Updating the state of the grid
            self.update_grid()

            # 3. Drawing
            self.screen.fill(BG_COLOR)
            self.grid.draw(self.screen)

            pygame.display.update()

            time.sleep(DELAY)  # Add time DELAY

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
            - SPACE: Stop the simulation.
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

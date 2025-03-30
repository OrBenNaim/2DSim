import sys
import time
import numpy as np
import pygame
from src.entities.herbivore import Herbivore
from src.entities.mobile_entity import MobileEntity
from src.events.event_manager import EventsManager
from src.events.observers import LiveOrganismsObserver, HerbivoreReproductionsObserver, InterestingEventsObserver
from src.grid import Grid
from src.constants import DELAY, BG_COLOR, SCREEN_WIDTH, SCREEN_HEIGHT


class Simulation:
    """ Manages the game logic, updates the grid, handles user input and events.
        This class functions as a pipeline between the main() function and the grid class. """

    def __init__(self) -> None:
        """Initialize the game simulation """
        self.sim_status = None
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Nature Simulation")

        self.grid = Grid()  # Create a new grid object for the current simulation
        self.temp_grid = Grid()  # It will be used at the update() function

        self.events_manager = EventsManager(self.grid)
        self.cnt_generation = 0

    def update_grid(self) -> None:
        """ Updates the grid to the next state according to the game rules """

        if self.sim_status == "play":
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

                    if not isinstance(obj, Herbivore):
                        if obj.current_lifespan == obj.lifespan:
                            self.events_manager.herbivore_reproduction(self.cnt_generation)

            self.temp_grid.add_random_plant()  # Plants appear randomly at empty spaces

            self.grid.cells = self.temp_grid.cells.copy()  # Update the original grid.cells at the end of the operation

    def run(self):
        """ This function handles the simulation itself """
        self.sim_status = "play"
        self.grid.load_param_from_yaml()  # Initialize the grid for the first time from .yaml file configuration

        self.create_alerts_observers()

        # Simulation Loop
        while self.sim_status != "stop":
            self.cnt_generation += 1

            # 1. User's Event Handling
            self.user_event_handler()

            # 2. Updating the state of the grid
            self.update_grid()

            # 3. Check predefined events of the game
            self.events_manager.check_live_organisms(self.cnt_generation)
            self.events_manager.herbivore_reproduction(self.cnt_generation)

            # 4. Drawing
            self.screen.fill(BG_COLOR)
            self.grid.draw(self.screen)

            pygame.display.update()

            time.sleep(DELAY)  # Add time DELAY

        self.events_manager.plot_all_graphs()

    def create_alerts_observers(self):
        """
        Creates and registers alert observers for predefined simulation events.

        This method initializes alert observers for specific events and registers
        them with the `events_manager`, which acts as the event dispatcher.

        The following alerts are created and added as observers:

        - `HerbivoreExtinctionAlert`: Triggers when no more Herbivores are alive.
        - `PredatorEatsHerbivoreAlert`: Triggers when a Predator eats a Herbivore.
        - `PlantsExceedsAlert`: Triggers when plants exceed 90% of the grid space.

        Each observer is associated with an event type from `EventName` and a corresponding message."""


        live_organisms_observer = LiveOrganismsObserver()
        self.events_manager.add_observer(observer=live_organisms_observer)

        herbivore_reproductions_observer = HerbivoreReproductionsObserver()
        self.events_manager.add_observer(observer=herbivore_reproductions_observer)

        interesting_events_observer = InterestingEventsObserver()
        self.events_manager.add_observer(observer=interesting_events_observer)

    def user_event_handler(self):
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
                    self.sim_status = "play"
                    pygame.display.set_caption("Game of Life is running")

                elif event.key == pygame.K_SPACE:  # Pause the simulation if the user presses the 'Space' key
                    self.sim_status = "pause"
                    pygame.display.set_caption("Game of Life has stopped")

                elif event.key == pygame.K_ESCAPE:  # Stop the simulation if the user presses the 'Esc' key
                    self.sim_status = "stop"

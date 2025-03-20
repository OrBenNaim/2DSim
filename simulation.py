import os
import sys
import time

import numpy as np
import pygame
from grid import Grid


def get_file_from_initial_patterns_folder(folder_path: str) -> str:
    """ This function display the existing initial_pattern files
        and allow the user to select his desired initial_pattern file """

    # List all files in the folder
    files = os.listdir(folder_path)

    # Filter out non-text files
    text_files = [file for file in files if file.endswith('.txt')]

    print("\nCurrent initial patterns files:")

    # Display the existing files in the folder
    for i, filename in enumerate(text_files, start=1):
        print(f"{i}. {filename}")

    # Allow the user to select the desired file
    while True:

        try:
            # Get the user selection (which is a number)
            file_selection_num = int(input(f"Select a file by number (1-{len(text_files)}): "))

            # Check if the input within a valid range
            if file_selection_num < 1 or file_selection_num > len(text_files):
                print(f"Invalid choice. Please select a number between 1 and {len(text_files)}.")
                continue

            # Get the file's name
            selected_filename = text_files[file_selection_num - 1]
            return os.path.join(folder_path, selected_filename)

        except ValueError:
            print("Invalid input. Please enter a valid number.")


class Simulation:
    """ The 'Simulation' class handles the different states of the game
        and updates the grid object accordingly.
        This class functions as pipeline between the main() function and the grid class """

    def __init__(self, screen_width: int, screen_height: int, cell_size: int) -> None:
        """Initialize the game simulation """
        self.grid = Grid(screen_width, screen_height, cell_size)          # Create new grid object for the current simulation
        self.temp_grid = Grid(screen_width, screen_height, cell_size)     # It will be used at the update() function

        self.screen_width = screen_width
        self.screen_height = screen_height

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


    def run(self):
        """ This function create the pygame screen and handles the simulation itself """

        pattern_folder = "initial_patterns"  # This folder store the initial patterns as text file

        # Let the user choose how he would like to initialize the pattern
        while True:
            use_text_file_for_pattern = input("\nDo you want to use text file for the initial pattern? (Press Y/N)\n").lower()

            if use_text_file_for_pattern == 'y' or use_text_file_for_pattern == 'n':
                break
            else:
                print("You entered wrong input. Please try again")

        if use_text_file_for_pattern == 'y':
            file_path = get_file_from_initial_patterns_folder(pattern_folder)
            if file_path:
                self.load_pattern_from_file(file_path)
                self.start()

        pygame.init()
        screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
        pygame.display.set_caption("Game of Life")

        bg_color = (20, 20, 20)  # Gray color

        # Simulation Loop
        while True:

            # 1. Event Handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # If the user press on specific cell with his mouse, mark this cell
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    row = pos[1] // self.grid.cell_size
                    column = pos[0] // self.grid.cell_size
                    self.toggle_cell(row, column)

                # If the user press on the keyboard, check it
                elif event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_RETURN:  # Start the simulation if the user press the 'Enter' key
                        self.start()
                        pygame.display.set_caption("Game of Life is running")

                    elif event.key == pygame.K_SPACE:  # Stop the simulation if the user press the 'Space' key
                        self.stop()
                        pygame.display.set_caption("Game of Life has stopped")

                    elif event.key == pygame.K_r:  # Create a random initial pattern if the user press the 'r' key
                        self.create_random_pattern()

                    elif event.key == pygame.K_c:  # Clear the grid if the user press the 'c' key
                        self.clear()

                    elif event.key == pygame.K_l:  # Load pattern (centered)
                        file_path = get_file_from_initial_patterns_folder(pattern_folder)
                        if file_path:
                            self.load_pattern_from_file(file_path)
                            self.start()

            # 2. Updating State
            self.update_grid()

            # 3. Drawing
            screen.fill(bg_color)
            self.draw(screen)

            pygame.display.update()

            time.sleep(0.02)    # Add delay of 0.02 sec
import numpy as np
import time
import os
from typing import Any

#-----------------------------------------------------------------------------------------------------------------------
def get_file_from_initial_patterns_folder(folder_path: str) -> str:
    """ This function display the existing initial_pattern files
        and allow the user to select his desired initial_pattern file """

    # List all files in the folder
    files = os.listdir(folder_path)

    # Filter out non-text files
    text_files = [file for file in files if file.endswith('.txt')]

    print("Current files:")

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


#-----------------------------------------------------------------------------------------------------------------------
def load_pattern(filename: str) -> np.ndarray:
    """ This function responsible to open the given file and to create the grid as 2D numpy array """
    with open(filename, "r") as file:
        lines = file.readlines()

    # For each line in the file, check each cell status (live\die) and create 2D array accordingly
    grid_arr = np.array([[ 1 if cell == 'O' else 0 for cell in line.strip() ] for line in lines ])
    return grid_arr


#-----------------------------------------------------------------------------------------------------------------------
def display_grid(grid: np.ndarray[np.int_, 2]) -> None:
    """ This function display the grid at its current state in the terminal """
    for row in grid:
        for cell in row:
            if cell:
                print('O', end='')
            else:
                print('.', end='')

        print() # Add newline

#-----------------------------------------------------------------------------------------------------------------------
def count_live_neighbors(grid: np.ndarray[np.int_, 2], ref_row: int, ref_col: int) -> int:
    """ This function counts how many live neighbors exist for a specific cell """
    counter = 0

    # In reference to the cell itself, the indexes of his neighbors are
    # always constants.
    # if cell is grid[ref_row][ref_col] so:
    # neighbor1 is grid[ref_row - 1][ref_col - 1]   # upper_left
    # neighbor2 is grid[ref_row - 1][ref_col]       # upper_mid
    # and so on.

    neighbors_shifts = [
        (-1, -1), (-1, 0), (-1, 1),     # upper_left, upper_mid, upper_right
        (0, -1), (0, 1),                # mid_left, mid_right
        (1, -1), (1, 0), (1, 1),        # upper_left, upper_mid, upper_right
    ]

    # Get the number of rows and columns
    rows, cols = grid.shape

    # Calculate the neighbors indexes for each cell on the grid
    for shift_row, shift_col in neighbors_shifts:
        neighbor_row_idx, neighbor_col_idx = shift_row + ref_row, shift_col + ref_col

        # Check if the neighbor's indexes are valid indexes
        if 0 <= neighbor_row_idx < rows and 0 <= neighbor_col_idx < cols:
            counter += grid[neighbor_row_idx, neighbor_col_idx]

    return counter


#-----------------------------------------------------------------------------------------------------------------------
def update_grid(grid: np.ndarray[np.int_, 2]) -> np.ndarray[np.int_, 2]:
    """ This function calculates and creates the next state of the grid according to the game rules """
    # Get the number of rows and columns
    rows, cols = grid.shape

    # Create new grid to the next generation.
    # Changing specific cell on the current grid will damage other cells.
    updated_grid = np.zeros((rows, cols), dtype=int)

    # For each cell, update his status accordingly to his living neighbors and the game rules
    for row in range(rows):         # 0 <= row <= len(rows) - 1
        for col in range(cols):     # 0 <= col <= len(rows) - 1
            cnt_live_neighbors = count_live_neighbors(grid, row, col)

            # Live cell
            if grid[row][col]:

                # A case of a live cell that lives to the next generation
                if cnt_live_neighbors == 2 and cnt_live_neighbors == 3:
                    updated_grid[row][col] = 1

            # Dead cell
            else:
                 if cnt_live_neighbors == 3:
                     updated_grid[row][col] = 1

    return updated_grid

#-----------------------------------------------------------------------------------------------------------------------
def game_of_life(filename:str, generations: int) -> None:
    """ This function activates the entire game algorithm """
    grid_arr = load_pattern(filename)   # grid_arr is 2D numpy array

    for _ in range(generations):
        display_grid(grid_arr)              # Display the grid at its current state before the next iteration
        grid_arr = update_grid(grid_arr)    # Update the grid's state
        time.sleep(0.5)                     # Create delay between iterations


#-----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    steps = 50      # The number of iterations of the game

    # Display the existing initial patterns and allow the user to select one of them
    selected_file = get_file_from_initial_patterns_folder("initial_patterns")

    # Activate the game and show each step during the simulation
    game_of_life(selected_file, steps)
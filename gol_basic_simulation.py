import numpy as np
import time
import os
from typing import Any

#-----------------------------------------------------------------------------------------------------------------------
def get_file_from_initial_patterns_folder(folder_path):
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
def game_of_life(filename:str, generations: int) -> None:
    """ This function activates and creates the entire game algorithm """
    grid_arr = load_pattern(filename)   # grid_arr is 2D numpy array
    print(grid_arr)



#-----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    steps = 50      # The number of iterations of the game
    selected_file = get_file_from_initial_patterns_folder("initial_patterns")

    game_of_life(selected_file, steps)
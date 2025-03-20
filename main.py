import os
import sys
import pygame
from simulation import Simulation


def get_file_from_initial_patterns_folder(folder_path: str) -> str:
    """ This function display the existing initial_pattern files
        and allow the user to select his desired initial_pattern file """

    # List all files in the folder
    files = os.listdir(folder_path)

    # Filter out non-text files
    text_files = [file for file in files if file.endswith('.txt')]

    print("\nCurrent files:")

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



if __name__ == "__main__":
    pygame.init()

    GREY = (40, 40, 40)
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    CELL_SIZE = 12
    FPS = 12
    PATTERN_FOLDER = "initial_patterns"  # Folder where patterns are stored

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Game of Life")

    clock = pygame.time.Clock()
    simulation = Simulation(SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE)

    # Simulation Loop
    while True:

        # 1. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # If the user press on specific cell with his mouse, mark this cell
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row = pos[1] // CELL_SIZE
                column = pos[0] // CELL_SIZE
                simulation.toggle_cell(row, column)


            # If the user press on the keyboard, check it
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:    # Start the simulation if the user press the 'Enter' key
                    simulation.start()
                    pygame.display.set_caption("Game of Life is running")

                elif event.key == pygame.K_SPACE:   # Stop the simulation if the user press the 'Space' key
                    simulation.stop()
                    pygame.display.set_caption("Game of Life has stopped")

                elif event.key == pygame.K_r:       # Create a random initial pattern if the user press the 'r' key
                    simulation.create_random_pattern()

                elif event.key == pygame.K_c:       # Clear the grid if the user press the 'c' key
                    simulation.clear()

                elif event.key == pygame.K_l:  # Load pattern (centered)
                    file_path = get_file_from_initial_patterns_folder(PATTERN_FOLDER)
                    if file_path:
                        simulation.load_pattern_from_file(file_path)
                        simulation.start()


        # 2. Updating State
        simulation.update_grid()

        # 3. Drawing
        screen.fill(GREY)
        simulation.draw(screen)

        pygame.display.update()
        clock.tick(FPS)
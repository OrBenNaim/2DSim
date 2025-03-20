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
    CELL_SIZE = 10
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



# import time
# import pygame
# import numpy as np
#
# COLOR_BG = (10, 10, 10,)
# COLOR_GRID = (40, 40, 40)
# COLOR_DIE_NEXT = (170, 170, 170)
# COLOR_ALIVE_NEXT = (255, 255, 255)
#
# pygame.init()
# pygame.display.set_caption("conway's game of life")
#
#
# def update(screen, cells, size, with_progress=False):
#     updated_cells = np.zeros((cells.shape[0], cells.shape[1]))
#
#     for row, col in np.ndindex(cells.shape):
#         alive = np.sum(cells[row-1:row+2, col-1:col+2]) - cells[row, col]
#         color = COLOR_BG if cells[row, col] == 0 else COLOR_ALIVE_NEXT
#
#         if cells[row, col] == 1:
#             if alive < 2 or alive > 3:
#                 if with_progress:
#                     color = COLOR_DIE_NEXT
#             elif 2 <= alive <= 3:
#                 updated_cells[row, col] = 1
#                 if with_progress:
#                     color = COLOR_ALIVE_NEXT
#         else:
#             if alive == 3:
#                 updated_cells[row, col] = 1
#                 if with_progress:
#                     color = COLOR_ALIVE_NEXT
#
#         pygame.draw.rect(screen, color, (col * size, row * size, size - 1, size - 1))
#
#     return updated_cells
#
#
# def main():
#     pygame.init()
#     screen = pygame.display.set_mode((800, 600))
#
#     cells = np.zeros((60, 80))
#     screen.fill(COLOR_GRID)
#     update(screen, cells, 10)
#
#     pygame.display.flip()
#     pygame.display.update()
#
#     running = False
#
#     while True:
#         for Q in pygame.event.get():
#             if Q.type == pygame.QUIT:
#                 pygame.quit()
#                 return
#
#             elif Q.type == pygame.KEYDOWN:
#                 if Q.key == pygame.K_SPACE:
#                     running = not running
#                     update(screen, cells, 10)
#                     pygame.display.update()
#
#             if pygame.mouse.get_pressed()[0]:
#                 pos = pygame.mouse.get_pos()
#                 cells[pos[1] // 10, pos[0] // 10] = 1
#                 update(screen, cells, 10)
#                 pygame.display.update()
#
#         screen.fill(COLOR_GRID)
#
#         if running:
#             cells = update(screen, cells, 10, with_progress=True)
#             pygame.display.update()
#
#         time.sleep(0.001)
#
#
# if __name__ == "__main__":
#     main()


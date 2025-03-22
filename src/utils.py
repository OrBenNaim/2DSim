import os


def get_file_from_initial_patterns_folder(folder_path: str) -> str:
    """ This function displays the existing initial_pattern files
        and allows the user to select his desired initial_pattern file """

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

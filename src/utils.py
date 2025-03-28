import numpy as np
import yaml
from src.constants import FOLDER_CONFIG_PATH


# Load the configuration once at the start
with open(FOLDER_CONFIG_PATH, "r", encoding="utf-8") as file:
    CONFIG_DATA = yaml.safe_load(file)


def get_config():
    """
    Retrieves the loaded configuration data.

    This function provides access to the global configuration settings
    that were loaded from the YAML file at the start of the program. It
    returns the configuration data as a Python dictionary, allowing other
    parts of the program to access the configuration without reloading
    the YAML file repeatedly.

    Returns:
        dict: The configuration data loaded from the YAML file.
    """
    return CONFIG_DATA

def get_target_indices(grid, target_object):
    """
    Finds the indices of all occurrences of a target object within a given grid.

    Args:
        grid (np.ndarray): A 2D NumPy array representing the grid, where each element is a cell.
        target_object (type): The class or type of the target objects to search for.

    Returns:
        tuple[np.ndarray, np.ndarray]: A tuple containing two NumPy arrays.
            - The first array contains the row indices of the target objects.
            - The second array contains the corresponding column indices.
    """

    # Create a boolean mask to identify cells that are instances of the target_object
    mask = np.vectorize(lambda cell: isinstance(cell, target_object))(grid.cells)

    # Get the row and column indices where the target objects are present
    target_indices = np.nonzero(mask)
    return target_indices

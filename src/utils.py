import yaml
from src.constants import FOLDER_CONFIG_PATH

# Load the configuration once at the start
with open(FOLDER_CONFIG_PATH, "r", encoding="utf-8") as file:
    CONFIG_DATA = yaml.safe_load(file)


# Function to access config
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

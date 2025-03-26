import yaml
from src.constants import FOLDER_CONFIG_PATH

# Load the configuration once at the start
with open(FOLDER_CONFIG_PATH, "r", encoding="utf-8") as file:
    CONFIG_DATA = yaml.safe_load(file)


# Function to access config
def get_config():
    return CONFIG_DATA
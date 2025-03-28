from src.events.event_name import EventName
import logging
import os

# Ensure the logs directory exists
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Configure logging
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "simulation_alerts.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

class Alert:
    """ Base class for alerts that listen to simulation events. """

    def __init__(self, event_name: EventName, log_to_console: bool, log_to_file: bool):
        self.event_name = event_name    # Enum value, e.g., EventName.PREDATOR_EATS_HERBIVORE
        self.log_to_console = log_to_console
        self.log_to_file = log_to_file

    def update(self, msg: str):
        """ Update the alert instance about the occurrence of a some event """
        self.log(msg)

    def log(self, message: str):
        """ Handles logging alerts to the console and optionally to a file. """
        formatted_message = f"[ALERT] {self.event_name.value}: {message}"
        print(formatted_message)  # Print to console

        if self.log_to_file:
            logging.info(formatted_message)  # Log to file

        if self.log_to_console:
            print(logging.info(formatted_message))  # Print to console
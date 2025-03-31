from enum import Enum


class EventName(Enum):
    """"
    Enumeration representing different types of events in the system.
    Each event is assigned a descriptive string value, making it easier
    to reference events consistently throughout the program.
    """
    PREDATOR_EATS_HERBIVORE = "Predator eats Herbivore"
    PLANT_OVERGROWTH = "Plant Overgrowth"
    HERBIVORE_EXTINCTION = "Herbivore Extinction"
    # Add more event names as needed

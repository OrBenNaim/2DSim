from enum import Enum


class EventName(Enum):
    """"
    Enumeration representing different types of events in the system.
    Each event is assigned a descriptive string value, making it easier
    to reference events consistently throughout the program.
    """

    LIVE_ORGANISMS = "Live Organisms"
    HERBIVORE_REPRODUCTIONS = "Herbivore Reproductions"
    ANIMAL_CONSUMPTION = "Animal Consumption"
    INTERESTING_EVENTS = "Summarizing Interesting Events"
    # Add more event names as needed

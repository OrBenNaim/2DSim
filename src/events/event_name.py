from enum import Enum


class EventName(Enum):
    """"
    Enumeration representing different types of events in the system.
    Each event is assigned a descriptive string value, making it easier
    to reference events consistently throughout the program.
    """

    LIVE_ORGANISMS = "Live Organisms"
    HERBIVORE_REPRODUCTIONS = "Herbivore Reproductions"
    INTERESTING_EVENTS = "Interesting Events"
    # Add more event names as needed

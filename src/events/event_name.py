from enum import Enum


class EventName(Enum):
    """
    An Enum makes it easier to manage event types because it provides a set of predefined values.
    This can be useful when needs to ensure that the names of events and
    alerts are consistent across the system.
    """

    LIVE_ORGANISMS = "Live Organisms"
    HERBIVORE_REPRODUCTIONS = "Herbivore Reproductions"
    INTERESTING_EVENTS = "Interesting Events"
    # Add more event names as needed

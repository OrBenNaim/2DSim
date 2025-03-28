from enum import Enum


class EventName(Enum):
    """
    An Enum makes it easier to manage event types because it provides a set of predefined values.
    This can be useful when needs to ensure that the names of events and
    alerts are consistent across the system.
    """

    PREDATOR_EATS_HERBIVORE = "Predator eats Herbivore"
    PLANT_OVERGROWTH = "Plant Overgrowth"
    HERBIVORE_EXTINCTION = "Herbivore Extinction"
    # Add more event names as needed
from abc import ABC, abstractmethod
from src.events.event_name import EventName
from src.utils import log_msg


class Observer(ABC):
    """
    Abstract base class for all observers in the event system.
    Observers listen for specific events and respond accordingly when notified.
    """
    event_name: EventName = None

    @abstractmethod
    def update(self, data):
        """
        Abstract method that subclasses must implement.
        This method defines how the observer responds when an event occurs.
        """


class HerbivoreExtinctionAlert(Observer):
    """
    Observer that triggers an alert when herbivores go extinct.
    Logs a message when notified of a herbivore extinction event.
    """
    event_name = EventName.HERBIVORE_EXTINCTION

    def update(self, data):
        """ Handles the herbivore extinction event by logging a message. """
        log_msg(event_name=self.event_name, message="All Herbivores are extinct")


class PredatorEatsHerbivoreAlert(Observer):
    """
    Observer that triggers an alert when a predator eats a herbivore.

    Logs a message when notified of a predator consuming a herbivore.
    """
    event_name = EventName.PREDATOR_EATS_HERBIVORE

    def update(self, data):
        """ Handles the predator eating herbivore event by logging a message. """
        log_msg(event_name=self.event_name, message="Predator Eats Herbivore")


class PlantsExceedsAlert(Observer):
    """
    Observer that triggers an alert when the plant population exceeds a certain limit.
    Logs a message when notified of excessive plant growth.
    """
    event_name = EventName.PLANT_OVERGROWTH

    def update(self, data):
        """ Handles the excessive plant growth event by logging a message. """
        msg = f"Plants exceeds {data * 100}% of the grid space"
        log_msg(PlantsExceedsAlert.event_name, msg)

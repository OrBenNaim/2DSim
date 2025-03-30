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


class LiveOrganismsObserver(Observer):
    """
    """
    event_name = EventName.LIVE_ORGANISMS

    def update(self, data):
        """  """
        log_msg(event_name=self.event_name, message="All Herbivores are extinct")


class HerbivoreReproductionsObserver(Observer):
    """
    """
    event_name = EventName.HERBIVORE_REPRODUCTIONS

    def update(self, data):
        """  """
        log_msg(event_name=self.event_name, message="Predator Eats Herbivore")


class InterestingEventsObserver(Observer):
    """
    """
    event_name = EventName.INTERESTING_EVENTS

    def update(self, data):
        """  """


from abc import ABC, abstractmethod
from src.events.event_name import EventName
from src.utils import log_msg


class Observer(ABC):
    """
    Abstract base class for all observers in the event system.
    Observers listen for specific events and respond accordingly when notified.
    """

    def __init__(self, event_name: EventName, msg: str):
        """
        Initializes an observer with an event name and a message.
        Args:
        event_name (EventName): The event that this observer is subscribed to.
        msg (str): The message associated with the event.
        """
        self.msg = msg
        self.event_name = event_name

    @abstractmethod
    def update(self):
        """
        Abstract method that subclasses must implement.

        This method defines how the observer responds when an event occurs.
        """


class HerbivoreExtinctionAlert(Observer):
    """
    Observer that triggers an alert when herbivores go extinct.
    Logs a message when notified of a herbivore extinction event.
    """
    def __init__(self, event_name: EventName, msg: str):
        super().__init__(event_name, msg)

    def update(self):
        """ Handles the herbivore extinction event by logging a message. """
        log_msg(self.event_name, self.msg)


class PredatorEatsHerbivoreAlert(Observer):
    """
        Observer that triggers an alert when a predator eats a herbivore.

        Logs a message when notified of a predator consuming a herbivore.
        """
    def __init__(self, event_name: EventName, msg: str):
        super().__init__(event_name, msg)

    def update(self):
        """ Handles the predator eating herbivore event by logging a message. """
        log_msg(self.event_name, self.msg)


class PlantsExceedsAlert(Observer):
    """
        Observer that triggers an alert when the plant population exceeds a certain limit.

        Logs a message when notified of excessive plant growth.
        """
    def __init__(self, event_name: EventName, msg: str):
        super().__init__(event_name, msg)

    def update(self):
        """ Handles the excessive plant growth event by logging a message. """
        log_msg(self.event_name, self.msg)

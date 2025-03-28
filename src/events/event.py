from typing import List

from src.alerts.alert import Alert
from src.events.event_name import EventName


class Event:
    """ Represents the Event object that observed by the appropriate Alert"""

    def __init__(self, event_name: EventName):
        self.event_name = event_name    # Enum value
        self._subscribers: List = []          # List of all subscribers to this event

    def add_subscribe(self, subscriber: type(Alert)):
        """ If the subscriber is not in the list, append it into the list """
        if subscriber not in self._subscribers:
            self._subscribers.append(subscriber)

    def remove_subscribe(self, subscriber: Alert):
        """Remove the observer from the observer list"""
        try:
            self._subscribers.remove(subscriber)

        except ValueError:
            pass

    def notify(self, msg: str):
        """ Notify all subscribers about the event with a message """
        for subscriber in self._subscribers:
            subscriber.update(msg)

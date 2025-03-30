from typing import Dict, List
from src.entities.plant import Plant
from src.events.event_name import EventName
from src.events.observers import Observer
from src.utils import get_target_indices


class EventsManager:
    """
    Manages event-based communication between observers and event types.

    This class maintains a dictionary where event names are mapped to lists of observers.
    Observers can subscribe to specific events and will be notified when an event occurs.
    """

    def __init__(self, grid):
        """
        Initializes the EventManager with an empty dictionary of observers.

        The dictionary keys represent event names (EventName objects), and the values
        are lists of observers subscribed to those events.
        """
        self.observers: Dict[EventName, List[Observer]] = {}
        self.grid = grid

    def add_observer(self, observer: Observer):
        """
        Adds an observer to a specific event.

        If the observer is not already subscribed to the given event, they will be added.

        Args:
            observer (Observer): The observer instance to subscribe.
        """
        if observer.event_name not in self.observers:
            self.observers[observer.event_name] = []

        if observer not in self.observers[observer.event_name]:
            self.observers[observer.event_name].append(observer)

    def remove_observer(self, observer: Observer, event_name: EventName):
        """
        Removes an observer from a specific event.

        If the observer is subscribed to the event, they will be removed.
        If the observer is not found, no action is taken.

        Args:
            observer (Observer): The observer instance to remove.
            event_name (EventName): The event from which the observer will be unsubscribed.
        """
        try:
            self.observers[event_name].remove(observer)
        except (ValueError, KeyError):
            pass  # Ignore if observer is not in the list or event_name is not found

    def notify(self, event_name: EventName, data=None):
        """
        Notifies all observers subscribed to a specific event.

        Each observer will receive the event notification, allowing them to react accordingly.

        Args:
            event_name (EventName): The event for which observers should be notified.
            :param event_name:
            :param data:
        """
        for observer in self.observers.get(event_name, []):
            observer.update(data)  # Assuming Observer class has an update method

    #--------------- Methods of business logic can notify subscribers about changes -----------------
    def check_live_organisms(self, cnt_generation: int) -> None:
        """
        """
        live_organisms_dict = {}

        for entity_name in self.grid.existing_entities:
            entity_obj = self.grid.existing_entities[entity_name]

            # Get the indices of all entity_obj in the grid
            entity_indices = get_target_indices(self.grid, entity_obj)

            # Count the number of entity_obj
            entity_obj_count = len(entity_indices[0])  # Number of row indices found

            live_organisms_dict[entity_name] = entity_obj_count

        # If no live organisms are found, notify all the relevant observers
        if len(live_organisms_dict) is not 0:
            self.notify(event_name=EventName.LIVE_ORGANISMS, data=(live_organisms_dict, cnt_generation))

    def herbivore_reproduction(self, cnt_generation: int) -> None:
        """ """
        self.notify(EventName.HERBIVORE_REPRODUCTIONS, cnt_generation)

    def check_interesting_events(self, cnt_generation: int) -> None:
        """
        """

        self.notify(EventName.INTERESTING_EVENTS)

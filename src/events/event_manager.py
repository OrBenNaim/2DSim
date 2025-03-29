from typing import Dict, List
from src.entities.herbivore import Herbivore
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
        self._observers: Dict[EventName, List[Observer]] = {}
        self.grid = grid

    def add_observer(self, observer: Observer):
        """
        Adds an observer to a specific event.

        If the observer is not already subscribed to the given event, they will be added.

        Args:
            observer (Observer): The observer instance to subscribe.
            event_name (EventName): The event to which the observer is subscribing.
        """
        if observer.event_name not in self._observers:
            self._observers[observer.event_name] = []

        if observer not in self._observers[observer.event_name]:
            self._observers[observer.event_name].append(observer)

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
            self._observers[event_name].remove(observer)
        except (ValueError, KeyError):
            pass  # Ignore if observer is not in the list or event_name is not found

    def notify(self, event_name: EventName):
        """
        Notifies all observers subscribed to a specific event.

        Each observer will receive the event notification, allowing them to react accordingly.

        Args:
            event_name (EventName): The event for which observers should be notified.
        """
        for observer in self._observers.get(event_name, []):
            observer.update()  # Assuming Observer class has an update method

    #--------------- Methods of business logic can notify subscribers about changes -----------------
    def check_herbivore_extinction(self) -> None:
        """
        Checks if all herbivores have gone extinct in the grid.
        If no herbivores are found, notify all the relevant observers.
        """

        # Get the indices of all Herbivores in the grid
        herbivore_indices = get_target_indices(self.grid, Herbivore)

        # Count the number of herbivores
        herbivore_count = len(herbivore_indices[0])  # Number of row indices found

        # If no herbivores are found, notify all the relevant observers
        if herbivore_count == 0:
            self.notify(EventName.HERBIVORE_EXTINCTION)

    def check_plant_overgrowth(self, overgrown):
        """
        Checks if the number of plants in the grid exceeds the defined threshold
        and notify all the relevant observers.
        """

        # Get the indices of all plants in the grid
        plant_indices = get_target_indices(self.grid, Plant)

        # Count the number of plants
        plant_count = len(plant_indices[0])  # Number of row indices found

        total_cells = self.grid.cells.size

        # If the number of plants in the grid exceeds the defined threshold,
        # notify all the relevant observers
        if plant_count / total_cells > overgrown:
            self.notify(EventName.PLANT_OVERGROWTH)

    def check_predator_eats_herbivore(self):
        self.notify(EventName.PREDATOR_EATS_HERBIVORE)
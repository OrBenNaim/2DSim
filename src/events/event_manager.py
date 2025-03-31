from typing import Dict, List

from src.entities.herbivore import Herbivore
from src.entities.mobile_entity import MobileEntity
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
        self.animal_consumption_cnt = 0
        self.reproduction_cnt = 0

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

    def remove_observer(self, observer: Observer):
        """
        Removes an observer from a specific event.
        If the observer is subscribed to the event, they will be removed.
        If the observer is not found, no action is taken.
        Args:
            observer (Observer): The observer instance to remove.
        """
        try:
            self.observers[observer.event_name].remove(observer)
        except (ValueError, KeyError):
            pass  # Ignore if observer is not in the list or event_name is not found

    def notify(self, event_name: EventName, generation_counter: int, stats_dict: Dict[str, int] = None):
        """
        Notifies all observers subscribed to a specific event.
        If stats_dict is provided, it is unpacked as keyword arguments.
        """
        for observer in self.observers.get(event_name, []):
            if stats_dict:
                observer.update(generation_counter, **stats_dict)  # Unpack if a dictionary is provided
            else:
                observer.update(generation_counter)  # Call update without extra arguments

    def plot_all_graphs(self):
        """
        Plots the data for all observers.
        """
        for _, observers in self.observers.items():
            for observer in observers:
                print(f"Plotting for {observer.__class__.__name__}")
                observer.plot_df()

    #--------------- Methods of business logic can notify subscribers about changes -----------------
    def check_live_organisms(self, generation_cnt: int) -> None:
        """
        Checks the number of live organisms in the grid for the current generation.
        Args:
            generation_cnt (int): The current generation number.
        """
        live_organisms_dict = {}

        for entity_name in self.grid.existing_entities:
            entity_obj = self.grid.existing_entities[entity_name]

            # Get the indices of all entity_obj in the grid
            entity_indices = get_target_indices(self.grid.cells, entity_obj)

            # Count the number of entity_obj
            entity_obj_count = len(entity_indices[0])  # Number of row indices found

            live_organisms_dict[entity_name] = entity_obj_count

        # If no live organisms are found, notify all the relevant observers
        if len(live_organisms_dict) != 0:
            self.notify(event_name=EventName.LIVE_ORGANISMS, generation_counter=generation_cnt,
                        stats_dict=live_organisms_dict)

    def check_herbivore_reproduction(self, old_row: int, old_col: int,
                                     new_row: int, new_col: int, generation_cnt: int) -> None:
        """
        Checks if a new herbivore has been reproduced at the specified grid location.
        Args:
            old_row (int): The previous row index of the herbivore's location.
            old_col (int): The previous column index of the herbivore's location.
            new_row (int): The new row index of the herbivore's location.
            new_col (int): The new column index of the herbivore's location.
            generation_cnt (int): The current generation number.
        """
        if new_row != old_row or new_col != old_col:
            if isinstance(self.grid.cells[new_row][old_row], Herbivore):
                self.notify(event_name=EventName.HERBIVORE_REPRODUCTIONS, generation_counter=generation_cnt)

    def check_interesting_events(self, generation_cnt: int, obj: MobileEntity,
                                 check_reproduction: bool, *args) -> None:
        """
        Checks for interesting events like reproduction and consumption in a simulation.

        Args:
            generation_cnt (int): The current generation count.
            obj (MobileEntity): The mobile entity (e.g., an organism) to check for events.
            check_reproduction (bool): Whether to check for reproduction events.
            *args: Additional arguments, expected to include old_row and old_col for reproduction checks.

        Returns:
            None: Updates internal counters and notifies observers of events.
        """
        interesting_events_dict = {}

        if check_reproduction is True:
            old_row = args[0]
            old_col = args[1]

            # Check if Reproduction occurred
            if obj.row != old_row or obj.col != old_col:
                if isinstance(self.grid.cells[obj.row][old_row], Herbivore):
                    self.reproduction_cnt += 1

        interesting_events_dict["Herbivore Reproductions"] = self.reproduction_cnt

        # Check organism consumption occurred
        if obj.current_lifespan == obj.lifespan:
            self.animal_consumption_cnt += 1

        interesting_events_dict["Animal Consumption"] = self.animal_consumption_cnt

        self.notify(EventName.INTERESTING_EVENTS, generation_cnt, stats_dict=interesting_events_dict)

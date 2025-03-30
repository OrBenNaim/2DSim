import os
from abc import ABC, abstractmethod
from typing import Dict
from src.constants import FOLDER_PLOTS_PATH
from src.events.event_name import EventName
import pandas as pd
import matplotlib.pyplot as plt


class Observer(ABC):
    """
    Abstract base class for all observers in the event system.
    Observers listen for specific events and respond accordingly when notified.
    """
    event_name: EventName = None

    def __init__(self):
        self.df = pd.DataFrame({})
        self.path_to_plot_folder = FOLDER_PLOTS_PATH
        os.makedirs(self.path_to_plot_folder, exist_ok=True)  # Create directory if it doesn't exist

    @abstractmethod
    def update(self, gen_cnt: int, stats_dict: Dict[str, int]=None):
        """
        Abstract method that subclasses must implement.
        This method defines how the observer responds when an event occurs.
        """

    @abstractmethod
    def plot_df(self):
        """ """


class LiveOrganismsObserver(Observer):
    """
    """
    event_name = EventName.LIVE_ORGANISMS

    def update(self, gen_cnt: int, live_organisms_dict: Dict[str, int]=None):
        """
        Adds a new row to the DataFrame.

        Parameters:
        - gen_cnt (int): The generation count.
        - live_organisms_dict (Dict[str, int], optional): A dictionary containing entity names as keys
          and their respective counts as values.
        """
        if live_organisms_dict is None:
            return

        # Create a new row with the generation count and the organisms' data
        new_row = {"Generation": gen_cnt, **live_organisms_dict}

        # Append the new row to the DataFrame
        self.df = pd.concat([self.df, pd.DataFrame([new_row])], ignore_index=True)


    def plot_df(self):
        """ """
        self.df.set_index("Generation").plot(marker="o", figsize=(8, 5), grid=True,
                                        title="Live Organisms Over Generations")
        plt.xlabel("Generations")
        plt.ylabel("Live Organisms Count")
        plt.legend()
        plt.savefig(self.path_to_plot_folder + "/live_organisms_per_gen.png", dpi=300)
        plt.show()


class HerbivoreReproductionsObserver(Observer):
    """
    """
    event_name = EventName.HERBIVORE_REPRODUCTIONS

    def update(self, gen_cnt: int, *stats_dict: Dict):
        """  """


    def plot_df(self):
        """ """
        self.df.set_index("Generation").plot(marker="o", figsize=(8, 5), grid=True,
                                        title="Herbivore Reproductions Over Generations")
        plt.xlabel("Generations")
        plt.ylabel("Herbivore Reproductions Count")
        plt.legend()
        plt.savefig(self.path_to_plot_folder + "/herbivore_reproductions_per_gen.png", dpi=300)
        plt.show()

class InterestingEventsObserver(Observer):
    """
    """
    event_name = EventName.INTERESTING_EVENTS

    def update(self, gen_cnt: int, *stats_dict: Dict):
        """  """

    def plot_df(self):
        """ """

import os
from abc import ABC, abstractmethod
from typing import Dict

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from src.constants import FOLDER_PLOTS_PATH
from src.events.event_name import EventName



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
    def update(self, gen_cnt: int, *args, **kwargs):
        """
        Abstract method that subclasses must implement.
        This method defines how the observer responds when an event occurs.
        """

    @abstractmethod
    def plot_df(self):
        """
        Abstract method for generating and displaying plots based on the observer's data.
        Subclasses must implement this method to visualize relevant statistics.
        """


class LiveOrganismsObserver(Observer):
    """
    Observer that tracks and visualizes the count of live organisms over generations.
    This class monitors the number of different organism types present in the
    ecosystem across generations.
    It stores the data in a DataFrame and provides
    methods to visualize the population trends as step functions.
    Attributes:
        event_name (EventName): The event type this observer listens for.
        df (pandas.DataFrame): DataFrame storing generation numbers and organism counts.
        path_to_plot_folder (str): Directory where plot images are saved.
    """
    event_name = EventName.LIVE_ORGANISMS

    def update(self, gen_cnt: int, *args, **live_organisms_dict: Dict[str, int]):
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
        """ Plots the number of live organisms over generations, ensuring correct axis limits. """
        if self.df.empty:
            print("No data to plot!")
            return

        # Sort by generation to ensure the correct order
        df_sorted = self.df.sort_values(by="Generation")

        plt.figure(figsize=(8, 5))

        # Define a list of different markers to cycle through
        markers = ['o', 's', '^', 'v', 'D', 'P', 'X', '*', 'p', 'h']

        # Plot all columns except Generation as step functions with different markers
        for i, column in enumerate(df_sorted.columns):
            if column != "Generation":
                marker = markers[i]
                plt.step(df_sorted["Generation"], df_sorted[column], where='post', marker=marker, label=column)

        # Set labels and title
        plt.xlabel("Generations")
        plt.ylabel("Live Organisms Count")
        plt.title("Live Organisms Over Generations")

        # Set y-axis ticks to increment by 1
        y_max = df_sorted.drop(columns=["Generation"]).max().max()
        plt.yticks(np.arange(0, y_max + 1, 2))  # From 0 to max value, step of 2

        # Set x-ticks to match generations
        plt.xticks(df_sorted["Generation"])

        # Ensure X-axis starts from 1
        plt.xlim(left=1)

        # Ensure Y-axis starts from 0
        plt.ylim(bottom=0)

        # Enable grid
        plt.grid(True)

        # Show legend
        plt.legend()

        # Save the plot
        plt.savefig(self.path_to_plot_folder + "/live_organisms_per_gen.png", dpi=300)

        # Show the plot
        plt.show()


class HerbivoreReproductionsObserver(Observer):
    """
    Observer class to track and visualize herbivore reproduction events over generations.

    This class is responsible for observing herbivore reproduction events and storing the
    reproduction counts for each generation in a DataFrame.
    The reproduction count for each generation is initialized as zero and is incremented each time a reproduction event
    occurs in the respective generation.
    The class also provides a method to plot the reproduction
    counts across generations.

    Attributes:
        event_name (EventName): The event name associated with herbivore reproduction.
        df (pd.DataFrame): A DataFrame storing the generations and their corresponding reproduction counts.
    """
    event_name = EventName.HERBIVORE_REPRODUCTIONS

    def __init__(self):
        super().__init__()
        self.df = pd.DataFrame([{"Generation": 1, "Reproduction_count": 0}])

    def update(self, gen_cnt: int, *args, **kwargs):
        """
        Handles herbivore reproduction events.
        Args:
            gen_cnt (int): The generation count.
            *args: Unused additional arguments.
            **kwargs: Unused additional keyword arguments.
        """
        if self.df.empty:
            # Initialize the DataFrame with "Generation" from 1 to gen_cnt and "Reproduction_count" to 0
            self.df = pd.DataFrame({
                "Generation": range(1, gen_cnt + 1),  # Creates a column with values from 1 to gen_cnt
                "Reproduction_count": [0] * gen_cnt  # Fills "Reproduction_count" with zeroes
            })

        if gen_cnt in self.df["Generation"].values:
            # Increment reproduction count for the correct generation
            self.df.loc[self.df["Generation"] == gen_cnt, "Reproduction_count"] += 1

        else:
            # Append a new row if gen_cnt exceeds initialized range
            new_row = pd.DataFrame([{"Generation": gen_cnt, "Reproduction_count": 1}])
            self.df = pd.concat([self.df, new_row], ignore_index=True)

    def plot_df(self):
        """
        Plot the reproduction counts data as a step function.
        Creates a visualization of herbivore reproduction counts across generations
        using a step plot with markers at each data point.
        The y-axis shows integer values starting from 0,
        and the x-axis shows the generation numbers.
        """
        # Sort by generation to ensure the correct order
        df_sorted = self.df.sort_values(by="Generation")

        plt.figure(figsize=(10, 6))
        plt.step(df_sorted["Generation"], df_sorted["Reproduction_count"], where='post', marker='o')
        plt.grid(True)
        plt.xlabel("Generations")
        plt.ylabel("Herbivore Reproductions Count")
        plt.title("Herbivore Reproductions Over Generations")

        # Set y-axis ticks to increment by 1
        y_max = df_sorted["Reproduction_count"].max()
        plt.yticks(np.arange(0, y_max + 1, 1))  # From 0 to max value, step of 1

        # Set x-ticks to match generations
        plt.xticks(df_sorted["Generation"])

        # Save the plot
        plt.savefig(self.path_to_plot_folder + "/herbivore_reproductions_per_gen.png", dpi=300)

        plt.show()



class InterestingEventsObserver(Observer):
    """
    Observer class to track and visualize interesting events (like reproductions, animal consumption, etc.)
    over generations.
    It provides a summary of these events and visualizes them as a timeline.
    Attributes:
        event_name (EventName): The event name associated with interesting events.
        df (pd.DataFrame): A DataFrame storing the event data for each generation.
    """
    event_name = EventName.INTERESTING_EVENTS
    interesting_events = [EventName.INTERESTING_EVENTS, EventName.HERBIVORE_REPRODUCTIONS,
                          EventName.ANIMAL_CONSUMPTION]

    def update(self, gen_cnt: int, *args, **interesting_events_dict: Dict[str, int]):
        """
        Updates the dataframe with a new generation count and corresponding interesting events' data.
        """
        if interesting_events_dict is None:
            return

        # Create a new row with the generation count and the organisms' data
        new_row = {"Generation": gen_cnt, **interesting_events_dict}

        # Append the new row to the DataFrame
        self.df = pd.concat([self.df, pd.DataFrame([new_row])], ignore_index=True)

    def plot_df(self):
        """
        Plots the dataframe as step functions for each column (except 'Generation').
        Saves the plot as a PNG file and displays it.
        """
        if self.df.empty:
            print("No data to plot!")
            return

        # Sort by generation to ensure the correct order
        df_sorted = self.df.sort_values(by="Generation")

        plt.figure(figsize=(8, 5))

        # Define a list of different markers to cycle through
        markers = ['o', 's', '^', 'v', 'D', 'P', 'X', '*', 'p', 'h']

        # Plot all columns except Generation as step functions with different markers
        for i, column in enumerate(df_sorted.columns):
            if column != "Generation":
                marker = markers[i]
                plt.step(df_sorted["Generation"], df_sorted[column], where='post', marker=marker, label=column)

        # Set labels and title
        plt.xlabel("Generations")
        plt.ylabel("Count")
        plt.title("Interesting Events Counts Over Generations")

        # Set y-axis ticks to increment by 1
        y_max = df_sorted.drop(columns=["Generation"]).max().max()
        plt.yticks(np.arange(0, y_max + 1, 2))  # From 0 to max value, step of 2

        # Set x-ticks to match generations
        plt.xticks(df_sorted["Generation"])

        # Ensure X-axis starts from 1
        plt.xlim(left=1)

        # Ensure Y-axis starts from 0
        plt.ylim(bottom=0)

        # Enable grid
        plt.grid(True)

        # Show legend
        plt.legend()

        # Save the plot
        plt.savefig(self.path_to_plot_folder + "/interesting_events.png", dpi=300)

        # Show the plot
        plt.show()

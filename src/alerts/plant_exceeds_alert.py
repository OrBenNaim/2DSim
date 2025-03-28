from src.alerts.alert import Alert
from src.entities.plant import Plant
from src.events.event_name import EventName
from src.utils import get_target_indices


class PlantOvergrowthAlert(Alert):
    """
    Alert triggered when the number of plants exceeds a certain percentage of the grid space.
    """

    def __init__(self, overgrown: float):
        """
        Initializes the PlantOvergrowthAlert.

        param overgrown: The threshold percentage (as a float between 0 and 1) at which the alert is triggered.
                          For example, if overgrown=0.9, the alert triggers when plants exceed 90% of the grid.
        """
        super().__init__(event_name=EventName.PLANT_OVERGROWTH, log_to_console=True, log_to_file=True)
        self.overgrown = overgrown

    def check(self, grid):
        """
        Checks if the number of plants in the grid exceeds the defined threshold.

        param grid: The simulation grid containing plant entities.
        return: None. Triggers an alert if the plant count exceeds the threshold.
        """

        # Get the indices of all plants in the grid
        plant_indices = get_target_indices(grid, Plant)

        # Count the number of plants
        plant_count = len(plant_indices[0])  # Number of row indices found

        total_cells = grid.cells.size

        # If no herbivores are found, trigger an alert
        if plant_count / total_cells > self.overgrown:
            self.update(f"Plants have overgrown {self.overgrown * 100}% of the grid!")

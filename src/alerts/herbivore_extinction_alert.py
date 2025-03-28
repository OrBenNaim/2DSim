from src.alerts.alert import Alert
from src.entities.herbivore import Herbivore
from src.events.event_name import EventName
from src.utils import get_target_indices


class HerbivoreExtinctionAlert(Alert):
    """ Alert triggered when all herbivores died. """

    def __init__(self):
        super().__init__(event_name=EventName.HERBIVORE_EXTINCTION, log_to_console=True, log_to_file=True)

    def check(self, grid) -> None:
        """
        Checks if all herbivores have gone extinct in the grid.
        If no herbivores are found, it triggers an alert update.

        Args:
            grid (np.ndarray): A 2D NumPy array representing the simulation grid.
        """

        # Get the indices of all Herbivores in the grid
        herbivore_indices = get_target_indices(grid, Herbivore)

        # Count the number of herbivores
        herbivore_count = len(herbivore_indices[0])  # Number of row indices found

        # If no herbivores are found, trigger an alert
        if herbivore_count == 0:
            self.update("All Herbivores have gone extinct!")
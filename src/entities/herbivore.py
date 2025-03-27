import numpy as np
from src.entities.mobile_entity import MobileEntity
from src.entities.plant import Plant


class Herbivore(MobileEntity):
    """ Herbivore move towards plants, eat them and reproduce. """

    def __init__(self, row: int, col: int) -> None:
        super().__init__(row, col, emoji="🐔")          # Initialize base constructor
        self.reproduction_cooldown = 0    # Cooldown before it can reproduce again
        self.current_cooldown = 0         # Tracks cooldown progress

    @property
    def target_object(self):
        """ Returns the class of the entity that Herbivores target (Plant). """
        return Plant

    def reproduce(self, grid) -> None:
        """
        Herbivores reproduce when reaching another herbivore,
        staying in the same space and spawning another herbivore in a random empty neighboring cell.
        """

        # If the herbivore is in cooldown, reduce cooldown and return
        if self.current_cooldown > 0:
            self.current_cooldown -= 1
            return

        empty_neighbors = grid.get_empty_neighbors(self.row, self.col)

        # If there are empty neighbors, choose one randomly and reproduce
        if empty_neighbors.size > 0:
            new_row, new_col = empty_neighbors[np.random.choice(len(empty_neighbors))]

            self.current_cooldown = self.reproduction_cooldown
            grid.cells[new_row, new_col] = Herbivore(new_row, new_col)
            grid.update_empty_cells(new_row, new_col, is_occupied=True)  # Mark cell as occupied

    def load_entity_param_from_yaml(self):
        """ Load object's parameters (T_herbivore_steps, R_herbivore_sight, T_cooldown_steps) from .yaml file. """
        self.reproduction_cooldown = self.game_param[self.name()]['T_cooldown_steps']

        if self.reproduction_cooldown <= 0:
            raise ValueError(f"Invalid T_cooldown_steps: {self.reproduction_cooldown}, must be > 0")

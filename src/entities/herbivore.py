import numpy as np
import yaml
from src.constants import FOLDER_CONFIG_PATH
from src.entities.mobile_entity import MobileEntity
from src.entities.plant import Plant


class Herbivore(MobileEntity):
    """ Herbivore move towards plants, eat them and reproduce. """

    def __init__(self, row: int, col: int) -> None:
        super().__init__(row, col)          # Initialize base constructor
        self.reproduction_cooldown = 0    # Cooldown before it can reproduce again
        self.current_cooldown = 0         # Tracks cooldown progress

    @property
    def emoji(self):
        """
        Returns the emoji representation of the entity.

        This property provides a visual representation of the entity
        using an emoji. Each subclass must define its own specific emoji.

        Returns:
            str: The emoji representing the entity.
        """
        return "🐔"

    @property
    def target_object(self):
        """ Returns the class of the entity that Herbivores target (Plant). """
        return Plant

    def eat(self, target):
        """ Herbivore eats a plant. """
        if isinstance(target, Plant):
            self.current_lifespan = self.lifespan  # Herbivore replenishes lifespan

    # def update_position_on_grid(self, grid, old_pos: tuple[int, int], new_pos: tuple[int, int]):
    #     """
    #     Move towards the closest plant in a (herbivore_sight) radius
    #     or randomly if none are visible
    #     If the Herbivore reaches a Predator, the Herbivore dies
    #     """
    #     old_row, old_col = old_pos
    #     new_row, new_col = new_pos
    #
    #     # Check for reproduction only if we moved to a new position with another herbivore
    #     new_pos_occupied_by_herbivore = (
    #             (new_row != old_row or new_col != old_col) and
    #             isinstance(grid.cells[new_row][new_col], Herbivore) and
    #             grid.cells[new_row][new_col] is not self
    #     )
    #
    #     # Update the grid: vacate old position and occupy new position
    #     if (new_row != old_row) or (new_col != old_col):
    #
    #         # Herbivore reaches another herbivore
    #         if new_pos_occupied_by_herbivore:
    #             self.reproduce(grid)  # Create new Herbivore in a random neighboring cell
    #             grid.cells[new_row][new_col] = self  # Move herbivore to his next location on the grid
    #
    #         # Herbivore reaches Plant
    #         elif isinstance(grid.cells[new_row][new_col], Plant):
    #             grid.cells[new_row][new_col] = self  # Move herbivore to his next location on the grid
    #             self.current_lifespan = self.lifespan  # Refuel lifespan
    #
    #         # Herbivore moves to empty cell
    #         elif grid.cells[new_row][new_col] is None:
    #             grid.cells[new_row][new_col] = self  # Move herbivore to his next location on the grid
    #             grid.update_empty_cells(new_row, new_col, is_occupied=True)
    #
    #         # If Herbivore reaches Predator -> Herbivore dies (clear old position)
    #
    #         # For all cases -> clear herbivore's old position on grid.cells
    #         grid.cells[old_row][old_col] = None
    #         grid.update_empty_cells(old_row, old_col, is_occupied=False)

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
        try:
            # Load configuration settings from a YAML file
            with open(FOLDER_CONFIG_PATH, "r", encoding="utf-8") as file:
                config = yaml.safe_load(file)

            game_param = config.get("game_param", {})

            if 'Herbivore' not in game_param:
                raise ValueError("Missing 'Herbivore' parameters in game_param")

            if 'T_Herbivore_steps' not in game_param['Herbivore']:
                raise ValueError("Missing 'T_Herbivore_steps' for Herbivore")

            if 'R_Herbivore_sight' not in game_param['Herbivore']:
                raise ValueError("Missing 'R_Herbivore_sight' parameters in game_param")

            if 'T_cooldown_steps' not in game_param['Herbivore']:
                raise ValueError("Missing 'T_cooldown_steps' parameters in game_param")

            self.lifespan = game_param['Herbivore']['T_Herbivore_steps']
            self.current_lifespan = self.lifespan

            self.radius_sight = int(game_param['Herbivore']['R_Herbivore_sight'])
            self.reproduction_cooldown = game_param['Herbivore']['T_cooldown_steps']

            if self.radius_sight <= 0:
                raise ValueError(f"Invalid R_Predator_sight: {self.radius_sight}, must be > 0")

            if self.reproduction_cooldown <= 0:
                raise ValueError(f"Invalid T_cooldown_steps: {self.reproduction_cooldown}, must be > 0")

        except FileNotFoundError as not_found:
            raise ValueError(f"Config file not found at {FOLDER_CONFIG_PATH}") from not_found

        except Exception as e:
            raise ValueError(f"Error loading Herbivore parameters: {e}") from e

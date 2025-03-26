import yaml
from src.constants import FOLDER_CONFIG_PATH
from src.entities.herbivore import Herbivore
from src.entities.mobile_entity import MobileEntity


class FastPredator(MobileEntity):
    """ FastPredator acts as Predator except it moves twice faster.
        Predators hunt herbivores and extend their lifespan when they eat. """

    def __init__(self, row: int, col: int):
        super().__init__(row, col)
        self.speed = 2      # Moves twice faster

    @property
    def emoji(self):
        """
        Returns the emoji representation of the entity.

        This property provides a visual representation of the entity
        using an emoji. Each subclass must define its own specific emoji.

        Returns:
            str: The emoji representing the entity.
        """
        return "🦊"

    @property
    def target_object(self):
        """
        Returns the class of the entity that this Predator targets.

        Predators seek out Herbivores as their primary food source. This property
        defines the type of entity they move towards in the simulation.

        Returns:
            Type[Entity]: The class reference of the entity this Predator targets (Herbivore).
        """
        return Herbivore

    def eat(self, target):
        """ Predator eats a herbivore and resets its lifespan. """
        if isinstance(target, Herbivore):
            self.current_lifespan = self.lifespan

    # def update_position_on_grid(self, grid, old_pos: tuple[int, int], new_pos: tuple[int, int]):
    #     """ Move towards the closest herbivore they can see in a (herbivore_sight) radius
    #         or randomly if none are visible.
    #          If predator reaches a Plant, the Plant dies."""
    #
    #     old_row, old_col = old_pos
    #     new_row, new_col = new_pos
    #
    #     # Update the grid: vacate old position and occupy new position
    #     if new_row != old_row or new_col != old_col:
    #
    #         # Predator reaches Plant
    #         if isinstance(grid.cells[new_row][new_col], Plant):
    #             grid.cells[new_row][new_col] = self  # Move predator to his next location on the grid
    #
    #         # Predator reaches Herbivore
    #         elif isinstance(grid.cells[new_row][new_col], Herbivore):
    #             grid.cells[new_row][new_col] = self  # Move predator to his next location on the grid
    #             self.current_lifespan = self.lifespan  # Refuel lifespan
    #
    #         # Predator reaches to empty cell
    #         elif grid.cells[new_row][new_col] is None:
    #             grid.cells[new_row][new_col] = self  # Move predator to his next location on the grid
    #             grid.update_empty_cells(new_row, new_col, is_occupied=True)
    #
    #         # Predator reaches another Predator (do nothing)
    #
    #         # For all cases -> clear predator's old position on grid.cells
    #         grid.cells[old_row][old_col] = None
    #         grid.update_empty_cells(old_row, old_col, is_occupied=False)

    def load_entity_param_from_yaml(self):
        """ Load object's parameters (T_predator_steps, R_predator_sight) from .yaml file. """
        try:
            with open(FOLDER_CONFIG_PATH, "r", encoding="utf-8") as file:
                config = yaml.safe_load(file)

            game_param = config.get("game_param", {})

            if 'FastPredator' not in game_param:
                raise ValueError("Missing 'FastPredator' parameters in game_param")

            if 'T_FastPredator_steps' not in game_param['FastPredator']:
                raise ValueError("Missing 'T_FastPredator_steps' for FastPredator")

            if 'R_FastPredator_sight' not in game_param['FastPredator']:
                raise ValueError("Missing 'R_FastPredator_sight' parameters in game_param")

            self.lifespan = game_param['FastPredator']['T_FastPredator_steps']
            self.current_lifespan = self.lifespan
            self.radius_sight = int(game_param['FastPredator']['R_FastPredator_sight'])

            if self.radius_sight <= 0:
                raise ValueError(f"Invalid R_FastPredator_sight: {self.radius_sight}, must be > 0")

        except FileNotFoundError as not_found:
            raise ValueError(f"Config file not found at {FOLDER_CONFIG_PATH}") from not_found

        except Exception as e:
            raise ValueError(f"Error loading Predator parameters: {e}") from e

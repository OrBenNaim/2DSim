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

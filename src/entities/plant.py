from src.entities.entity import Entity


class Plant(Entity):
    """ Plants don't move, they die after fix steps or after being eaten """

    @property
    def emoji(self):
        """
        Returns the emoji representation of the entity.

        This property provides a visual representation of the entity
        using an emoji. Each subclass must define its own specific emoji.

        Returns:
            str: The emoji representing the entity.
        """
        return "🌱"

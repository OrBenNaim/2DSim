from src.entities.entity import Entity


class Tree(Entity):
    """ Tree don't move, they die after fix steps """
    def __init__(self, row: int, col: int):
        super().__init__(row, col)
        self.lifespan = 0
        self.current_lifespan = 0   # This kind of object never live

    @property
    def emoji(self):
        return "🌳"

    def load_entity_param_from_yaml(self):
        """ Load object's parameters (T_Object_steps) from .yaml file.
            Tree is static parameter and doesn't have any object parameters """
        pass

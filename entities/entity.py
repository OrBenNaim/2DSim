class Entity:
    """ Base class for all entities in the simulation """
    def __init__(self, row: int, col: int, lifespan: int) -> None:
        self.row = row
        self.col = col
        self.lifespan = lifespan

    def move(self, grid):
        """ Defines how the entity moves, Each subclass will implement this """
        pass

    def reproduce(self, grid):
        """ Defines reproduction behavior, Each subclass will implement this """
        pass

    def is_alive(self):
        """ Checks if the entity still alive """
        return self.lifespan > 0


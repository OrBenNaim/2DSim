from entity import Entity

class Plant(Entity):
    """ Plants don't move, they die after fix steps or after being eaten """
    def __init__(self, row: int, col: int, lifespan: int):
        super().__init__(row, col, lifespan)

    # Plants don't move and can't reproduce
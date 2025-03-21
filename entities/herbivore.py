from entity import Entity

class Herbivore(Entity):
    """ Herbivore move towards plants, eat them and reproduce  """
    def __init__(self, row: int, col: int, lifespan: int, herbivore_sight: int, reproduction_cooldown: int) -> None:
        super().__init__(row, col, lifespan)
        self.herbivore_sight = herbivore_sight
        self.reproduction_cooldown = reproduction_cooldown      # Cooldown before it can reproduce again
        self.current_cooldown = 0   # Tracks cooldown progress


    def move(self, grid):
        """ Move towards the closest plant they can see in a (herbivore_sight) radius
            or randomly if none are visible """
        plant = self.find_nearest_plant(grid)
        if plant:
            self.move_towards(plant)

        else:
            self.move_randomly()
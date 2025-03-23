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


    def reproduce(self, grid) -> None:
        """ Staying in the same space and spawning another herbivore
            in a random neighboring cell if cooldown is over """
        if self.current_cooldown > 0:
            self.current_cooldown -= 1
            return

        # else, cooldown is over
        # Create all neighbor indexes
        ref_shifts = [

        ]

        neighbors = grid[self.row - 1 : self.row + 2, self.col - 1 : self.col + 2], (self.row, self.col)








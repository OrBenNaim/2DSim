import yaml
from src.entities.entity import Entity
from src.constants import FOLDER_CONFIG_PATH


class Plant(Entity):
    """ Plants don't move, they die after fix steps or after being eaten """
    def __init__(self, row: int, col: int):
        super().__init__(row, col)

    @property
    def emoji(self):
        return "🌱"

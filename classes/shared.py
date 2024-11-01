"""file for all shared classes"""


class BaseObject:
    """base class for every physical object in the game"""

    def __init__(self, x: int, y: int, physical: bool = True):
        self.x = x
        self.y = y
        self.physical = physical  # whether the object exists in the physical world, if no, it's invisible.

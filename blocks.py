from classes.block import Block, Liquid

class Dirt(Block):
    """class for a dirt block"""

    def __init__(self, x: int, y: int):
        super().__init__(x, y, "🟫")

    def tick(self, world):
        """called every game tick"""
        return world


class Grass(Block):
    """class for a grass block"""

    def __init__(self, x: int, y: int):
        super().__init__(x, y, "🟩")

    def tick(self, world):
        """called every game tick"""
        return world


class Wood(Block):
    """class for a wood block"""

    def __init__(self, x: int, y: int):
        super().__init__(x, y, "🪵")

    def tick(self, world):
        """called every game tick"""
        return world


class Leaf(Block):
    """class for a leaf block"""

    def __init__(self, x: int, y: int):
        super().__init__(x, y, "🍃", solid=False)

    def tick(self, world):
        """called every game tick"""
        return world

# liquid blocks
class Water(Liquid):
    """class for a water block"""

    def __init__(self, x: int, y: int):
        super().__init__(x, y, "🌊", 90)



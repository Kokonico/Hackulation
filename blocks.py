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


class ErrorBlock(Block):
    """class for a block that has errored out, if you see one of these, something bad has happened"""

    def __init__(self, x: int, y: int, error: Exception | BaseException):
        super().__init__(x, y, "�")
        self.error = error

    def tick(self, world):
        """called every game tick"""
        return world

    def __str__(self):
        return f"""
        Something bad happened here...
        Error: {self.error}
        """

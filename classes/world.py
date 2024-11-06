"""the entire world of the game"""
from blocks import ErrorBlock
from classes.block import Block
from classes.entities import Entity

from noise import pnoise2

sea_level = 30  # sea level (in percentage)


class World:
    """class for the world"""
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.world_array = [[None for _ in range(width)] for _ in range(height)]

    def tick(self):
        """called every game tick"""
        for row in self.world_array:
            for block in row:
                if isinstance(block, Block):
                    if not block.skip_tick:
                        try:
                            self.world_array = block.tick(self).world_array
                        except Exception as e:
                            self.world_array[block.y][block.x] = ErrorBlock(block.x, block.y, e)
                    else:
                        block.skip_tick = False
                        self.world_array[block.y][block.x] = block
                elif isinstance(block, Entity):
                    block.tick()

    def display(self):
        """display the world"""
        for row in self.world_array:
            for block in row:
                if isinstance(block, Block) or isinstance(block, Entity):
                    print(block.visual(), end="")
                else:
                    print(" ", end="")
            print()

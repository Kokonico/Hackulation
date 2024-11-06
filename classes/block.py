"""the world is made up of blocks, which are the basic building blocks of the game"""

from classes.shared import BaseObject
import random


def is_valid_block(x, y, world):
    """return whether the block is valid"""
    if x < 0 or x >= world.width or y < 0 or y >= world.height:
        return False
    return True


class Block(BaseObject):
    """class for a block"""

    def __init__(self, x: int, y: int, appearance: str, solid: bool = True, skip_tick: bool = False):
        super().__init__(x, y)
        self.solid = solid
        self.appearance = appearance
        self.skip_tick = skip_tick

    def tick(self, world):
        """called every game tick"""
        return world  # return the world after the tick

    def __str__(self):
        return f"""
        Block: {self.appearance}
        solid: {self.solid}
        """

    def visual(self):
        """return the visual representation of the block"""
        return self.appearance


class Liquid(Block):
    """class for a liquid block"""

    def __init__(self, x: int, y: int, appearance: str, viscosity: int,
                 liquid_level: float = 100, surface_tension: float = 1.0, skip_tick: bool = False):
        super().__init__(x, y, appearance, solid=False, skip_tick=skip_tick)
        self.viscosity = viscosity
        self.liquid_level = liquid_level
        self.surface_tension = surface_tension
        self.threshold = 0.1
        # the higher the viscosity, the less liquid can move

    def tick(self, world):
        """called every game tick"""

        # LIQUID MOVEMENT
        # 1. attempt to move down
        # 2. if not possible, attempt to move to the sides 3. equalize the
        # liquid levels of the blocks to the sides (that means that the liquid level of this block will be the
        # average of the liquid levels of the blocks next to it)

        blocks_to_move_to = []

        # move down
        if self.can_flow_into(self.x, self.y + 1, world):
            # flow into the block below
            if world.world_array[self.y + 1][self.x] is None:
                # if the block below is empty, move down
                world.world_array[self.y + 1][self.x] = self.__class__(self.x, self.y + 1, self.appearance, self.viscosity,
                                                                       self.liquid_level, skip_tick=True)
                world.world_array[self.y][self.x] = None
                self.liquid_level = 0
            else:
                # empty as much liquid as possible into the block below
                block_below = world.world_array[self.y + 1][self.x]
                if block_below.liquid_level + self.liquid_level <= 100:
                    block_below.liquid_level += self.liquid_level
                    self.liquid_level = 0
                    world.world_array[self.y][self.x] = None
                else:
                    # see how much liquid can be moved
                    liquid_to_move = 100 - block_below.liquid_level
                    block_below.liquid_level = 100
                    self.liquid_level -= liquid_to_move
                    if self.liquid_level <= 0:
                        world.world_array[self.y][self.x] = None
        if self.liquid_level > 0:
            # move to the sides
            blocks_to_move_to = self.get_blocks_to_flow_into(world)

            # now we have the blocks we want to move to

            if len(blocks_to_move_to) > 0:
                # get the total liquid of the blocks next to me
                total_liquid = self.get_all_liquid_in_blocks(blocks_to_move_to, world) + self.liquid_level
                # get the average liquid level
                average_liquid = total_liquid / (len(blocks_to_move_to) + (1 if self.liquid_level > self.threshold else 0))
                # check if any of the blocks next to me are None
                NoneBlocks = []
                for block in blocks_to_move_to:
                    if world.world_array[block[1]][block[0]] is None:
                        NoneBlocks.append(block)
                # if there are None blocks, check if the liquid can flow into them (if surface tension allows it)
                if len(NoneBlocks) > 0 and average_liquid < self.surface_tension:
                    # we can't flow into the None blocks
                    blocks_to_move_to = [block for block in blocks_to_move_to if world.world_array[block[1]][block[0]] is not None]
                    # recalculate the average liquid (total liquid is the same)
                    average_liquid = total_liquid / (len(blocks_to_move_to) + (1 if self.liquid_level > self.threshold else 0))

                # move the liquid
                if self.liquid_level > self.threshold:
                    old_liquid_level = self.liquid_level
                    self.liquid_level = average_liquid
                else:
                    self.liquid_level = 0
                for block in blocks_to_move_to:
                    if world.world_array[block[1]][block[0]] is not None:
                        world.world_array[block[1]][block[0]].liquid_level = average_liquid
                    else:
                        world.world_array[block[1]][block[0]] = self.__class__(block[0], block[1], self.appearance, self.viscosity, average_liquid, skip_tick=True)

        # if the liquid level is 0, remove the block
        if self.liquid_level <= 0:
            world.world_array[self.y][self.x] = None

        return world  # return the modified world after the tick

    def can_flow_into(self, x, y, world, block_higher_level=False):
        """return whether the liquid can flow into the block"""
        if not is_valid_block(x, y, world):
            return False

        block = world.world_array[y][x]

        if block is None:
            return True
        elif isinstance(block, self.__class__):
            if block_higher_level:
                return block.liquid_level < self.liquid_level
            else:
                return block.liquid_level < 100

        return False

    def get_blocks_to_flow_into(self, world):
        """return the blocks the liquid can flow into"""
        blocks = []
        if self.can_flow_into(self.x + 1, self.y, world):
            blocks.append((self.x + 1, self.y))
        if self.can_flow_into(self.x - 1, self.y, world):
            blocks.append((self.x - 1, self.y))
        return blocks

    def get_all_liquid_in_blocks(self, blocks, world):
        """return the total liquid in the blocks"""
        total_liquid = 0
        for block in blocks:
            if world.world_array[block[1]][block[0]] is not None:
                total_liquid += world.world_array[block[1]][block[0]].liquid_level
        return total_liquid

    def __str__(self):
        return f"""
        Liquid: {self.appearance}
        viscosity: {self.viscosity}
        surface tension: {self.surface_tension}
        liquid level: {self.liquid_level}
        """

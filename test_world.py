import curses
import time

from classes.world import World
from blocks import Liquid, Block


def create_world(width, height):
    return World(width, height)


def display_world(stdscr, world, cursor_x, cursor_y, total_liquid):
    stdscr.clear()
    for y, row in enumerate(world.world_array):
        for x, block in enumerate(row):
            if isinstance(block, Block) or isinstance(block, Liquid):
                stdscr.addstr(y, x, "^" if cursor_y == y and cursor_x == x else block.visual())
            else:
                stdscr.addstr(y, x, "^" if cursor_y == y and cursor_x == x else ".")

    # show block info
    block = world.world_array[cursor_y][cursor_x]
    stdscr.addstr(world.height + 1, 0, f"Total liquid: {total_liquid}")
    stdscr.addstr(world.height + 2, 0, block.__str__())
    stdscr.refresh()


def main(stdscr):
    curses.curs_set(0)
    width, height = 40, 40
    world = create_world(width, height)
    cursor_x, cursor_y = 0, 0
    total_liquid = 0.0

    while True:
        total_liquid = 0.0
        for row in world.world_array:
            for block in row:
                if isinstance(block, Liquid):
                    total_liquid += block.liquid_level
        display_world(stdscr, world, cursor_x, cursor_y, total_liquid)
        key = stdscr.getch()

        if key == curses.KEY_UP and cursor_y > 0:
            cursor_y -= 1
        elif key == curses.KEY_DOWN and cursor_y < height - 1:
            cursor_y += 1
        elif key == curses.KEY_LEFT and cursor_x > 0:
            cursor_x -= 1
        elif key == curses.KEY_RIGHT and cursor_x < width - 1:
            cursor_x += 1
        elif key == ord('q'):
            break
        elif key == ord('l'):
            world.world_array[cursor_y][cursor_x] = Liquid(cursor_x, cursor_y, "~", 100, 100, 1)
        elif key == ord('b'):
            world.world_array[cursor_y][cursor_x] = Block(cursor_x, cursor_y, "#")
        elif key == ord('d'):
            world.world_array[cursor_y][cursor_x] = None
        elif key == ord(' '):
            world.tick()


if __name__ == "__main__":
    curses.wrapper(main)
    # world = create_world(10, 10)
    # until_water_settles(world)

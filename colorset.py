import curses
from random import randint


class ColorSet:
    def __init__(self):
        self.colors = [
            [curses.COLOR_GREEN, curses.COLOR_BLUE, curses.COLOR_CYAN, curses.COLOR_BLACK],
            [curses.COLOR_BLACK, curses.COLOR_WHITE, curses.COLOR_CYAN, curses.COLOR_BLACK],
            [curses.COLOR_YELLOW, curses.COLOR_BLACK, curses.COLOR_BLUE, curses.COLOR_BLACK],
            [curses.COLOR_BLUE, curses.COLOR_WHITE, curses.COLOR_YELLOW, curses.COLOR_BLACK],
            [curses.COLOR_YELLOW, curses.COLOR_MAGENTA, curses.COLOR_BLUE, curses.COLOR_BLACK],
            [curses.COLOR_BLACK, curses.COLOR_GREEN, curses.COLOR_MAGENTA, curses.COLOR_BLACK],
            [curses.COLOR_MAGENTA, curses.COLOR_YELLOW, curses.COLOR_WHITE, curses.COLOR_BLACK],
            [curses.COLOR_WHITE, curses.COLOR_BLUE, curses.COLOR_GREEN, curses.COLOR_BLACK],
            [curses.COLOR_GREEN, curses.COLOR_BLACK, curses.COLOR_WHITE, curses.COLOR_BLACK],
            [curses.COLOR_BLUE, curses.COLOR_BLACK, curses.COLOR_YELLOW, curses.COLOR_BLACK],
            [curses.COLOR_BLACK, curses.COLOR_MAGENTA, curses.COLOR_BLUE, curses.COLOR_BLACK],
            [curses.COLOR_CYAN, curses.COLOR_BLUE, curses.COLOR_MAGENTA, curses.COLOR_BLACK],
            [curses.COLOR_MAGENTA, curses.COLOR_BLACK, curses.COLOR_GREEN, curses.COLOR_BLACK],
            [curses.COLOR_CYAN, curses.COLOR_BLACK, curses.COLOR_YELLOW, curses.COLOR_BLACK],
            [curses.COLOR_WHITE, curses.COLOR_BLACK, curses.COLOR_MAGENTA, curses.COLOR_BLACK],
        ]

    def get_colors(self):
        num = randint(0, len(self.colors) - 1)
        return tuple(self.colors[num])

    # 0:black, 1:red, 2:green, 3:yellow, 4:blue, 5:magenta, 6:cyan, and 7:white.

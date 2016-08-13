# Authors                  Connor Pacala(Network Developer),
#                          Joseph Vidal(Engine Developer),
#                          Paul Zotz(Input and Tools Developer)
# Date Created:            7/14/2016
# Date Last Modified:      7/22/2016
# File Name:               colorset.py
#
# Overview:                This is a set of color palettes that are used to give the
#                          games aesthetic variety
# Citations:               This is color information researched at
#                          https://docs.python.org/2/howto/curses.html to incorporate
#                          color into the the game presentation
import curses
from random import randint

# Available color set reminder
# 0:black, 1:red, 2:green, 3:yellow, 4:blue, 5:magenta, 6:cyan, and 7:white.


class ColorSet:
    def __init__(self):
        # Color palettes the are picked at random to represent the games levels
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

    # randomly picks from the self.colors palettes and returns the selected palette
    def get_colors(self):
        num = randint(0, len(self.colors) - 1)
        return tuple(self.colors[num])

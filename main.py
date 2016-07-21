import curses
from level import LevelGen
from menu import menu

# set up curses - to be passed to menu object, game engine, etc
stdscr = curses.initscr()
stdscr.nodelay(1)
stdscr.keypad(1)
curses.cbreak()
curses.noecho()
curses.start_color()
curses.curs_set(0)

# user menu options - match to menu options in mainmenu.txt
newGameChoice = 1
highScoreChoice = 2
quitChoice = 3
gameMenu = menu("mainmenu.txt", stdscr)
while True:  # return to menu until user chooses to quit

    menuChoice = gameMenu.menuLaunch() 
    if menuChoice == quitChoice:
        break

    if menuChoice == highScoreChoice:
        # launch high score screen here
        break

    if menuChoice == newGameChoice:
        grid = []
        height = 23
        width = 79
        running = True
    gridMaker = LevelGen(grid, height, width, stdscr)
    gridMaker.level_build()
    gridMaker.level_run(running)



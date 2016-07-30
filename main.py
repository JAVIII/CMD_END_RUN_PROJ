# Authors                  Connor Pacala(Network Developer),
#                          Joseph Vidal(Engine Developer),
#                          Paul Zotz(Input and Tools Developer)
# Date Created:            7/08/2016
# Date Last Modified:      7/22/2016
# File Name:               main.py
#
# Overview:                This is a two-dimensional side scrolling endless runner
#                          with one player controlling the y axis of the "hero" and
#                          another player controlling the x axis over a networked
#                          connection.  If the players touch a wall, obstacle, or
#                          enemy the game is over and will return to the main menu.
#                          A log of furthest distance travelled is kept and can be
#                          viewed from the main menu.

import curses
from level import LevelGen
from menu import menu
from highscore import highScore

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
gameMenu = menu("mainmenu.txt", "highscore.txt", stdscr)
scoreTracker = highScore("highscore.xml")
scoreTracker.readFile()  # read high score file
scoreTracker.readScore() 
currentHighScore = scoreTracker.getScore()

while True:  # return to menu until user chooses to quit

    menuChoice = gameMenu.menuLaunch() 
    if menuChoice == quitChoice:
        break

    if menuChoice == highScoreChoice:
        gameMenu.highScoreLaunch(currentHighScore)

    if menuChoice == newGameChoice:
        grid = []
        height = 23
        width = 79
        running = True

        gridMaker = LevelGen(grid, height, width, stdscr)  # Initialize the game
        gridMaker.level_build() # Generate initial game screen
        score = gridMaker.level_run(running)  # run primary game loop - returns final score once game is over
        # check for new high score and write to file if found
        if score > currentHighScore: # check for new high score
            currentHighScore = score
            scoreTracker.setScore(currentHighScore) # set current high score    
            scoreTracker.writeScore() # write current high score to high score file

    stdscr.clear()



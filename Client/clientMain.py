# Authors                  Connor Pacala(Network Developer),
#                          Joseph Vidal(Engine Developer),
#                          Paul Zotz(Input and Tools Developer)
# Date Created:            7/08/2016
# Date Last Modified:      7/31/2016
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
import ConfigParser
from clientLevel import LevelGen
from clientMenu import menu
from highscore import highScore
from client import ClientUDP

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
menuFile = "mainmenu.txt"
hScoreFile = "highscore.txt"
gameOverFile = "gameover.txt"
waitingFile = "waitforplayers.txt"

#get server and port from config file
config = ConfigParser.RawConfigParser()
config.read("serverdat.cfg")

host = config.get("Server", "host")
port = config.getint("Server", "port")

client = ClientUDP(host, port)

gameMenu = menu(menuFile, hScoreFile, gameOverFile, waitingFile, client,  stdscr)
scoreTracker = highScore("highscore.xml")
scoreTracker.readFile()  # read high score file
scoreTracker.readScore() 
currentHighScore = scoreTracker.getScore()



while True:  # return to menu until user chooses to quit
    clientA = False
    clientB = False
    newHighScore = False
    menuChoice, clientA = gameMenu.menuLaunch()
    if menuChoice == quitChoice:
        break

    if menuChoice == highScoreChoice:
        gameMenu.highScoreLaunch(currentHighScore)

    #menuChoice = seed for levelGen
    else:
        if not clientA:
            clientB = True

        gameMenu.waitForPlayersLaunch(clientA, clientB)
        # new game setup
        grid = []
        height = 23
        width = 79
        running = True

        gridMaker = LevelGen(grid, height, width, menuChoice, client, stdscr)  # Initialize the game
        gridMaker.level_build() # Generate initial game screen
        score = gridMaker.level_run(running)  # run primary game loop - returns final score once game is over
        # check for new high score and write to file if found
        if score > currentHighScore: # check for new high score
            newHighScore = True
            currentHighScore = score
            scoreTracker.setScore(currentHighScore) # set current high score    
            scoreTracker.writeScore() # write current high score 	

        gameMenu.gameOverLaunch(score, newHighScore)

    stdscr.clear()

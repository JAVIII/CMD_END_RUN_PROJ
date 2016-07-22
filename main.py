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
scoreTracker.readFile() #read high score file
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
    	gridMaker = LevelGen(grid, height, width, stdscr)
    	gridMaker.level_build()
    	score = gridMaker.level_run(running) 
        # check for new high score and write to file if found
        if score > currentHighScore:
            currentHighScore = score
            scoreTracker.setScore(currentHighScore)    
            scoreTracker.writeScore()

	stdscr.clear() 
       



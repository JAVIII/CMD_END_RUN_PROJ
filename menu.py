import curses
import sys
import re

class menu():
    def __init__(self, menuFile, highScoreFile, stdscr):
	self.menuFile = menuFile
        self.highScoreFile = highScoreFile
	self.stdscr = stdscr
        self.menuChars = []
        self.highScoreChars = []	

    # reads file at filename and stores all characters (including newlines)
    def readFile(self, filename):
        thisFile = open(filename)
        fileChars = []
        while True:
            c = thisFile.read(1)
            if not c:
                break
            fileChars.append(c)        

	thisFile.close()
        return fileChars 
   
    ''' renders menu based on characters stored in menuChars.
        expects characters read from a menu text file in a certain format:
            - 80 x 24 characters (excluding newlines)
            - lines separated by newline characters
            - menu options numbered in ascending order starting with 1
            - certain characters used (to achieve desired colors)
    '''
    def renderScreen(self, screenChars):
        row = 0
        col = 0
        options = 0
        cursRow = 0
        cursCol = 0 
        highScore = False
        
        # will fill standard terminal window and work (with issues) on smaller
        curses.resizeterm(30, 85) 
        
        for c in screenChars:
            if c == '\n':
                row += 1
                col = 0
                continue
            
            if c == '#':
                self.stdscr.addch(row, col, c, curses.color_pair(1))
            elif re.match(r'[,()`/\\_]', c): 
                self.stdscr.addch(row, col, c, curses.color_pair(2))
            elif re.match(r'[\d\.\w]', c):
                self.stdscr.addch(row, col, c, curses.color_pair(4))
            else:
                self.stdscr.addch(row, col, c)

            if c == '1': # determine where to put cursor (player file 
                cursRow = row
                cursCol = col - 2
                self.stdscr.addch(cursRow, cursCol, '@', curses.color_pair(3))
            elif c == ':': #if we have a colon then this is a high score screen
                cursRow = row
                cursCol = col + 2
                
            if c.isdigit() and not highScore:
                options += 1
        
            col += 1

        curses.resizeterm(24, 80) #resize terminal back to standard

        return options, cursRow, cursCol        
        
    def clearRefresh(self):
        self.stdscr.clear()
        self.stdscr.refresh()
            
    def menuLaunch(self):
        if len(self.menuChars) == 0:
	    self.menuChars = self.readFile(self.menuFile)

        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        
        #call renderMenu and get number of options and @ location
        options, row, col = self.renderScreen(self.menuChars)
        selectedOption = 1
        #self.stdscr.refresh()

        while True: #menu input loop - user can press number or select & enter
            c = self.stdscr.getch()
            if c == -1:
                continue
            
            if c >= ord('1') and c <= (ord('0') + options): #number input
                self.clearRefresh()
                return int(chr(c)) 
            if c == curses.KEY_UP:
                if selectedOption > 1:
                    self.stdscr.addch(row, col, ' ')
                    row -= 1
                    selectedOption -= 1
                    self.stdscr.addch(row, col, '@', curses.color_pair(3))
                    self.stdscr.refresh()
            if c == curses.KEY_DOWN:
                if selectedOption < options:
                    self.stdscr.addch(row, col, ' ')
                    row += 1
                    selectedOption += 1
                    self.stdscr.addch(row, col, '@', curses.color_pair(3))
                    self.stdscr.refresh() 
            if c == curses.KEY_ENTER or c == 10:
            	if selectedOption >= 1 and selectedOption <= options:
                    self.clearRefresh()
                    return selectedOption

    def highScoreLaunch(self, score):
        if len(self.highScoreChars) == 0:
            self.highScoreChars = self.readFile(self.highScoreFile)
        
        options, row, col = self.renderScreen(self.highScoreChars)
        self.stdscr.addstr(row, col, str(score))
  
        while True:
            c = self.stdscr.getch()
            if c == -1:
                continue
            if c == curses.KEY_ENTER or c == 10 or c == 13:
                break

'''
stdscr = curses.initscr()
stdscr.nodelay(1)
stdscr.keypad(1)
curses.cbreak()
curses.noecho()
curses.start_color()
curses.curs_set(0)       
thisMenu = menu("mainmenu.txt", stdscr)
thisMenu.menuLaunch()
'''

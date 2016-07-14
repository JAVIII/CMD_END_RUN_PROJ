import curses
import sys
import re

class menu():
    def __init__(self, filename, stdscr):
	self.filename = filename
	self.stdscr = stdscr
        self.menuChars = []
	

    # reads file at filename and stores all characters (including newlines)
    def readFile(self):
        menuFile = open(self.filename)
        while True:
            c = menuFile.read(1)
            if not c:
                break
            self.menuChars.append(c)        

	menuFile.close() 
   
    ''' renders menu based on characters stored in menuChars.
        expects characters read from a menu text file in a certain format:
            - 80 x 24 characters (excluding newlines)
            - lines separated by newline characters
            - menu options numbered in ascending order starting with 1
            - certain characters used (to achieve desired colors)
    '''
    def renderMenu(self):
        row = 0
        col = 0
        options = 0
        selectRow = 0
        selectCol = 0 
        
        # will fill standard terminal window and work (with issues) on smaller
        curses.resizeterm(30, 85) 
        
        for c in self.menuChars:
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

            if c == '1': #determine starting position of player cursor
                cursRow = row
                cursCol = col - 2
                self.stdscr.addch(cursRow, cursCol, '@', curses.color_pair(3))

            if c.isdigit():
                options += 1
        
            col += 1

        curses.resizeterm(24, 80) #resize terminal back to standard

        return options, cursRow, cursCol
        
             
    def menuLaunch(self):
        if len(self.menuChars) == 0:
	    self.readFile()

        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        
        #call renderMenu and get number of options and @ location
        options, row, col = self.renderMenu()
        selectedOption = 1
        #self.stdscr.refresh()

        while True: #menu input loop - user can press number or select & enter
            c = self.stdscr.getch()
            if c == ord('1'):
                break
            if c == ord('2'):
                break
            if c == ord('3'):
                break
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
                    self.stdscr.clear()
                    self.stdscr.refresh()
                    return selectedOption

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

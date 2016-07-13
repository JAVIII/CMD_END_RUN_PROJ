import curses
import sys
import re

class menu():
    def __init__(self):
        self.menuChars = []

    # reads file at filename and stores all characters (including newlines)
    def readFile(self, filename):
        menuFile = open(filename)
        while True:
            c = menuFile.read(1)
            if not c:
                break
            self.menuChars.append(c)         
   
    ''' renders menu based on characters stored in menuChars.
        expects characters read from a menu text file in a certain format:
            - 80 x 24 characters (excluding newlines)
            - lines separated by newline characters
            - menu options numbered in ascending order starting with 1
            - certain characters used (to achieve desired colors)
    '''
    def renderMenu(self, stdscr):
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
                stdscr.addch(row, col, c, curses.color_pair(1))
            elif re.match(r'[,()`/\\_]', c): 
                stdscr.addch(row, col, c, curses.color_pair(2))
            elif re.match(r'[\d\.\w]', c):
                stdscr.addch(row, col, c, curses.color_pair(4))
            else:
                stdscr.addch(row, col, c)

            if c == '1':
                selectRow = row
                selectCol = col - 2
                stdscr.addch(selectRow, selectCol, '@', curses.color_pair(3))

            if c.isdigit():
                options += 1
        
            col += 1

        curses.resizeterm(24, 80) #resize terminal back to standard

        return options, selectRow, selectCol
        
             
    def menuLaunch(self):
        #curses setup
        stdscr = curses.initscr()
        stdscr.nodelay(1)
        stdscr.keypad(1)
        curses.cbreak()
        curses.noecho()
        curses.start_color()
        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        
        #call renderMenu and get number of options and @ location
        options, row, col = self.renderMenu(stdscr)
        selectedOption = 1
        stdscr.refresh()

        while True: #menu input loop - user can press number or select & enter
            c = stdscr.getch()
            if c == ord('1'):
                break
            if c == ord('2'):
                break
            if c == ord('3'):
                break
            if c == curses.KEY_UP:
                if selectedOption > 1:
                    stdscr.addch(row, col, ' ')
                    row -= 1
                    selectedOption -= 1
                    stdscr.addch(row, col, '@', curses.color_pair(3))
                    stdscr.refresh()
            if c == curses.KEY_DOWN:
                if selectedOption < options:
                    stdscr.addch(row, col, ' ')
                    row += 1
                    selectedOption += 1
                    stdscr.addch(row, col, '@', curses.color_pair(3))
                    stdscr.refresh() 
            if c == curses.KEY_ENTER or c == 10:
                if selectedOption == options:
                    break
                #handle pressing enter on other options       
            

        curses.endwin()
        
thisMenu = menu()            
thisMenu.readFile("mainmenu.txt")
thisMenu.menuLaunch()

# Authors                  Connor Pacala(Network Developer),
#                          Joseph Vidal(Engine Developer),
#                          Paul Zotz(Input and Tools Developer)
# Date Created:            7/10/2016
# Date Last Modified:      7/31/2016
# File Name:               menu.py
#
# Overview:     The menu class is used to read simple menu/screen designs in 
#               text files, generate menus/screens in curses based on expected
#               ASCII values, and return any relevant user selections to main.
#            
#          
# Citations:    Curses code based off examples found in documentation:
#	        https://docs.python.org/2/library/curses.html
			

import curses
import sys
import re
import time
import asyncore
import random

class menu():
    def __init__(self, menuFile, highScoreFile, gameOverFile, waitingFile, socket, stdscr):
        self.menuFile = menuFile
        self.highScoreFile = highScoreFile
        self.gameOverFile = gameOverFile
        self.waitingFile = waitingFile
        self.socket = socket
        self.stdscr = stdscr
        self.menuChars = []
        self.highScoreChars = []	
        self.gameOverChars = []
        self.waitingChars = []

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
            elif re.match(r'[,()`/\\_|]', c): 
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

        readyA = False
        readyB = False
        
        seed = 0
        
        while True: #menu input loop - user can press number or select & enter
            asyncore.loop(timeout = 1, count = 1)
            
            p = self.socket.getData()
            
            if p == "" and readyA and readyB:
                return seed
            
            while p != "":
                client, cmd, val = p.split('*')
                val = int(val)
                
                #move character from one point to another
                if cmd == "sel":
                    if client == str(self.socket.clientA):
                        readyA = True
                        self.socket.buildAPacket("A", 0)
                    if  client == str(self.socket.clientB):
                        readyB = True
                        self.socket.buildBPacket("B", 0)
                    if readyA and readyB:
                        random.random()
                        seed = random.randint(0, sys.maxint)
                        self.socket.buildPacket("start", seed)

                    if val == 2:
                        if client == str(self.socket.clientA):
                            readyA =  True
                        elif  client == str(self.socket.clientB):
                            readyB = True
#                            
                        if readyA and readyB:
                            random.random()
                            seed = random.randint(0, sys.maxint)
                            self.socket.buildPacket("start", seed)
                            
                p = self.socket.getData()
                    
    def highScoreLaunch(self, score):
        if len(self.highScoreChars) == 0:
            self.highScoreChars = self.readFile(self.highScoreFile)
        
        options, row, col = self.renderScreen(self.highScoreChars)
        self.stdscr.addstr(row, col, str(score))
        self.stdscr.refresh()
  
        while True:
            c = self.stdscr.getch()
            if c == -1:
                continue
            if c == curses.KEY_ENTER or c == 10 or c == 13:
                break

    def gameOverLaunch(self, score, newScore):
        row = 12
        col = 30

        if len(self.gameOverChars) == 0:
            self.gameOverChars = self.readFile(self.gameOverFile)
       
        self.stdscr.clear()
        self.renderScreen(self.gameOverChars)
        if newScore: 
            self.stdscr.move(row, col)
            self.stdscr.addstr("New high score!")

        self.stdscr.move(row + 1, col)
        self.stdscr.addstr("SCORE: " + str(score))
        self.stdscr.refresh()
        
        while True:
            c = self.stdscr.getch()
            if c == -1:
                continue
            if c == curses.KEY_ENTER or c == 10 or c == 13:
                break

    def waitForPlayersLaunch(self):
        countdown = 9 #must be same value as countdown variable in clientMenu.py for things to sync properly!
        while countdown > 0:
            time.sleep(1)
            countdown -= 1

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

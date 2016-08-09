# Authors                  Connor Pacala(Network Developer),
#                          Joseph Vidal(Engine Developer),
#                          Paul Zotz(Input and Tools Developer)
# Date Created:            7/08/2016
# Date Last Modified:      7/22/2016
# File Name:               level.py
#
# Overview:                This is the primary game engine which generates the levels,
#                          the obstacles in the levels, and calls on the enemy creation,
#                          and player interaction algorithms. Controls player movement
#                          based off of user input
# Citations:               This is color information researched at
#                          https://docs.python.org/2/howto/curses.html to incorporate
#                          color into the the game presentation

import time
import curses
import asyncore
from colorset import ColorSet
import random
from random import randint
from enemies import EnemyGen
from obstacle import Obstacle


class LevelGen:
    # Initialize game
    def __init__(self, level_grid, height, width, seed, socket, stdscr):
        random.seed(seed)
        self.height = height
        self.width = width
        self.level_grid = [[0 for i in range(width)] for j in range(height)]
        self.socket = socket
        self.stdscr = stdscr
        self.heroRow = width / 6
        self.heroCol = height / 2
        self.level_count = 0
        self.currID = 0
        self.enemies = []
        self.obstacles = []
        self.del_enemies = []

    # build initial screen for running game
    def level_build(self):
        for i in range(self.height):
            for j in range(self.width):
                self.level_grid[i][j] = ' '

        # Places initial walls
        for i in range(1, self.width):
            self.level_grid[0][i] = '#'
            self.level_grid[self.height - 1][i] = '#'
#            for j in range(self.width):
 #               if j > 0:
 #                   if i <= 0 or i >= self.height - 1:
#                        wall = Obstacle(self.currID, i, j)
#                        #add wall to obstacles list
#                        self.obstacles.append(wall)
#                        self.socket.buildPacket("wall", str(self.currID) + "*" + str(i) + "*" + str(j))
#                        self.currID += 1

    # update the game at designated intervals to move the level. Additionally calls for creation
    # of obstacles, and enemies and moves them as well
    def level_update(self, top, bottom, player_height, player_depth):

        # Generate continuation of walls
        for i in range(self.height):
                if i <= top or i >= bottom:
                    self.level_grid[i][self.width - 1] = '#'
                
#        for i in range(self.height):
#            for j in range(self.width):
#                if self.level_grid[i][j] == '&' and j != 0:
#                    enemy.enemy_hunt(i, j)

        # Checks for enemy that can no longer chase character and destroys them graphically if they can not
#        for e in self.enemies[:]:
#            if e.width >= 0 and e.width <= self.width and e.height > 0 and e.height < self.height:
#                if e.width < player_depth - 2:
#                    EnemyGen.enemy_death(e, self, top, bottom)
#                    #add deleted enemy to del_enemies list
#                    self.del_enemies.append(e)
 #                   self.socket.buildPacket("delEn", str(e.ID))
 #                   self.enemies.remove(e)

        #handle progression of explosion for deleted enemies and remove enemy when finished
        for e in self.del_enemies[:]:
            death = EnemyGen.enemy_death(e, self, top, bottom)
            if death == -1:
                    self.del_enemies.remove(e)
                    
#        for i in range(self.height):
#            for j in range(self.width):
#                if j != 0:
#                    enemy.enemy_death(i, j)

        # Shift all designated elements left
        
        #shift all enemies left
        for e in self.enemies:
            if e.width >= 0 and e.width <= self.width and e.height > 0 and e.height < self.height:
                self.level_grid[e.height][e.width] = '&'
            
        #shift all walls left
        for o in self.obstacles:
            if o.width > 0 and o.width < self.width:
                self.level_grid[o.height][o.width] = '#'
            
        #shift top and bottom boundary walls if wall has 2 different sizes (i.e. two levels on screen at once)
        for j in range(1, self.width - 1):
            if self.level_grid[top][j + 1] == '#':
                self.level_grid[top][j ] = '#'
            if self.level_grid[bottom][j + 1] == '#':
                self.level_grid[bottom][j] = '#'

#        for i in range(self.height):
#            for j in range(self.width):
#                if self.level_grid[i][j] != ' ' and self.level_grid[i][j] != '@' and j != 0:
#                    temp = self.level_grid[i][j]
#                    self.level_grid[i][j] = ' '
#                    self.level_grid[i][j - 1] = temp

                # Remove elements which have reached the left side of the screen
                if 0 <= i <= self.height and self.level_grid[i][0] != ' ' and self.level_grid[i][0] != '@':
                    self.level_grid[i][0] = ' '

    # Creates obstacles at right side of the screen
    def level_obstacles(self, top, bottom):
        for i in range(self.height):
            if top < i < bottom:
                rand = randint(0, 90)
                if rand == 1:
                    rand2 = randint(0, 4)
                    if rand2 <= (bottom - i):
                        for k in range(rand2):
                            wall = Obstacle(self.currID, i + k, self.width - 1)
                            #add wall to obstacles list
                            self.obstacles.append(wall)
#                            self.socket.buildPacket("wall", str(self.currID) + "*" + str(wall.height) + "*" + str(wall.width))
                            self.currID += 1
#                            self.level_grid[i + k][self.width - 1] = '#'

    # Generate hero
    def place_hero(self):
        self.level_grid[self.heroRow][self.heroCol] = '@'

    # Print game to screen
    def level_draw(self, color, old_color, new_level):

        # Generate colors for this level
        curses.init_pair(1, color[0], color[1])
        curses.init_pair(2, color[2], color[3])

        # Placeholder to preserve passed level's colors until no longer needed
        curses.init_pair(3, old_color[0], old_color[1])
        curses.init_pair(4, old_color[2], old_color[3])

        # Change enemy color while hunting(NOT YET COMPLETE)
        curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(8, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(9, curses.COLOR_BLACK, curses.COLOR_BLACK)

        count = 0

        # Draws game to screen with appropriate color palettes
        for i in range(self.height):
            for j in range(self.width):
                count += 1

                if count == self.width:
                    if self.level_grid[i][j] == '#':
                        self.stdscr.addstr(i, j, self.level_grid[i][j] + "\n", curses.color_pair(1))
                    elif self.level_grid[i][j] == '&':
                        self.stdscr.addstr(i, j, self.level_grid[i][j] + "\n", curses.color_pair(2))
                    elif self.level_grid[i][j] == '%':
                        self.stdscr.addstr(i, j, self.level_grid[i][j] + "\n", curses.color_pair(5) | curses.A_BOLD | curses.A_REVERSE)
                    elif self.level_grid[i][j] == '$':
                        self.stdscr.addstr(i, j, self.level_grid[i][j] + "\n", curses.color_pair(6) | curses.A_BOLD | curses.A_REVERSE)
                    elif self.level_grid[i][j] == '*':
                        self.stdscr.addstr(i, j, self.level_grid[i][j] + "\n", curses.color_pair(7) | curses.A_BOLD | curses.A_REVERSE)
                    elif self.level_grid[i][j] == '+':
                        self.stdscr.addstr(i, j, self.level_grid[i][j] + "\n", curses.color_pair(8) | curses.A_BOLD | curses.A_REVERSE)
                    elif self.level_grid[i][j] == '!' or self.level_grid[i][j] == '~' or self.level_grid[i][j] == '`':
                        self.stdscr.addstr(i, j, self.level_grid[i][j] + "\n", curses.color_pair(9))
                    else:
                        self.stdscr.addstr(i, j, self.level_grid[i][j] + "\n")
                    count = 0
                elif count >= self.width - new_level:
                    if self.level_grid[i][j] == '#':
                        self.stdscr.addstr(i, j, self.level_grid[i][j], curses.color_pair(1))
                    elif self.level_grid[i][j] == '&':
                        self.stdscr.addstr(i, j, self.level_grid[i][j], curses.color_pair(2))
                    elif self.level_grid[i][j] == '%':
                        self.stdscr.addstr(i, j, self.level_grid[i][j] + "\n", curses.color_pair(5) | curses.A_BOLD | curses.A_REVERSE)
                    elif self.level_grid[i][j] == '$':
                        self.stdscr.addstr(i, j, self.level_grid[i][j] + "\n", curses.color_pair(6) | curses.A_BOLD | curses.A_REVERSE)
                    elif self.level_grid[i][j] == '*':
                        self.stdscr.addstr(i, j, self.level_grid[i][j] + "\n", curses.color_pair(7) | curses.A_BOLD | curses.A_REVERSE)
                    elif self.level_grid[i][j] == '+':
                        self.stdscr.addstr(i, j, self.level_grid[i][j] + "\n", curses.color_pair(8) | curses.A_BOLD | curses.A_REVERSE)
                    elif self.level_grid[i][j] == '!' or self.level_grid[i][j] == '~' or self.level_grid[i][j] == '`':
                        self.stdscr.addstr(i, j, self.level_grid[i][j] + "\n", curses.color_pair(9))
                    else:
                        self.stdscr.addstr(i, j, self.level_grid[i][j])
                else:
                    if self.level_grid[i][j] == '#':
                        self.stdscr.addstr(i, j, self.level_grid[i][j], curses.color_pair(3))
                    elif self.level_grid[i][j] == '&':
                        self.stdscr.addstr(i, j, self.level_grid[i][j], curses.color_pair(4))
                    elif self.level_grid[i][j] == '%':
                        self.stdscr.addstr(i, j, self.level_grid[i][j] + "\n", curses.color_pair(5) | curses.A_BOLD | curses.A_REVERSE)
                    elif self.level_grid[i][j] == '$':
                        self.stdscr.addstr(i, j, self.level_grid[i][j] + "\n", curses.color_pair(6) | curses.A_BOLD | curses.A_REVERSE)
                    elif self.level_grid[i][j] == '*':
                        self.stdscr.addstr(i, j, self.level_grid[i][j] + "\n", curses.color_pair(7) | curses.A_BOLD | curses.A_REVERSE)
                    elif self.level_grid[i][j] == '+':
                        self.stdscr.addstr(i, j, self.level_grid[i][j] + "\n", curses.color_pair(8) | curses.A_BOLD | curses.A_REVERSE)
                    elif self.level_grid[i][j] == '!' or self.level_grid[i][j] == '~' or self.level_grid[i][j] == '`':
                        self.stdscr.addstr(i, j, self.level_grid[i][j] + "\n", curses.color_pair(9))
                    else:
                        self.stdscr.addstr(i, j, self.level_grid[i][j])

    # Controls "hero" movement
    def move_hero_row(self, moveBy):
        self.level_grid[self.heroRow][self.heroCol] = ' '
        self.heroRow += moveBy
        self.level_grid[self.heroRow][self.heroCol] = '@'

    def getInput(self):
        c = self.stdscr.getch()
        #no key pressed
        if c == -1:
            return 0, 0
        # -1 for up key, 1 for down key, or 0 for no valid keys
        return int(c == curses.KEY_DOWN) - int(c == curses.KEY_UP), int(c == curses.KEY_RIGHT) - int(c == curses.KEY_LEFT)
		
    # Primary game loop, provides all necessary information for game to run and initiates all game actions
    def level_run(self, running):

        # Initial variable set
        self.level_count = 0
        color_setting = ColorSet()
        color = color_setting.get_colors()
        old_color = color
        counter = 0
        score = 0
        top = 0
        bottom = self.height - 1
        refresh_start = False
        refresh_count = 0
        calc_start = False
        calc_count = 0
        new_level = 0
        level_length = 100
        score_label = "Score: "
        self.place_hero()

        # place score label in bottom left hand corner
        self.stdscr.move(self.height, 0)
        self.stdscr.addstr(score_label)
        
        # Primary loop
        while running:
            asyncore.loop(timeout = 1, count = 1)
			
            timer = int(round(time.clock() * 1000)) # Referenced to maintain updates and refresh rate

            p = self.socket.getData()
            
            while p != "":
                cmd, val = p.split('*')
                if ',' in val:
                    id, x, y = val.split(',')
                    id = int(id)
                    x = int(x)
                    y = int(y)
                else:
                    val = int(val)
                    
                if cmd == "mPV":
                    self.move_hero_row(val)
                #move enemy
                elif cmd == "mE":
                    for e in self.enemies:
                        if e.ID == id:
                            if e.width >= 0 and e.width <= self.width and e.height > 0 and e.height < self.height:
                                self.level_grid[e.height][e.width] = ' '
                            e.height = y
                            e.width = x
                            self.level_grid[e.height][e.width] = '&'
                #move wall
                elif cmd == "mW":
                    for o in self.obstacles:
                        if o.ID == id:
                            if o.width >= 0 and o.width <= self.width and o.height > 0 and o.height < self.height:
                                self.level_grid[o.height][o.width] = ' '
                            o.height = y
                            o.width = x
                            self.level_grid[o.height][o.width] = '#'
                #create enemy
                elif cmd == "cE":
                    enemy = EnemyGen(id, y, x, top, bottom, self.level_grid, player_height, player_depth, self.level_count)
                    self.enemies.append(enemy)
                #create wall
                elif cmd == "cW":
                    wall = Obstacle(id, y, x)
                    self.obstacles.append(wall)
                #delete enemy
                elif cmd == "delE":
                    for e in self.enemies[:]:
                        if e.ID == id:
                            e.width = x
                            e.height = y
                            EnemyGen.enemy_death(e, self, top, bottom)
                            self.del_enemies.append(e)
                            self.enemies.remove(e)
                #delete wall
                elif cmd == "delW":
                    for o in self.obstacles[:]:
                        if o.ID == id:
                            if o.width > 0 and o.width < self.width:
                                self.level_grid[o.height][o.width] = ' '
                                self.obstacles.remove(o)
                elif cmd == "end":
                    return val
                                
                p = self.socket.getData()
                
                
            #get user input
            vIn, hIn = self.getInput()
				
            if vIn != 0:
                self.socket.buildPacket("mV", vIn)
            if hIn != 0:
                self.socket.buildPacket("mH", hIn)
                
            player_height = self.heroRow
            player_depth = self.heroCol

            # Update all aspects of game at designated intervals
            if calc_start is False:
                calc_count = timer
                calc_start = True
            elif calc_start and (timer - calc_count) > 100:  # Interval to update game elements(milliseconds)
                counter += 1
                new_level += 1
                if counter == level_length:
                    if bottom - top > 7:
                        top += 1
                        bottom -= 1
                    counter = 0
                    self.level_count += 1

                # Change color palette upon reaching new level
                elif counter == level_length - 1:
                    old_color = color
                    while old_color == color:
                        color = color_setting.get_colors()
                    new_level = 0

                self.level_update(top, bottom, player_height, player_depth)
                score += 1 # update score whenever level updates
                self.stdscr.move(self.height, len(score_label))
                self.stdscr.addstr(str(score))

                calc_start = False

            # Refreash screen at designated intervals
            if refresh_start is False:
                refresh_count = timer
                refresh_start = True
                self.level_draw(color, old_color, new_level)
            elif refresh_start and (timer - refresh_count) > 16:  # Interval to refresh game screen(milliseconds)
                refresh_start = False
                self.stdscr.refresh()

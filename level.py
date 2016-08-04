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
from colorset import ColorSet
from random import randint
from enemies import EnemyGen
from laser import laser

class LevelGen:
    # Initialize game
    def __init__(self, level_grid, height, width, stdscr):
        self.height = height
        self.width = width
        self.level_grid = [[0 for i in range(width)] for j in range(height)]
        self.stdscr = stdscr
        self.heroRow = width / 6
        self.heroCol = height / 2
        self.level_count = 0
        self.lasers = []
        
    # build initial screen for running game
    def level_build(self):
        for i in range(self.height):
            for j in range(self.width):
                self.level_grid[i][j] = ' '

        # Places initial walls
        for i in range(self.height):
            for j in range(self.width):
                if j > 0:
                    if i <= 0 or i >= self.height - 1:
                        self.level_grid[i][j] = '#'

    # update the game at designated intervals to move the level. Additionally calls for creation
    # of obstacles, and enemies and moves them as well
    def level_update(self, top, bottom, player_height, player_depth):
        # Generate new obstacles
        self.level_obstacles(top, bottom)

        # Generate and place enemies
        enemy = EnemyGen(self.height, self.width, top, bottom, self.level_grid, player_height, player_depth, self.level_count)
        enemy.enemy_spawn()
        
        # Generate continuation of walls
        for i in range(self.height):
                if i <= top or i >= bottom:
                    self.level_grid[i][self.width - 1] = '#'

        # Enemies check for player to interact with
        for i in range(self.height):
            for j in range(self.width):
                if self.level_grid[i][j] == '&' and j != 0:
                    enemy.enemy_hunt(i, j)

        # Checks for enemy that can no longer chase character and destroys them graphically if they can not
        for i in range(self.height):
            for j in range(self.width):
                if j != 0:
                    enemy.enemy_death(i, j)
        
        # Shift all designated elements left
        for i in range(self.height):
            for j in range(self.width):
                if self.level_grid[i][j] != ' ' and self.level_grid[i][j] != '@' and j != 0:
                    temp = self.level_grid[i][j]
                    # make sure laser chars aren't shifted
                    if temp == '-':
                        temp = ' '
                        # fix to make sure char isn't shifted through laser
                        if j<self.width-1 and self.level_grid[i][j + 1] != ' ':
			    for k in self.lasers:
                                if k.getRow() == i and k.getCol() == j:
                                    self.lasers.remove(k)
                            
                            self.level_grid[i][j + 1] = ' '

	            self.level_grid[i][j] = ' '
                    self.level_grid[i][j - 1] = temp
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
                            self.level_grid[i + k][self.width - 1] = '#'

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
        curses.init_pair(10, curses.COLOR_RED, curses.COLOR_RED)
        count = 0

        # Draws game to screen with appropriate color palettes
        for i in range(self.height):
            for j in range(self.width):
                count += 1
                
                if self.level_grid[i][j] == '-':
                    self.stdscr.addstr(i, j, self.level_grid[i][j], curses.color_pair(6))                
                elif count == self.width:
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

    def update_lasers(self):
        # move all laser objects right

        for i in self.lasers:
            row = i.getRow()
            col = i.getCol()
        
            self.level_grid[row][col] = ' '
            on_map = i.advance()
            if on_map:
                row = i.getRow()
                col = i.getCol()
                thisChar = self.level_grid[row][col]
                prevChar = self.level_grid[row][col - 1]
                if thisChar == ' ':
                    self.level_grid[row][col] = '-'
                elif thisChar == '&':
                    self.level_grid[row][col] = ' '
                    self.lasers.remove(i)
                elif prevChar == '#' or thisChar == '#':
                    self.level_grid[row][col] = ' '
                    self.lasers.remove(i)
            else:
                self.lasers.remove(i)


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
        score_label = " Score: "
        laser_label = "Laser: "
        laser_interval = 30 #number of steps before laser replinishes
        laser_max = 5 #max number of lasers player can have
        laser_count = 5
        self.place_hero()
        
        # place score label in bottom left hand corner
        self.stdscr.move(self.height, 0)
        self.stdscr.addstr(score_label)
        
        prev = -1
        # Primary loop
        while running:
            timer = int(round(time.clock() * 1000)) # Referenced to maintain updates and refresh rate

            # temporary single player control code
            c = self.stdscr.getch()
            if c == curses.KEY_UP:
                if self.level_grid[self.heroRow - 1][self.heroCol] == ' ':
                    self.move_hero_row(-1)
                else:  # handle collision
                    return score     
            elif c == curses.KEY_DOWN:
                if self.level_grid[self.heroRow + 1][self.heroCol] == ' ':
                    self.move_hero_row(1)
                else:  # handle collision
                    return score
            elif c == ord(' '): # space bar used to shoot lasers
            
                if laser_count > 0:
                    thisLaser = laser(self.heroRow, self.heroCol + 1, self.width-1)
                    self.lasers.append(thisLaser)
                    laser_count -= 1 
                    

            player_height = self.heroRow
            player_depth = self.heroCol
        
            update_interval = False
            
            # Update all aspects of game at designated intervals
            if calc_start is False:
                calc_count = timer
                calc_start = True
    
            if calc_start and (timer - calc_count) > 100:
                update_interval = True
            if update_interval:  # Interval to update game elements(milliseconds)
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
    
                if (score % laser_interval == 0) and laser_count < laser_max:
                    laser_count = laser_count + 1

                # check for collisions after level update
                #if self.level_grid[self.heroRow][self.heroCol] != '@':
                #    return score

                calc_start = False

            # Refreash screen at designated intervals
            if refresh_start is False:
                refresh_count = timer
                refresh_start = True
                #update laser positions on screen refresh
                self.update_lasers() #looks better than updating on lvl update  
                self.level_draw(color, old_color, new_level)
                # add score and laser count
                self.stdscr.move(self.height, len(score_label))
                self.stdscr.addstr(str(score))
                self.stdscr.move(self.height, self.width-(len(score_label)+10))
                self.stdscr.addstr(laser_label)
                # add a red bar for each laser
                for i in range(laser_count):
                    self.stdscr.addstr('|', curses.color_pair(10))
                    self.stdscr.addstr(' ')
                # make sure rest of laser bar is blacked out
                for i in range(laser_max - laser_count): 
                    self.stdscr.addstr('  ')

                    

                #check for collisions after drawing level
                if self.level_grid[self.heroRow][self.heroCol] != '@':
                    return score
            elif refresh_start and (timer - refresh_count) > 16:  # Interval to refresh game screen(milliseconds)
                refresh_start = False
                self.stdscr.refresh()

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
from laser import laser

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
        self.del_obstacles = []
        self.lasers = []

    # build initial screen for running game
    def level_build(self):
        for i in range(self.height):
            for j in range(self.width):
                self.level_grid[i][j] = ' '

        # Places initial walls
        for i in range(1, self.width):
            self.level_grid[0][i] = '#'
            self.level_grid[self.height - 1][i] = '#'

    # update the game at designated intervals to move the level. Additionally calls for creation
    # of obstacles, and enemies and moves them as well
    def level_update(self, top, bottom, player_height, player_depth):
        # Generate new obstacles
        self.level_obstacles(top, bottom)

        # Generate and place enemies
        enemy = EnemyGen(self.currID, self.height, self.width, top, bottom, self.level_grid, player_height, player_depth, self.level_count)
        if enemy.enemy_spawn():
            self.socket.buildPacket("cE", str(enemy.ID) + "," + str(enemy.width) + "," + str(enemy.height))
            #add enemy to enemies list
            self.enemies.append(enemy)
            self.currID += 1

        # Generate continuation of walls
        for i in range(self.height):
                if i <= top or i >= bottom:
                    self.level_grid[i][self.width - 1] = '#'

        #handle progression of explosion for deleted enemies and remove enemy when finished
        for e in self.del_enemies[:]:
            death = EnemyGen.enemy_death(e, self, top, bottom)
            if death == -1:
                    self.del_enemies.remove(e)
                    
        #explode wall
        for o in self.del_obstacles[:]:
            if(o.wall_break(o.height, o.width) == 1):
                self.del_obstacles.remove(o)
                    
        # Enemies check for player to interact with
        for e in self.enemies[:]:
            temp_x, temp_y = EnemyGen.enemy_hunt(e, player_height, player_depth)
            if temp_x >= 0 and temp_x < self.width and temp_y >= 0 and temp_y< self.height:
                if self.level_grid[temp_y][temp_x] == ' ':
                    self.level_grid[e.height][e.width] = ' '
                    e.height = temp_y
                    e.width = temp_x
                #collision with laser
                elif self.level_grid[temp_y][temp_x] == '-':
                    self.set_effect_char('&', e.height, e.width)
                    self.socket.buildPacket("delE", str(e.ID) + "," + str(e.width) + "," + str(e.height))
                    self.del_enemies.append(e)
                    self.enemies.remove(e)
                    
        # Checks for enemy that can no longer chase character and destroys them graphically if they can not
        for e in self.enemies[:]:
            if e.width >= 0 and e.width <= self.width and e.height > 0 and e.height < self.height:
                if e.width < player_depth - 2:
                    EnemyGen.enemy_death(e, self, top, bottom)
                    #add deleted enemy to del_enemies list
                    self.socket.buildPacket("delE", str(e.ID) + "," + str(e.width) + "," + str(e.height))
                    self.del_enemies.append(e)
                    self.enemies.remove(e)

        #shift all enemies left
        for e in self.enemies:
            if e.width >= 0 and e.width < self.width and e.height >= 0 and e.height < self.height:
                    self.level_grid[e.height][e.width] = ' '
                    e.width -= 1
                    #check for collision with laser
                    if self.level_grid[e.height][e.width] == '-':
                        self.set_effect_char('&', e.height, e.width)
                        self.socket.buildPacket("eE", str(e.ID) + "," + str(e.width) + "," + str(e.height))
                        self.del_enemies.append(e)
                        self.enemies.remove(e)
                    else:
                        self.level_grid[e.height][e.width] = '&'
                        self.socket.buildPacket("mE", str(e.ID) + "," + str(e.width) + "," + str(e.height))
            
        #shift all walls left
        for o in self.obstacles[:]:
            if o.width > 0 and o.width < self.width:
                self.level_grid[o.height][o.width] = ' '
            o.width -= 1
            if o.width > 0 and o.width < self.width:
                #collision with laser
                if self.level_grid[o.height][o.width] == '-':
                    #explode wall
                    self.set_effect_char('#', o.height, o.width)
                    self.socket.buildPacket("eW", str(o.ID) + "," + str(o.width) + "," + str(o.height))
                    self.del_obstacles.append(o)
                    self.obstacles.remove(o)
                else:
                    self.level_grid[o.height][o.width] = '#'
                    self.socket.buildPacket("mW", str(o.ID) + "," + str(o.width) + "," + str(o.height))
            else:
                self.socket.buildPacket("delW", str(o.ID))
                self.obstacles.remove(o)
            
        #shift top and bottom boundary walls if wall has 2 different sizes (i.e. two levels on screen at once)
        for j in range(1, self.width - 1):
            if self.level_grid[top][j + 1] == '#':
                self.level_grid[top][j ] = '#'
            if self.level_grid[bottom][j + 1] == '#':
                self.level_grid[bottom][j] = '#'
        
        #update laser position
        self.update_lasers()
        
    def update_lasers(self):
        # move all laser objects right
        for i in self.lasers[:]:
            row = i.getRow()
            col = i.getCol()
        
            #after updating other objects, check for laser collision (other objects already exploding at this point)
            if self.level_grid[row][col] == '?' or self.level_grid[row][col] == '}':
                self.socket.buildPacket("delL", str(i.ID) + "," + str(col) + "," + str(row))
                self.lasers.remove(i)
                continue
            
            #if no collision, move laser forward
            self.level_grid[row][col] = ' '
            on_map = i.advance()
            if on_map:
                row = i.getRow()
                col = i.getCol()
                thisChar = self.level_grid[row][col]
                
                if thisChar == ' ':
                    self.socket.buildPacket("mL", str(i.ID) + "," + str(col) + "," + str(row))
                    self.level_grid[row][col] = '-'
                else:
                    #collision with wall
                    if self.level_grid[row][col] == '#':
                        for o in self.obstacles[:]:
                            if o.height == row and o.width == col:
                                self.set_effect_char('#', o.height, o.width)
                                self.socket.buildPacket("eW", str(o.ID) + "," + str(o.width) + "," + str(o.height))
                                self.del_obstacles.append(o)
                                self.obstacles.remove(o)
                                self.socket.buildPacket("delL", str(i.ID) + "," + str(col) + "," + str(row))
                                self.lasers.remove(i)
                                break
                    #collision with enemy
                    elif self.level_grid[row][col] == '&':
                        for e in self.enemies[:]:
                            if e.height == row and e.width == col:
                                self.set_effect_char('&', e.height, e.width)
                                self.socket.buildPacket("eE", str(e.ID) + "," + str(e.width) + "," + str(e.height))
                                self.del_enemies.append(e)
                                self.enemies.remove(e)
                                self.socket.buildPacket("delL", str(i.ID) + "," + str(col) + "," + str(row))
                                self.lasers.remove(i)
                                self.set_effect_char(thisChar, row, col)
            else:
                self.socket.buildPacket("delL", str(i.ID) + "," + str(col) + "," + str(row))
                self.lasers.remove(i)
                
    def set_effect_char(self, char, row, col):
        if char == '&':
            self.level_grid[row][col] = '}'
        elif char == '#':
            self.level_grid[row][col] = '?'
                
    # Creates obstacles at right side of the screen
    def level_obstacles(self, top, bottom):
        for i in range(self.height):
            if top < i < bottom:
                rand = randint(0, 90)
                if rand == 1:
                    rand2 = randint(0, 4)
                    if rand2 <= (bottom - i):
                        for k in range(rand2):
                            wall = Obstacle(self.currID, i + k, self.width - 1, self)
                            #add wall to obstacles list
                            self.obstacles.append(wall)
                            self.socket.buildPacket("cW", str(self.currID) + "," + str(wall.width) + "," + str(wall.height))
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
        curses.init_pair(10, curses.COLOR_RED, curses.COLOR_RED)
        count = 0

        # Draws game to screen with appropriate color palettes
        for i in range(self.height):
            for j in range(self.width):
                count += 1
                
                if self.level_grid[i][j] == '-':
                    self.stdscr.addstr(i, j, self.level_grid[i][j], curses.color_pair(6))                
                elif count == self.width:
                    if self.level_grid[i][j] == '#' or self.level_grid[i][j] == ',':
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
                    elif self.level_grid[i][j] == '!' or self.level_grid[i][j] == '~' or self.level_grid[i][j] == '`' or self.level_grid[i][j] == '?' or self.level_grid[i][j] == '}':
                        self.stdscr.addstr(i, j, self.level_grid[i][j] + "\n", curses.color_pair(9))
                    else:
                        self.stdscr.addstr(i, j, self.level_grid[i][j] + "\n")
                    count = 0
                elif count >= self.width - new_level:
                    if self.level_grid[i][j] == '#' or self.level_grid[i][j] == ',':
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
                    elif self.level_grid[i][j] == '!' or self.level_grid[i][j] == '~' or self.level_grid[i][j] == '`' or self.level_grid[i][j] == '?' or self.level_grid[i][j] == '}':
                        self.stdscr.addstr(i, j, self.level_grid[i][j] + "\n", curses.color_pair(9))
                    else:
                        self.stdscr.addstr(i, j, self.level_grid[i][j])
                else:
                    if self.level_grid[i][j] == '#' or self.level_grid[i][j] == ',':
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
                    elif self.level_grid[i][j] == '!' or self.level_grid[i][j] == '~' or self.level_grid[i][j] == '`' or self.level_grid[i][j] == '?' or self.level_grid[i][j] == '}':
                        self.stdscr.addstr(i, j, self.level_grid[i][j] + "\n", curses.color_pair(9))
                    else:
                        self.stdscr.addstr(i, j, self.level_grid[i][j])

    # Controls "hero" movement
    def move_hero(self, moveV, moveH):
        newV = self.heroRow
        newH = self.heroCol
        if not self.heroRow + moveV >= self.height or self.heroRow + moveV < 0:
            newV += moveV
        
        if not self.heroCol + moveH >= self.width or self.heroCol + moveH < 0:
            newH += moveH
            
        self.level_grid[self.heroRow][self.heroCol] = ' '
        self.heroRow = newV
        self.heroCol = newH
        self.level_grid[self.heroRow][self.heroCol] = '@'
        
    # Primary game loop, provides all necessary information for game to run and initiates all game actions
    def level_run(self, running):

        # Initial variable set
        self.level_count = 0
        color_setting = ColorSet()
        color = color_setting.get_colors()
        old_color = color
        counter = 0
        score = 0
        finalScore = 0
        top = 0
        bottom = self.height - 1
        refresh_start = False
        refresh_count = 0
        calc_start = False
        calc_count = 0
        new_level = 0
        level_length = 100
        score_label = "Score: "
        laser_label = "Laser: "
        laser_interval = 30  # number of steps before laser replinishes
        laser_max = 5  # max number of lasers player can have
        laser_count = 5
        self.place_hero()
        moveH = 0
        moveV = 0
        createLaser = False

        # place score label in bottom left hand corner
        self.stdscr.move(self.height, 0)
        self.stdscr.addstr(score_label)
        
        # Primary loop
        while running:
            asyncore.loop(timeout = 1, count = 1)

            timer = int(round(time.clock() * 1000)) # Referenced to maintain updates and refresh rate
            
            p = self.socket.getData()
            
            while p != "":
                client, cmd, val = p.split('*')
                val = int(val)
                if cmd == "mH":
                    if  client == str(self.socket.clientB):
                        moveH += val
                elif cmd == "mV":
                    if client == str(self.socket.clientA):
                        moveV += val
                elif cmd == "fL":
                    createLaser = True
                                  
                p = self.socket.getData()
                
            #move hero after all packets processed
            if self.level_grid[self.heroRow + moveV][self.heroCol + moveH] != '&' and self.level_grid[self.heroRow + moveV][self.heroCol + moveH] != '#' :
                self.move_hero(moveV, moveH)
                self.socket.buildPacket("mP", "-1," + str(moveH) + "," + str(moveV))
                moveV = 0
                moveH = 0
            else:
                self.socket.buildPacket("end", score)
                asyncore.loop(timeout = 1, count = 1)
                return score
                
            #fire laser
            if createLaser:
                createLaser = False
                if  client == str(self.socket.clientB) and laser_count > 0:
                    l = laser(self.currID, self.heroRow, self.heroCol + 1, self.width - 1)
                    self.lasers.append(l)
                    self.socket.buildPacket("cL", str(self.currID))
                    laser_count -= 1
                    self.currID += 1

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
                
                if (score % laser_interval == 0) and laser_count < laser_max:
                    laser_count = laser_count + 1

                calc_start = False

            # Refreash screen at designated intervals
            if refresh_start is False:
                refresh_count = timer
                refresh_start = True
                
                self.level_draw(color, old_color, new_level)
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
                    
                # check for collisions after drawing level
                if self.level_grid[self.heroRow][self.heroCol] != '@':
                    self.socket.buildPacket("end", score)
                    asyncore.loop(timeout = 1, count = 1)
                    return score

            elif refresh_start and (timer - refresh_count) > 16:  # Interval to refresh game screen(milliseconds)
                refresh_start = False
                self.stdscr.refresh()

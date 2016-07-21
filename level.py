import time
import curses
from colorset import ColorSet
from random import randint
from enemies import EnemyGen


class LevelGen:
    def __init__(self, level_grid, height, width, stdscr):
        self.height = height
        self.width = width
        self.levelGrid = [[0 for i in range(width)] for j in range(height)]
        self.stdscr = stdscr
	self.heroRow = width / 6
	self.heroCol = height / 2        

    def level_build(self):
        for i in range(self.height):
            for j in range(self.width):
                self.levelGrid[i][j] = ' '

        for i in range(self.height):
            for j in range(self.width):
                if j > 0:
                    if i <= 0 or i >= self.height - 1 :
                        self.levelGrid[i][j] = '#'

    def level_update(self, top, bottom):

        for i in range(self.height):
            for j in range(self.width):
                if (i <= top or i >= bottom) and j == self.width - 1:
                    self.levelGrid[i][j] = '#'

        for i in range(self.height):
            for j in range(self.width):
                if self.levelGrid[i][j] != ' ' and self.levelGrid[i][j] != '@' and j != 0:
                    temp = self.levelGrid[i][j]
                    self.levelGrid[i][j] = ' '
                    self.levelGrid[i][j - 1] = temp

    def level_obstacles(self, top, bottom):
        for i in range(self.height):
            for j in range(self.width):
                if (i > top or i < bottom) and j == self.width - 1:
                    rand = randint(0, 90)
                    if rand == 1:
                        rand2 = randint(0, 4)
                        if rand2 <= (bottom - i):
                            for k in range(rand2):
                                self.levelGrid[i + k][j] = '#'

                if (i > top or i < bottom) and j == 0 and self.levelGrid[i][j] != ' ' and self.levelGrid[i][j] != '@':
                    self.levelGrid[i][j] = ' '

    def place_hero(self):
        self.levelGrid[self.heroRow][self.heroCol] = '@'
        '''
        for i in range(self.height):
            for j in range(self.width):
                if i == 10 and j == 3:
                    self.levelGrid[i][j] = '@'
        '''

    def level_draw(self, color, old_color, new_level):
        curses.init_pair(1, color[0], color[1])
        curses.init_pair(2, color[2], color[3])
        curses.init_pair(3, old_color[0], old_color[1])
        curses.init_pair(4, old_color[2], old_color[3])
        curses.init_pair(5, curses.COLOR_RED, curses.COLOR_BLACK)
        count = 0

        for i in range(self.height):
            for j in range(self.width):
                count += 1

                if count == self.width:
                    if self.levelGrid[i][j] == '#':
                        self.stdscr.addstr(i, j, self.levelGrid[i][j] + "\n", curses.color_pair(1))
                    elif self.levelGrid[i][j] == '&':
                        self.stdscr.addstr(i, j, self.levelGrid[i][j] + "\n", curses.color_pair(2))
                    else:
                        self.stdscr.addstr(i, j, self.levelGrid[i][j] + "\n")
                    count = 0
                elif count >= self.width - new_level:
                    if self.levelGrid[i][j] == '#':
                        self.stdscr.addstr(i, j, self.levelGrid[i][j], curses.color_pair(1))
                    elif self.levelGrid[i][j] == '&':
                        self.stdscr.addstr(i, j, self.levelGrid[i][j], curses.color_pair(2))
                    else:
                        self.stdscr.addstr(i, j, self.levelGrid[i][j])
                else:
                    if self.levelGrid[i][j] == '#':
                        self.stdscr.addstr(i, j, self.levelGrid[i][j], curses.color_pair(3))
                    elif self.levelGrid[i][j] == '&':
                        self.stdscr.addstr(i, j, self.levelGrid[i][j], curses.color_pair(4))
                    else:
                        self.stdscr.addstr(i, j, self.levelGrid[i][j])
    
    def move_hero_row(self, moveBy):
        self.levelGrid[self.heroRow][self.heroCol] = ' ' 
        self.heroRow += moveBy
        self.levelGrid[self.heroRow][self.heroCol] = '@'

    def level_run(self, running):
        color_setting = ColorSet()
        color = color_setting.get_colors()
        old_color = color
        counter = 0
        top = 0
        bottom = self.height - 1
        enemy = EnemyGen(True, self.height, self.width, top, bottom, self.levelGrid)
        refresh_start = False
        refresh_count = 0
        calc_start = False
        calc_count = 0
        new_level = 0
        player_height = 11
        player_depth = 5
        self.place_hero()

        while running:
            timer = int(round(time.clock() * 1000))

            # temporary single player control code
            c = self.stdscr.getch()
            if c == curses.KEY_UP:
                if self.levelGrid[self.heroRow - 1][self.heroCol] == ' ':
                    self.move_hero_row(-1)
                else: #handle collision
                    return
                    
            elif c == curses.KEY_DOWN:
                if self.levelGrid[self.heroRow + 1][self.heroCol] == ' ':
                    self.move_hero_row(1)
                else: #handle collision
                    return

            if calc_start is False:
                calc_count = timer
                calc_start = True
            elif calc_start and (timer - calc_count) > 100:
                counter += 1
                new_level += 1
                if counter == 100:
                    if bottom - top > 7:
                        top += 1
                        bottom -= 1
                    counter = 0

                elif counter == 99:
                    old_color = color
                    while old_color == color:
                        color = color_setting.get_colors()
                    new_level = 0

                self.level_update(top, bottom)
                self.level_obstacles(top, bottom)
                #self.hero()
                enemy.enemy_spawn()
                enemy.enemy_hunt(player_height, player_depth)
                calc_start = False
                #self.hero()

            if refresh_start is False:
                refresh_count = timer
                refresh_start = True
                self.level_draw(color, old_color, new_level)
            elif refresh_start and (timer - refresh_count) > 16:
                refresh_start = False
                self.stdscr.refresh()

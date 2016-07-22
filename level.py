import time
import curses
from colorset import ColorSet
from random import randint
from enemies import EnemyGen


class LevelGen:
    def __init__(self, level_grid, height, width, stdscr):
        self.height = height
        self.width = width
        self.level_grid = [[0 for i in range(width)] for j in range(height)]
        self.stdscr = stdscr
        self.heroRow = width / 6
        self.heroCol = height / 2
        self.level_count = 0

    def level_build(self):
        for i in range(self.height):
            for j in range(self.width):
                self.level_grid[i][j] = ' '

        for i in range(self.height):
            for j in range(self.width):
                if j > 0:
                    if i <= 0 or i >= self.height - 1:
                        self.level_grid[i][j] = '#'

    def level_update(self, top, bottom, player_height, player_depth):
        self.level_obstacles(top, bottom)
        enemy = EnemyGen(self.height, self.width, top, bottom, self.level_grid, player_height, player_depth, self.level_count)
        enemy.enemy_spawn()

        for i in range(self.height):
                if i <= top or i >= bottom:
                    self.level_grid[i][self.width - 1] = '#'

        for i in range(self.height):
            for j in range(self.width):
                if self.level_grid[i][j] == '&' and j != 0:
                    enemy.enemy_hunt(i, j)

        for i in range(self.height):
            for j in range(self.width):
                if self.level_grid[i][j] != ' ' and self.level_grid[i][j] != '@' and j != 0:
                    temp = self.level_grid[i][j]
                    self.level_grid[i][j] = ' '
                    self.level_grid[i][j - 1] = temp

                if 0 <= i <= self.height and self.level_grid[i][0] != ' ' and self.level_grid[i][0] != '@':
                    self.level_grid[i][0] = ' '

    def level_obstacles(self, top, bottom):

        for i in range(self.height):
            if top < i < bottom:
                rand = randint(0, 90)
                if rand == 1:
                    rand2 = randint(0, 4)
                    if rand2 <= (bottom - i):
                        for k in range(rand2):
                            self.level_grid[i + k][self.width - 1] = '#'

    def place_hero(self):
        self.level_grid[self.heroRow][self.heroCol] = '@'
        '''
        for i in range(self.height):
            for j in range(self.width):
                if i == 10 and j == 3:
                    self.level_grid[i][j] = '@'
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
                    if self.level_grid[i][j] == '#':
                        self.stdscr.addstr(i, j, self.level_grid[i][j] + "\n", curses.color_pair(1))
                    elif self.level_grid[i][j] == '&':
                        self.stdscr.addstr(i, j, self.level_grid[i][j] + "\n", curses.color_pair(2))
                    else:
                        self.stdscr.addstr(i, j, self.level_grid[i][j] + "\n")
                    count = 0
                elif count >= self.width - new_level:
                    if self.level_grid[i][j] == '#':
                        self.stdscr.addstr(i, j, self.level_grid[i][j], curses.color_pair(1))
                    elif self.level_grid[i][j] == '&':
                        self.stdscr.addstr(i, j, self.level_grid[i][j], curses.color_pair(2))
                    else:
                        self.stdscr.addstr(i, j, self.level_grid[i][j])
                else:
                    if self.level_grid[i][j] == '#':
                        self.stdscr.addstr(i, j, self.level_grid[i][j], curses.color_pair(3))
                    elif self.level_grid[i][j] == '&':
                        self.stdscr.addstr(i, j, self.level_grid[i][j], curses.color_pair(4))
                    else:
                        self.stdscr.addstr(i, j, self.level_grid[i][j])
    
    def move_hero_row(self, moveBy):
        self.level_grid[self.heroRow][self.heroCol] = ' '
        self.heroRow += moveBy
        self.level_grid[self.heroRow][self.heroCol] = '@'

    def level_run(self, running):
        self.level_count = 0
        color_setting = ColorSet()
        color = color_setting.get_colors()
        old_color = color
        counter = 0
        top = 0
        bottom = self.height - 1
        refresh_start = False
        refresh_count = 0
        calc_start = False
        calc_count = 0
        new_level = 0
        level_length = 100
        self.place_hero()

        while running:
            timer = int(round(time.clock() * 1000))

            # temporary single player control code
            c = self.stdscr.getch()
            if c == curses.KEY_UP:
                if self.level_grid[self.heroRow - 1][self.heroCol] == ' ':
                    self.move_hero_row(-1)
                else:  # handle collision
                    return
                    
            elif c == curses.KEY_DOWN:
                if self.level_grid[self.heroRow + 1][self.heroCol] == ' ':
                    self.move_hero_row(1)
                else:  # handle collision
                    return
            player_height = self.heroRow
            player_depth = self.heroCol

            if calc_start is False:
                calc_count = timer
                calc_start = True
            elif calc_start and (timer - calc_count) > 100:
                counter += 1
                new_level += 1
                if counter == level_length:
                    if bottom - top > 7:
                        top += 1
                        bottom -= 1
                    counter = 0
                    self.level_count += 1

                elif counter == level_length - 1:
                    old_color = color
                    while old_color == color:
                        color = color_setting.get_colors()
                    new_level = 0

                self.level_update(top, bottom, player_height, player_depth)

                # check for collisions after level update
                if self.level_grid[self.heroRow][self.heroCol] != '@':
                    return

                calc_start = False

            if refresh_start is False:
                refresh_count = timer
                refresh_start = True
                self.level_draw(color, old_color, new_level)
            elif refresh_start and (timer - refresh_count) > 16:
                refresh_start = False
                self.stdscr.refresh()

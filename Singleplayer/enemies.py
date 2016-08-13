# Authors                  Connor Pacala(Network Developer),
#                          Joseph Vidal(Engine Developer),
#                          Paul Zotz(Input and Tools Developer)
# Date Created:            7/08/2016
# Date Last Modified:      7/22/2016
# File Name:               enemies.py
#
# Overview:                This is the toolset that creates and maintains the games
#                          enemies and controls the enemy interactions with the player

from random import randint


class EnemyGen:
    # initialize this enemy
    def __init__(self, height, width, top, bottom, level_grid, player_height, player_depth, level_count):
        self.height = height
        self.width = width
        self.top = top
        self.bottom = bottom
        self.level_grid = level_grid
        self.player_height = player_height
        self.player_depth = player_depth
        self.level_count = level_count

    # generate an enemy at random at the right side of the screen with increasing frequency as
    # the game progresses
    def enemy_spawn(self):
        # Adjust rate of enemy creation dependant on level players have achieved
        spread = 500
        level_spread = spread - (100 * self.level_count)
        if level_spread <= 100:
            level_spread = 100

        # generate the enemy base on "level_spread"
        for i in range(self.height):
            if self.top < i < self.bottom and self.level_grid[i][self.width - 1] != '#':
                rand = randint(0, level_spread)
                if rand == 1:
                    self.level_grid[i][self.width - 1] = '&'

    # The enemy becomes aware of the player when they enter "hunt" distance and then will
    # attempt to reach the player at random intervals
    def enemy_hunt(self, yloc, xloc):
        hunt = 50
        temp_y = yloc
        temp_x = xloc

        # decide enemy movement direct based on current location of "hero"
        if (xloc - self.player_depth) < hunt:
            rand = randint(0, 3)
            if rand == 1:
                if self.player_height < yloc and self.level_grid[yloc - 1][xloc] != '#' and self.level_grid[yloc- 1][xloc] != '&':
                    temp_y = yloc - 1
                if self.player_height > yloc and self.level_grid[yloc + 1][xloc] != '#' and self.level_grid[yloc + 1][xloc] != '&':
                    temp_y = yloc + 1
                if self.player_height < xloc and self.level_grid[yloc][xloc - 1] != '#' and self.level_grid[yloc][xloc - 1] != '&':
                    temp_x = xloc - 1

        # Move enemy to decided upon location
        if self.level_grid[yloc][xloc] != '#':
            temp = self.level_grid[yloc][xloc]
            self.level_grid[yloc][xloc] = ' '
            self.level_grid[temp_y][temp_x] = temp

    def enemy_death(self, yloc, xloc):
        if (self.level_grid[yloc][xloc] == '&' and (xloc < self.player_depth - 2 or self.level_grid[yloc - 1][xloc] == ',')) or self.level_grid[yloc][xloc] == '}':
            self.level_grid[yloc][xloc] = '+'
            self.level_grid[yloc][xloc + 2] = ' '
            self.level_grid[yloc][xloc - 2] = ' '
            self.level_grid[yloc][xloc + 1] = ' '
            self.level_grid[yloc][xloc - 1] = ' '

            if yloc < self.bottom and self.level_grid[yloc + 1][xloc] != '#':
                self.level_grid[yloc + 1][xloc] = ' '
                self.level_grid[yloc + 1][xloc + 1] = ' '
                self.level_grid[yloc + 1][xloc - 1] = ' '

            if yloc + 2 < self.bottom and self.level_grid[yloc + 2][xloc] != '#':
                self.level_grid[yloc + 2][xloc] = ' '

            if yloc - 1 > self.top and self.level_grid[yloc - 1][xloc] != '#':
                self.level_grid[yloc - 1][xloc] = ' '
                self.level_grid[yloc - 1][xloc + 1] = ' '
                self.level_grid[yloc - 1][xloc - 1] = ' '

            if yloc - 2 > self.top and self.level_grid[yloc - 2][xloc] != '#':
                self.level_grid[yloc - 2][xloc] = ' '

        elif self.level_grid[yloc][xloc] == '+' and self.level_grid[yloc][xloc - 1] != '$':
            self.level_grid[yloc][xloc + 1] = '$'
            self.level_grid[yloc][xloc - 1] = '$'

            if yloc + 1 < self.bottom and self.level_grid[yloc + 1][xloc] != '#':
                self.level_grid[yloc + 1][xloc] = '$'
                self.level_grid[yloc + 1][xloc + 1] = '%'
                self.level_grid[yloc + 1][xloc - 1] = '%'

            if yloc - 1 > self.top and self.level_grid[yloc - 1][xloc] != '#':
                self.level_grid[yloc - 1][xloc] = '$'
                self.level_grid[yloc - 1][xloc + 1] = '%'
                self.level_grid[yloc - 1][xloc - 1] = '%'

        elif self.level_grid[yloc][xloc] == '+' and self.level_grid[yloc][xloc - 1] == '$' and self.level_grid[yloc][xloc - 2] != '*':
            self.level_grid[yloc][xloc + 2] = '*'
            self.level_grid[yloc][xloc - 2] = '*'

            if yloc + 2 < self.bottom and self.level_grid[yloc + 2][xloc] != '#':
                self.level_grid[yloc + 2][xloc] = '*'

            if yloc - 2 > self.top and self.level_grid[yloc - 2][xloc] != '#':
                self.level_grid[yloc - 2][xloc] = '*'

        elif self.level_grid[yloc][xloc] == '+' and self.level_grid[yloc][xloc - 1] == '$' and self.level_grid[yloc][xloc - 2] == '*':
            self.level_grid[yloc][xloc] = '!'
        elif self.level_grid[yloc][xloc] == '!' and self.level_grid[yloc][xloc - 2] == '*':
            self.level_grid[yloc][xloc + 1] = '~'
            self.level_grid[yloc][xloc - 1] = '~'

            if yloc + 1 < self.bottom and self.level_grid[yloc + 1][xloc] != '#':
                self.level_grid[yloc + 1][xloc] = '~'
                self.level_grid[yloc + 1][xloc + 1] = '~'
                self.level_grid[yloc + 1][xloc - 1] = '~'

            if yloc - 1 > self.top and self.level_grid[yloc - 1][xloc] != '#':
                self.level_grid[yloc - 1][xloc] = '~'
                self.level_grid[yloc - 1][xloc + 1] = '~'
                self.level_grid[yloc - 1][xloc - 1] = '~'

        if self.level_grid[yloc][xloc] == '!' and self.level_grid[yloc][xloc - 1] == '~' and self.level_grid[yloc][xloc - 2] != '`':
            self.level_grid[yloc][xloc + 2] = '`'
            self.level_grid[yloc][xloc - 2] = '`'

            if yloc + 2 < self.bottom and self.level_grid[yloc + 2][xloc] != '#':
             self.level_grid[yloc + 2][xloc] = '`'

            if yloc - 2 > self.top and self.level_grid[yloc - 2][xloc] != '#':
                self.level_grid[yloc - 2][xloc] = '`'

        if self.level_grid[yloc][xloc] == '!' and self.level_grid[yloc][xloc - 1] == '~' and self.level_grid[yloc][xloc - 2] == '`':
            self.level_grid[yloc][xloc] = ' '
            self.level_grid[yloc][xloc + 2] = ' '
            self.level_grid[yloc][xloc - 2] = ' '
            self.level_grid[yloc][xloc + 1] = ' '
            self.level_grid[yloc][xloc - 1] = ' '

            if yloc + 1 < self.bottom and self.level_grid[yloc + 1][xloc] != '#':
                self.level_grid[yloc + 1][xloc] = ' '
                self.level_grid[yloc + 1][xloc + 1] = ' '
                self.level_grid[yloc + 1][xloc - 1] = ' '

            if yloc + 2 < self.bottom and self.level_grid[yloc + 2][xloc] != '#':
                self.level_grid[yloc + 2][xloc] = ' '

            if yloc - 1 > self.top and self.level_grid[yloc - 1][xloc] != '#':
                self.level_grid[yloc - 1][xloc] = ' '
                self.level_grid[yloc - 1][xloc + 1] = ' '
                self.level_grid[yloc - 1][xloc - 1] = ' '

            if yloc - 2 > self.top and self.level_grid[yloc - 2][xloc] != '#':
                self.level_grid[yloc - 2][xloc] = ' '

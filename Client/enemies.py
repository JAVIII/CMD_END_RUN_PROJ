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
    def __init__(self, ID, height, width, top, bottom, level_grid, player_height, player_depth, level_count):
        self.ID = ID
        self.height = height
        self.width = width
        self.top = top
        self.bottom = bottom
        self.level_grid = level_grid
        self.player_height = player_height
        self.player_depth = player_depth
        self.level_count = level_count
        self.death_step = 0

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
                    self.width -= 1
                    self.level_grid[i][self.width] = '&'
                    self.height = i
                    return True

        return False

    # The enemy becomes aware of the player when they enter "hunt" distance and then will
    # attempt to reach the player at random intervals
    def enemy_hunt(self, yloc, xloc):
        hunt = 50
        temp_y = self.height
        temp_x = self.width

        # decide enemy movement direct based on current location of "hero"
        if (temp_x - self.player_depth) < hunt:
            rand = randint(0, 3)
            if rand == 1:
#                if self.player_height < temp_y and self.level_grid[temp_y - 1][temp_x] != '#' and self.level_grid[temp_y- 1][temp_x] != '&':
                if yloc < temp_y:
                    temp_y -= 1
 #               if self.player_height > temp_y and self.level_grid[temp_y + 1][temp_x] != '#' and self.level_grid[temp_y + 1][temp_x] != '&':
                if yloc > temp_y:
                    temp_y += 1
 #               if self.player_height < temp_x and self.level_grid[temp_y][temp_x - 1] != '#' and self.level_grid[temp_y][temp_x - 1] != '&':
                if xloc < temp_x:
                    temp_x -= 1

        # Move enemy to decided upon location
#        temp = self.level_grid[yloc][xloc]
#        if e.width >= 0 and e.width <= self.width and e.height > 0 and e.height < self.height:
#            self.level_grid[e.height][e.width] = ' '
#            e.width = temp_x
#            e.height = temp_y
#        self.level_grid[temp_y][temp_x] = temp
        return temp_x, temp_y

    def enemy_death(self, level, top, bottom):
        if self.death_step == 0:
            level.level_grid[self.height][self.width] = '+'
            self.death_step += 1
            return 1
        elif self.death_step == 1:
            level.level_grid[self.height][self.width + 1] = '$'
            level.level_grid[self.height][self.width - 1] = '$'
            if self.height + 1 <= bottom:
                level.level_grid[self.height + 1][self.width] = '$'
                level.level_grid[self.height + 1][self.width + 1] = '%'
                level.level_grid[self.height + 1][self.width - 1] = '%'
            if self.height - 1 >= top:
                level.level_grid[self.height - 1][self.width] = '$'
                level.level_grid[self.height - 1][self.width + 1] = '%'
                level.level_grid[self.height - 1][self.width - 1] = '%'
            self.death_step += 1
            return 0
        elif self.death_step == 2:
            if self.height + 2 <= bottom:
                level.level_grid[self.height + 2][self.width] = '*'
            if self.height - 2 >= top:
                level.level_grid[self.height - 2][self.width] = '*'
                level.level_grid[self.height][self.width + 2] = '*'
                level.level_grid[self.height][self.width - 2] = '*'
            self.death_step += 1
            return 0
        elif self.death_step == 3:
            level.level_grid[self.height][self.width] = '!'
            self.death_step += 1
            return 0
        elif self.death_step == 4:
            level.level_grid[self.height][self.width + 1] = '~'
            level.level_grid[self.height][self.width - 1] = '~'
            if self.height + 1 <= bottom:
                level.level_grid[self.height + 1][self.width] = '~'
                level.level_grid[self.height + 1][self.width + 1] = '~'
                level.level_grid[self.height + 1][self.width - 1] = '~'
            if self.height - 1 >= top:
                level.level_grid[self.height - 1][self.width] = '~'
                level.level_grid[self.height - 1][self.width + 1] = '~'
                level.level_grid[self.height - 1][self.width - 1] = '~'
            self.death_step += 1
            return 0
        elif self.death_step == 5:
            if self.height + 2 <= bottom:
                level.level_grid[self.height + 2][self.width] = '`'
            if self.height - 2 >= top:
                level.level_grid[self.height - 2][self.width] = '`'
            level.level_grid[self.height][self.width + 2] = '`'
            level.level_grid[self.height][self.width - 2] = '`'
            self.death_step += 1
            return 0
        elif self.death_step == 6:
            if self.height + 2 <= bottom:
                level.level_grid[self.height + 2][self.width] = ' '
            if self.height - 2 >= top:
                level.level_grid[self.height - 2][self.width] = ' '
            if self.height + 1 <= bottom:
                level.level_grid[self.height + 1][self.width] = ' '
                level.level_grid[self.height + 1][self.width + 1] = ' '
                level.level_grid[self.height + 1][self.width - 1] = ' '
            if self.height - 1 >= top:
                level.level_grid[self.height - 1][self.width] = ' '
                level.level_grid[self.height - 1][self.width + 1] = ' '
                level.level_grid[self.height - 1][self.width - 1] = ' '
            level.level_grid[self.height][self.width + 2] = ' '
            level.level_grid[self.height][self.width - 2] = ' '
            level.level_grid[self.height][self.width + 1] = ' '
            level.level_grid[self.height][self.width - 1] = ' '
            self.death_step = -1
            return -1
        return 0

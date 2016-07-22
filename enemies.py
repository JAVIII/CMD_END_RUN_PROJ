from random import randint


class EnemyGen:
    def __init__(self, height, width, top, bottom, level_grid, player_height, player_depth, level_count):
        self.height = height
        self.width = width
        self.top = top
        self.bottom = bottom
        self.level_grid = level_grid
        self.player_height = player_height
        self.player_depth = player_depth
        self.level_count = level_count

    def enemy_spawn(self):
        spread = 500
        level_spread = spread - (100 * self.level_count)
        if level_spread <= 100:
            level_spread = 100

        for i in range(self.height):
            if self.top < i < self.bottom and self.level_grid[i][self.width - 1] != '#':
                rand = randint(0, level_spread)
                if rand == 1:
                    self.level_grid[i][self.width - 1] = '&'

    def enemy_hunt(self, yloc, xloc):
        hunt = 50
        temp_y = yloc
        temp_x = xloc

        if (xloc - self.player_depth) < hunt:
            rand = randint(0, 5)
            if rand == 1:
                if self.player_height < yloc and self.level_grid[yloc - 1][xloc] != '#' and self.level_grid[yloc- 1][xloc] != '&':
                    temp_y = yloc - 1
                if self.player_height > yloc and self.level_grid[yloc + 1][xloc] != '#' and self.level_grid[yloc + 1][xloc] != '&':
                    temp_y = yloc + 1
                if self.player_height < xloc and self.level_grid[yloc][xloc - 1] != '#' and self.level_grid[yloc][xloc - 1] != '&':
                    temp_x = xloc - 1

        temp = self.level_grid[yloc][xloc]
        self.level_grid[yloc][xloc] = ' '
        self.level_grid[temp_y][temp_x] = temp

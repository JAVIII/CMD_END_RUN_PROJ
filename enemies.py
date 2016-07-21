from random import randint


class EnemyGen:
    def __init__(self, living, height, width, top, bottom, levelGrid):
        self.living = living
        self.height = height
        self.width = width
        self.top = top
        self.bottom = bottom
        self.levelGrid = levelGrid

    def enemy_spawn(self):
        for i in range(self.height):
            for j in range(self.width):
                if (i > self.top and i < self.bottom) and j == self.width - 1 and self.levelGrid[i][j] != '#':
                    rand = randint(0, 90)
                    if rand == 1:
                        self.levelGrid[i][j] = '&'

                # to remove enemies as they reach left side of screen
                if (i > self.top or i < self.bottom) and j == 0 and self.levelGrid[i][j] == '&':
                    self.levelGrid[i][j] = ' '

    def enemy_hunt(self, player_height, player_depth):
        up_blocked = False
        down_blocked = False
        hunt = 50

        for i in range(self.height):
            for j in range(self.width):
                if self.levelGrid[i][j] == '&' and j > 0 and (j - player_depth) < hunt:
                    if i > 0 and (self.levelGrid[i - 1][j] == '#' or self.levelGrid[i - 1][j] == '#'):
                        up_blocked = True
                    if i < self.height - 1 and (self.levelGrid[i + 1][j] == '#' or self.levelGrid[i + 1][j] == '&'):
                        down_blocked = True

                    if player_height < i or (up_blocked == False and down_blocked == True):
                        temp = self.levelGrid[i][j]
                        self.levelGrid[i][j] = ' '
                        self.levelGrid[i - 1][j] = temp
                    if player_height > i or (up_blocked == True and down_blocked == False):
                        temp = self.levelGrid[i][j]
                        self.levelGrid[i][j] = ' '
                        self.levelGrid[i + 1][j] = temp

                    if player_height < j and self.levelGrid[i][j - 1] != '#' and self.levelGrid[i][j - 1] != '&':
                        temp = self.levelGrid[i][j]
                        self.levelGrid[i][j] = ' '
                        self.levelGrid[i][j - 1] = temp
                        up_blocked = False
                        down_blocked = False

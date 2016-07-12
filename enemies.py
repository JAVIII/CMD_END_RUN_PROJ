from random import randint

class enemyGen:
    def __init__(self, living, height, width, top, bottom, levelGrid):
        self.living = living
        self.height = height
        self.width = width
        self.top = top
        self.bottom = bottom
        self.levelGrid = levelGrid

    def enemySpawn(self):
        for i in range(self.height):
            for j in range(self.width):
                if (i > self.top or i < self.bottom) and j == self.width - 1 and self.levelGrid[i][j] != '#':
                    rand = randint(0, 90)
                    if rand == 1:
                        self.levelGrid[i][j] = '&'

                if (i > self.top or i < self.bottom) and j == 0 and self.levelGrid[i][j] == '&':
                    self.levelGrid[i][j] = ' '

    def enemyHunt(self):
        playerHeight = 10
        playerDepth = 3
        upBLocked = False
        downBlocked = False

        for i in range(self.height):
            for j in range(self.width):
                if self.levelGrid[i][j] == '&' and j > 0:
                    if i > 0 and (self.levelGrid[i - 1][j] == '#' or self.levelGrid[i - 1][j] == '#'):
                        upBLocked = True
                    if i < self.height - 1 and (self.levelGrid[i + 1][j] == '#' or self.levelGrid[i + 1][j] == '&'):
                        downBlocked = True

                    if playerHeight < i or (upBLocked == False and downBlocked == True):
                        temp = self.levelGrid[i][j]
                        self.levelGrid[i][j] = ' '
                        self.levelGrid[i - 1][j] = temp
                    if playerHeight > i or (upBLocked == True and downBlocked == False):
                        temp = self.levelGrid[i][j]
                        self.levelGrid[i][j] = ' '
                        self.levelGrid[i + 1][j] = temp

                    if playerDepth < j and self.levelGrid[i][j - 1] != '#' and self.levelGrid[i][j - 1] != '&':
                        temp = self.levelGrid[i][j]
                        self.levelGrid[i][j] = ' '
                        self.levelGrid[i][j - 1] = temp
                        upBLocked = False
                        downBlocked = False
import sys
import time
import os
import curses
from random import randint
from enemies import enemyGen



class levelGen():

    def __init__(self, levelGrid, height, width):
        self.height = height
        self.width = width
        self.levelGrid = [[0 for i in range(width)] for j in range(height)]

    def levelBuild(self):
        for i in range(self.height):
            for j in range(self.width):
                self.levelGrid[i][j] = ' '

        for i in range(self.height):
            for j in range(self.width):
                if (i <= 0 or i >= self.height - 1):
                    self.levelGrid[i][j] = '#'

    def levelUpdate(self, top, bottom):

        for i in range(self.height):
            for j in range(self.width):
                if (i <= top or i >= bottom) and j == self.width - 1:
                    self.levelGrid[i][j] = '#'

        for i in range(self.height):
            for j in range(self.width):
                if self.levelGrid[i][j] != ' ' and j != 0:
                    temp = self.levelGrid[i][j]
                    self.levelGrid[i][j] = ' '
                    self.levelGrid[i][j - 1] = temp

    def levelObstacles(self, top, bottom):
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

    def levelDraw(self):
        count = 0
        gridStr = ""

        for i in range(self.height):
            for j in range(self.width):
                count += 1
                if count == self.width:
                    gridStr += self.levelGrid[i][j] + "\n"
                    count = 0
                else:
                    gridStr += self.levelGrid[i][j]

        return gridStr

    def levelRun(self, running):
        counter = 0
        top = 0
        bottom = self.height - 1
        Enemy = enemyGen(True, self.height, self.width, top, bottom, self.levelGrid)
        refreshStart = False
        refreshCount = 0
        calcStart = False
        calcCount = 0

        while(running):
            stdscr = curses.initscr()
            timer = int(round(time.clock() * 1000))

            if calcStart == False:
                calcCount = timer
                calcStart= True
            elif calcStart == True and (timer - calcCount) > 100:
                counter += 1
                if counter == 100:
                    top += 1
                    bottom -= 1
                    counter = 0
                self.levelUpdate(top, bottom)
                self.levelObstacles(top, bottom)
                #Enemy.enemySpawn()
                #Enemy.enemyHunt()
                calcStart = False

            if refreshStart == False:
                refreshCount = timer
                refreshStart = True
                gridStr = self.levelDraw()
                stdscr.addstr(0, 0, gridStr)
            elif refreshStart == True and (timer - refreshCount) > 16:
                refreshStart = False
                stdscr.refresh()






from level import levelGen

grid = []
height = 15
width = 71
running = True
gridMaker = levelGen(grid, height, width)

gridMaker.levelBuild()
gridMaker.levelRun(running)



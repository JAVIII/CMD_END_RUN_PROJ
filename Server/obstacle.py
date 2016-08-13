class Obstacle:
    def __init__(self, ID, height, width, level):
        self.ID = ID
        self.height = height
        self.width = width
        self.death_step = 0
        self.level = level
        
    def wall_break(self, yloc, xloc):
        if self.death_step == 0:
            self.level.level_grid[yloc][xloc + 1] = ','
            self.level.level_grid[yloc][xloc - 1] = ','
            self.level.level_grid[yloc][xloc] = ' '
            self.death_step += 1
            return 0
        elif self.death_step == 1:
            self.level.level_grid[yloc][xloc + 1] = ' '
            self.level.level_grid[yloc][xloc - 1] = ' '
            return 1
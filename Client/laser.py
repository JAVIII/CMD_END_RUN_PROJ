class laser:
    def __init__(self, id, row, col, barrier):
        self.ID = id
        self.row = row
        self.col = col
        self.barrier = barrier
    def advance(self):
        if self.col < self.barrier - 1:
            self.col = self.col + 1
            return True
        
        return False
    def getRow(self):
        return self.row
    def getCol(self):
        return self.col
    
    

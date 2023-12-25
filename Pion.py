from Jeton import Jeton
from Dame import Dame

class Pion(Jeton):
    def __init__(self, x, y, color) -> None:
        super().__init__(self, x, y, color, type = "pion", color = color)
    
    def to_queen(self, board):
        pass
        
    
    def see_available_takes(self, board):
        left = board.get_squares()[self.x - 1, self.y + 1]
        right = board.get_squares()[self.x + 1, self.y + 1]
        if not (left.occupied() or right.occupied()): return(None)
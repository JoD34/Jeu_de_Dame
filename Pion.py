from Jeton import Jeton

class Pion(Jeton):
    def __init__(self, x, y, color) -> None:
        super().__init__(x = x, y = y, color = color, type = "pion")
    
    def to_queen(self, board):
        pass
        
    
    def see_available_takes(self, board):
        left = board.get_squares()[self.x - 1, self.y + 1]
        right = board.get_squares()[self.x + 1, self.y + 1]
        if not (left.occupied() or right.occupied()): return(None)
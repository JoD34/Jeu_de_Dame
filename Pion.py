import Jeton

class Pion(Jeton):
    def __init__(self) -> None:
        Jeton.__init__(self, )
        
    
    def see_available_takes(self, board):
        left = board.get_squares()[self.x - 1, self.y + 1]
        right = board.get_squares()[self.x + 1, self.y + 1]
        if not (left.occupied() or right.occupied()): return(None)
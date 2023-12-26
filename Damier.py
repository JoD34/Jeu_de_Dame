from Case import Case

class Damier():
    def __init__(self) -> None:
        self.squares = self.create_board()
        
    def get_square(self, x, y):
        """Access a given square on the board.

        Args:
            x (int): position in x on the board.
            y (int): position in y on the board.

        Returns:
            Case: case on the board.
        """
        return self.squares[x][y]
    
    def create_square(self, x, y):
        """Create a square

        Args:
            x (int): position in x on the board.
            y (int): position in y on the board.
            color (str): set color of the square.
        """
        return Case(x=x, y=y)
        
    
    def create_board(self):
        """Create the entire board with the squares
        """
        SIDE = 10
        return [[self.create_square(x=i, y=j) for j in range(SIDE)] for i in range(SIDE)]
                
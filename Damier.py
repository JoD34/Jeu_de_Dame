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
    
    def get_diagonal_squares(self, x, y, team_color):
        """Get diagonal squares of a given square. 

        Args:
            x (int): row in the damier
            y (int): column in the damier
            team_color (str): color of team

        Returns:
            dict: squares retrieved
        """
        # Correction depending of color
        x  = x + 1 if team_color == 'black' else x - 1
        
        # Get squares that should be available
        left = self.get_square(x=x, y=(y - 1)) if ((y - 1  < 10) and (y - 1 >= 0)) else None
        right = self.get_square(x=x, y=(y + 1)) if ((y + 1  < 10) and (y + 1 >= 0)) else None
        
        return {'left' : left, 'right' : right}
    
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
    
                
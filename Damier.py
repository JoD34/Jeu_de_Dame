from Case import Case

class Damier():
    def __init__(self) -> None:
        self.squares = self.create_board()
        self.colors = {'pale' : "#eab676", 'fonce' : "#1e81b0"}
        
    def get_square(self, x, y):
        """Access a given square on the board.

        Args:
            x (int): position in x on the board.
            y (int): position in y on the board.

        Returns:
            Case: case on the board.
        """
        return self.squares[x, y]
    
    def get_colors(self):
        """Return the colors for the board

        Returns:
            dict: different colors of the board
        """
        return self.colors
    
    def create_square(self, x, y):
        """Create a square

        Args:
            x (int): position in x on the board.
            y (int): position in y on the board.
            color (str): set color of the square.
        """
        return Case(pos_x = x, 
                    pos_y = y, 
                    color = self.colors()["pale" if ((x + y) % 2 != 0) else "fonce"])
    
    def create_board(self):
        """Create the hole board with the squares
        """
        SIDE = 10
        self.square = [self.create_square(x = i, y = j) for j in range(SIDE) for i in range(SIDE)]
                
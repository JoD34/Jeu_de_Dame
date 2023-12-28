from Case import Case
from Equipe import Equipe
from Pion import Pion
import sys

class Damier():
    def __init__(self) -> None:
        self.squares = self.create_board()
        self.turn = ['white', 'red']
        self.teams = {"red": Equipe("red"), "black": Equipe("black")}
        
        # Set pions
        self.init_pions('red')
        self.init_pions('black')
        
    def get_square(self, x, y):
        """Access a given square on the board.

        Args:
            x (int): position in x on the board.
            y (int): position in y on the board.

        Returns:
            Case: case on the board.
        """
        return self.squares[int(str(x) + str(y))]
    
    def get_squares(self):
        """Get the list of squares present in the damier

        Returns:
            list: All Case objects making up the damier
        """
        return self.squares
    
    def get_diagonal_squares(self, x, y, team_color, square):
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
        return {'left' : self.__set_highlight_square(x=x, y=(y - 1), current=square),
                'right' : self.__set_highlight_square(x=x, y=(y + 1), current=square)}
    
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
        return [self.create_square(x=i, y=j) for i in range(SIDE) for j in range(SIDE)]
    
    def __check_if_friend(self, current, square):
        """Check if it is friend or foe

        Args:
            current (Case): Current Case. Origin of the event
            square (Case): diagonal Case. Checked if foe or not

        Returns:
            bool: True if friend. False if foe.
        """
        return current.get_jeton().get_color() == square.get_jeton().get_color()
        
    def __set_highlight_square(self, x, y, current):
        
        # Check if column index is out of bound
        if ((y >= 10) or (y < 0)): return None
        
        # Get square
        square = self.get_square(x=x, y=y) 
    
        # Return if square should be highlighted
        return None if (square.is_occupied() and self.__check_if_friend(current=current, square=square)) else square
    
    def init_pions(self, team_color):
        """Initiate pions, there position and there relation to a case

        Args:
            team_color (str): color corresponding to one of two teams
        """
        beg_x, end_x = (0, 4) if team_color == 'black' else (6, 10)
        
        for i in range(beg_x, end_x):
            for j in range(0, 10):
                
                # Only set Pions on dark squares
                if (i + j) % 2 == 0 : continue
                
                # Get corresponding square
                square = self.get_square(x=i, y=j)
                # Generate jeton
                pion = Pion(x=i, y=j, case=square, color=team_color)
                # Add pion to square
                square.set_jeton(pion)
                # Add new pion to team
                self.teams[team_color].add_jeton(pion)
                
    def get_turn(self):
        """Get which team color is it to play.

        Returns:
            str: color of the team.
        """
        return self.turn[0]
    
    def next_turn(self):
        """Switch turn.
        """
        self.turn = self.turn[-1:]
from Case import Case
from Equipe import Equipe
from Pion import Pion
import sys

class Damier():
    def __init__(self) -> None:
        self.squares = self.create_board()
        self.turn = ['red', 'black']
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
        self.turn = self.turn[::-1]
        
    def move_pieces(self, current_square, new_square):
        """_summary_

        Args:
            current_square (_type_): _description_
            new_square (_type_): _description_
        """
        # Remove jeton from current square
        jeton = current_square.get_jeton()
        current_square.remove_jeton()
    
        # Add jeton to new square
        new_square.set_jeton(jeton)
        jeton.set_case(new_square)
        
        # Switch turns
        self.next_turn()
    
    def take_pion(self, taker, taken, team_color):
        """Changes jetons position for a take movement

        Args:
            taker (Jeton): Jeton information for the jeton that is taking
            taken (Jeton): Jeton information for the jeton that is taken
            team_color (str): information about the movement of the current pion
        """
        # Get move modification to add to the current position of taker
        move_y = (taken.get_y() - taker.get_y()) * 2
        move_x = 2 if team_color == 'black' else -2
        
        # Remove taken jeton from case
        taken.get_case().remove_jeton()
        
        # Get infos to remove the pion from the stake
        team_color = taken.get_jeton().get_color()
        team = self.teams[team_color]
        team.remove[team.index(taken)]
        
        # Set new information to the taker pions
        taker.set_y(new_y = taker.get_y() + move_y)
        taker.set_x(new_x = taker.get_x() + move_x)
        
        # Check if game is over
        print(team.has_lost())
        
    def get_forced_moves(self, team_color):
        """Get square for takes

        Args:
            team_color (str): color of pion

        Returns:
            list: all square which can be taken
        """
        res = []
        moves = 1 if team_color == 'black' else -1
        
        # Parse all square on the board
        for square in self.board:
            
            # Interact with squares that contain pion of a given team only
            if square.get_jeton().get_color() != team_color: continue
            
            # set x on which to look upon
            x = square.get_x() + moves
            
            # Parse the two columns to looks
            for num in [1, -1]:
                case = self.__get_square_takes(x = x, y = square.get_y() + num, 
                                               next_x = moves, next_y = num, 
                                               current = square)
                if not case: 
                    for i in case: res.append(i)
                
        return res
            
    def __get_square_takes(self, x, y, current, next_x, next_y):
        """_summary_

        Args:
            x (int): position in x of taken square
            y (int): position in y of taken square
            current (Case): Square from which the move originates
            next_x (int): x changes in for the x value for the landing strip
            next_y (int): y changes in for the y value for the landing strip

        Returns:
            list: Case for valid moves
        """
        # Check if column index is out of bound
        if ((y + 1 >= 10) or (y - 1 < 0)): return []
        
        # Get squares
        square_to_take = self.get_square(x=x, y=y) 
        square_to_land = self.get_square(x = x + next_x, y = y + next_y)
    
        # Return if square should be highlighted
        valid = square_to_take if (square_to_take.is_occupied() and 
                                   not self.__check_if_friend(current=current, 
                                                              square=square_to_take)) else None
        # Return if take is valid and landing spot is open
        return [] if ((valid is None) or not square_to_land.is_occupied()) else [square_to_land, square_to_take]
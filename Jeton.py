
class Jeton:
    def __init__(self, x, y, type, case, color) -> None:
        self.type = type
        self.move = []
        self.x = x
        self.y = y
        self.case = case
        self.color = color
    
    def get_move(self):
        """Get the possible moves in x

        Returns:
            list: All possible moves in x
        """
        return self.move
    
    def get_type(self):
        """Get the piece type

        Returns:
            str: piece type between 'pion' and 'queen'
        """
        return self.type
    
    def get_x(self):
        """Get the position in x of the token

        Returns:
            int: x value of the position of the token
        """
        return self.x
    
    def get_y(self):
        """Get the position in y of the token

        Returns:
            int: y value of the position of the token
        """
        return self.y
    
    def get_case(self):
        """Get Case on witch the pion is standing

        Returns:
            Case: Case on witch the pion is standing
        """
        return self.case
    
    def get_color(self):
        """Get color associated to current Jeton.

        Returns:
            str: Color of the team in which the Jeton is.
        """
        return self.color
        
    def set_type(self, new_type):
        """Set type of piece

        Args:
            new_type (str): New type of piece
        """
        self.type = new_type
        
    def set_move(self, new_move):
        """Set possible moves in x

        Args:
            new_move (list): all possible moves in x
        """
        self.move = new_move
        
    def set_x(self, new_x):
        """Set new value of x

        Args:
            new_x (int): new value of the token on the x axis
        """
        self.x = new_x
        
    def set_y(self, new_y):
        """Set new value of y

        Args:
            new_y (int): new value of the token on the y axis
        """
        self.y = new_y 
    
    def set_case(self, new_case):
        """Set a new case on witch the pion is standing

        Args:
            new_case (Case): New case on witch the pion is standing
        """
        self.case = new_case
    
    def get_valid_moves(self):
        return([(i, i) for i in self.move])
    
    def see_available_takes(self, board):
        pass
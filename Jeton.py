
class Jeton:
    def __init__(self, type) -> None:
        self.type = type
        self.move_x = None
        self.move_y = None
        self.color = None
    
    def get_move_x(self):
        """Get the possible moves in x

        Returns:
            list: All possible moves in x
        """
        return self.move_x
    
    def get_move_y(self):
        """Get the possible moves in y

        Returns:
            list: All possible moves in y
        """
        return self.move_y
    
    def get_color(self):
        """Get color of the pieces

        Returns:
            str: color code for the piece
        """
        return self.color
    
    def get_type(self):
        """Get the piece type

        Returns:
            str: piece type between 'pion' and 'queen'
        """
        return self.type
    
    def set_type(self, new_type):
        """Set type of piece

        Args:
            new_type (str): New type of piece
        """
        self.type = new_type
        
    def set_move_x(self, new_move):
        """Set possible moves in x

        Args:
            new_move (list): all possible moves in x
        """
        self.move_x = new_move
        
    def set_move_y(self, new_move):
        """Set possible moves in y

        Args:
            new_move (list): all possible moves in y
        """
        self.move_y = new_move
    
    def set_color(self, color):
        """Set color of piece

        Args:
            color (str): color code of piece
        """
        self.color = color
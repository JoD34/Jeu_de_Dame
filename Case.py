
class Case:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.jeton = None
    
    def get_x(self):
        """Get position of x value.

        Returns:
            int: position (square) in x.
        """
        return self.x
    
    def get_y(self):
        """Get position of y value.

        Returns:
            int: position (square) in y value.
        """
        return self.y
    
    def get_occupancy(self):
        """Get occupancy statue of the square.

        Returns:
            bool: True if occupied; False if not.
        """
        return self.jeton is None
    
    def set_x(self, new_x):
        """Set new position in x.

        Args:
            new_pos_x (int): new position in x value.
        """
        self.x = new_x
        
    def set_y(self, new_y):
        """Set new position in y.

        Args:
            new_y (int): new position in x value.
        """
        self.y = new_y
        
    def set_jeton(self, jeton):
        """Set a jeton on the square

        Args:
            jeton (Jeton): Jeton place on the Case. Can be an object of type Pion or Dame
        """
        self.jeton = jeton
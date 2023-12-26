
class Case:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.color = None
        self.occupied = False
    
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
    
    def get_color(self):
        """Get color of pion placed on square

        Returns:
            str: team color of the pion placed on the square.
                Return None if no pion is places on the square  
        """
        return self.color
    
    def get_occupancy(self):
        """Get occupancy statue of the square.

        Returns:
            bool: True if occupied; False if not.
        """
        return self.occupied
    
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
        
    def set_color(self, new_color):
        """Set a new color for the team occupying a square

        Args:
            new_color (str): team color occupying new square
        """
        self.color = new_color
        
    def switch_occupancy(self):
        """Switch status of occupancy.
        """
        self.occupied = not self.get_occupancy()

class Case:
    def __init__(self) -> None:
        pos_x = None
        pos_y = None
        color = None
        occupied = False
    
    def get_pos_x(self):
        """Get position of x value.

        Returns:
            int: position (square) in x.
        """
        return self.get_pos_x
    
    def get_pos_y(self):
        """Get position of y value.

        Returns:
            int: position (square) in y value.
        """
        return self.get_pos_y
    
    def get_color(self):
        """Get color of square to be shown.

        Returns:
            str: color of square.
        """
        return self.get_color
    
    def get_occupancy(self):
        """Get occupancy statue of the square.

        Returns:
            bool: True if occupied; False if not.
        """
        return self.occupied
    
    def set_pos_x(self, new_pos_x):
        """Set new position in x.

        Args:
            new_pos_x (int): new position in x value.
        """
        self.get_pos_x = new_pos_x
        
    def set_pos_y(self, new_pos_y):
        """Set new position in y.

        Args:
            new_pos_y (int): new position in x value.
        """
        self.get_pos_y = new_pos_y
        
    def set_color(self, new_color):
        """Set new color of square.

        Args:
            new_color (str): code of new color.
        """
        self.color = new_color
        
    def set_occupancy(self):
        """Switch status of occupancy.
        """
        self.occupied = not self.get_occupancy()
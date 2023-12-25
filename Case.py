
class Case:
    def __init__(self, x, y, color) -> None:
        self.x = x
        self.y = y
        self.color = color
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
        """Get color of square to be shown.

        Returns:
            str: color of square.
        """
        return self.color
    
    def get_occupancy(self):
        """Get occupancy statue of the square.

        Returns:
            bool: True if occupied; False if not.
        """
        return self.occupied
    
    def set_pos_x(self, new_x):
        """Set new position in x.

        Args:
            new_pos_x (int): new position in x value.
        """
        self.x = new_x
        
    def set_pos_y(self, new_y):
        """Set new position in y.

        Args:
            new_y (int): new position in x value.
        """
        self.y = new_y
        
    def set_color(self, new_color):
        """Set new color of square.

        Args:
            new_color (str): code of new color.
        """
        self.color = new_color
        
    def switch_occupancy(self):
        """Switch status of occupancy.
        """
        self.occupied = not self.get_occupancy()
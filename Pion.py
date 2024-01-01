from Jeton import Jeton


class Pion(Jeton):
    def __init__(self, x, y, case, color) -> None:
        super().__init__(x=x, y=y, type="pion", case=case, color=color)
        self.direction = 'up' if color == 'red' else 'down'
        self.move = [-1] if color == 'red' else [1]

    def get_direction(self):
        """
        Get the direction of the pion object
        :return: the direction of the pion object
        """
        return self.direction

    def get_move(self):
        """
        Get the move of the pion object
        :return: moves of the pion object
        """
        return self.move
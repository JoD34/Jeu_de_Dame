from Jeton import Jeton


class Pion(Jeton):
    def __init__(self, x, y, case, color) -> None:
        super().__init__(x=x, y=y, type="pion", case=case, color=color)
        self.direction = 'up' if color == 'red' else 'down'

    def get_direction(self):
        """
        Get the direction of the pion object
        :return: the direction of the pion object
        """
        return self.direction
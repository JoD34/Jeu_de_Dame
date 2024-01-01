from Jeton import Jeton


class Dame(Jeton):
    def __init__(self, x, y, case, color) -> None:
        super().__init__(x=x, y=y, type="Dame", case=case, color=color)
        self.move = [-10, 10]

    def get_move(self):
        """
        Returns the possible move of the dame object
        :return: possible moves of the dame object
        """
        return self.move
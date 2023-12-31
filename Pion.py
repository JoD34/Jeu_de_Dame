from Jeton import Jeton


class Pion(Jeton):
    def __init__(self, x, y, case, color) -> None:
        super().__init__(x=x, y=y, type="pion", case=case, color=color)

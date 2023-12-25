import Jeton

class Dame(Jeton):
    def __init__(self, x, y, color) -> None:
        super().__init__(x = x, y = y, type = "Dame", color = color)
        self.move:[0, 10]
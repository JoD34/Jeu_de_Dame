import Pion

class Equipe():
    def __init__(self, color) -> None:
        self.pion = self.make_team()
        self.image = p
        self.per_x = 5
        self.per_y = 4
        self.color = None
    
    def make_team(self):
        return [Pion(x = i,y = j, color = self.color) for j in self.per_x for i in self.per_y]
    
    def get_pion(self):
        return self.pion
    
    def has_lost(self):
        return len(self.pion) == 0
    
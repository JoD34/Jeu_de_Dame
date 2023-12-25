import Pion

class Equipe():
    def __init__(self, color) -> None:
        self.pion = self.make_team()
        self.image = ""
        self.color = color
    
    def make_team(self):
        """Generate the full team with accurate coordonates

        Returns:
            list: Pions of one team
        """
        # Set variables
        INIT_X, INIT_Y = 5, 4
        END_OF_BOARD = 10
        
        # Changes of coordonates for generating black teams
        if (self.color == "Black"):
            return [Pion(x = i, y = (END_OF_BOARD - j), color = self.color) 
                    for j in range(INIT_X) for i in range(INIT_Y)]

        # Generate White teams
        return [Pion(x = i,y = j, color = self.color) for j in range(INIT_X) for i in range(INIT_Y)]
    
    def get_pion(self):
        return self.pion
    
    def has_lost(self):
        return len(self.pion) == 0
    
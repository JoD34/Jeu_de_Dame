from Pion import Pion
import matplotlib.image as mpimg

class Equipe():
    def __init__(self, color) -> None:
        self.color = color
        self.color_code = {'red' : "#000000", 'white': "#FFFFFF"}
        self.pion = self.make_team()
        self.images = self.get_images()
    
    def make_team(self):
        """Generate the full team with accurate coordonates

        Returns:
            list: Pions of one team
        """
        # Set variables
        INIT_X, INIT_Y = 5, 4
        END_OF_BOARD = 10
        
        # Changes of coordonates for generating black teams
        if (self.color == "black"):
            return [Pion(x = i, y = (END_OF_BOARD - j), color = self.color) 
                    for j in range(INIT_X) for i in range(INIT_Y)]

        # Generate White teams
        return [Pion(x = i, y = j, color = self.color) 
                for j in range(INIT_X) for i in range(INIT_Y)]
    
    def get_pion(self):
        """Get list of all pions of a team

        Returns:
            list: all remaining Jetons objects of a given team
        """
        return self.pion
    
    def get_color(self):
        """Get color of team

        Returns:
            str: color of a team
        """
        return self.color
    
    def has_lost(self):
        """See if a given team has zero Jeton left. Means end of game

        Returns:
            bool: if the number of player in a team is zero
        """
        return len(self.pion) == 0
    
    def get_images(self):
        img_paths = ["C:\Users\josep\Documents\prog_projects\images\red_regular-no_bg.png",
                     "C:\Users\josep\Documents\prog_projects\images\red_queen-no_bg.png",
                     "C:\Users\josep\Documents\prog_projects\images\black_regular-no_bg.png",
                     "C:\Users\josep\Documents\prog_projects\images\black_queen-no_bg.png"]
        
        return {'red' : {'reg' : mpimg.imread(img_paths[0]), 'queen' : mpimg.imread(img_paths[1])},
                'black' : {'reg' : mpimg.imread(img_paths[2]), 'queen' : mpimg.imread(img_paths[3])}}
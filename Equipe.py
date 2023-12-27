from Pion import Pion
from PIL import ImageTk, Image

class Equipe():
    def __init__(self, color) -> None:
        self.color = color
        self.pions = []
        #self.pion = self.make_team()
    
    def make_team(self):
        """Generate the full team with accurate coordonates

        Returns:
            list: Pions of one team
        """
        # Set variables
        INIT_X, INIT_Y = 5, 4
        END_OF_BOARD = 10
        
        # Changes of coordonates for generating black teams
        if (self.color == "red"):
            return [Pion(x = i, y = (END_OF_BOARD - j)) for j in range(INIT_X) for i in range(INIT_Y)]

        # Generate black teams
        return [Pion(x = i, y = j) for j in range(INIT_X) for i in range(INIT_Y)]
    
    def get_pions(self):
        """Get list of all pions of a team

        Returns:
            list: all remaining Jetons objects of a given team
        """
        return self.pions
    
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
    
    def add_jeton(self, jeton):
        """Add a jeton to the pions teams

        Args:
            jeton (Jeton): New Jeton
        """
        self.pions.append(jeton)
    
    @classmethod
    def __get_images_dict(cls, team_color, piece_category):
        img_paths = ["C:\\Users\\josep\\Documents\\prog_projects\\images\\red_regular-no_bg.png",
                     "C:\\Users\\josep\\Documents\\prog_projects\\images\\red_queen-no_bg.png",
                     "C:\\Users\\josep\\Documents\\prog_projects\\images\\black_regular-no_bg.png",
                     "C:\\Users\\josep\\Documents\\prog_projects\\images\\black_queen-no_bg.png"]
        try:
            images_dict = {'red': {'reg': Image.open(img_paths[0]), 'queen': Image.open(img_paths[1])},
                           'black': {'reg': Image.open(img_paths[2]), 'queen': Image.open(img_paths[3])}}
            
            return images_dict[team_color][piece_category]
        
        except FileNotFoundError as e:
            print(f"Error loading image: {e}")
    
    @classmethod
    def get_images(cls, team_color, piece_category):
        img = cls.__get_images_dict(team_color = team_color, piece_category = piece_category)
        img = img.resize(size = (50, 50))
        return ImageTk.PhotoImage(img)
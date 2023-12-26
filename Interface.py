from tkinter import *
from Damier import Damier
from Equipe import Equipe

class JeuDeDame(Tk):
    def __init__(self, titre):
        super().__init__()
        self.title(titre)
        self.side = 650
        self.number_of_squares = 10
        self.colors = {'pale' : "#edd2a7", 'fonce' : "#a24e31"}
        self.board = []
        self.turn = ['white', 'red']
        
        # Generate attributes with relation to other classes
        self.damier = Damier()
        self.main_frame = Frame(master = self, width = self.side, height = self.side)
        self.teams = {"red": Equipe("red"), "black": Equipe("black")}
        
        # Miscellaneous functions
        self.make_board()
        self.center_ecran()
    
    def center_ecran(self):
        """Centrer la fenêtre au centre de l'écran
        """
        # Calculate appropriate width
        position_droite = int((self.winfo_screenwidth() - self.side) / 2)
        
        # Calculate appropriate height
        position_bas = int((self.winfo_screenheight() - self.side) / 2) - 50    
        
        # Applied geometry
        self.geometry(f"+{position_droite}+{position_bas}")
        
    def make_board(self):
        """Generate all the frame for the board with coordinated colors.
        """
        # Constants
        SIDE_SQUARE = self.side / self.number_of_squares
        
        for i in range(self.number_of_squares):
            for j in range(self.number_of_squares):
                
                # Create frame
                canvas = Canvas(self.main_frame, 
                                width=SIDE_SQUARE, 
                                height=SIDE_SQUARE, 
                                highlightthickness=0,
                                background=self.colors["pale" if (i + j) % 2 == 0 else "fonce"])

                
                # Place canvas widget on grid
                canvas.grid(row = i, column = j)
                
                # Append canvas to all canvas
                self.board.append(canvas)
        
        # Set every frame to viewers
        self.main_frame.pack()
        
        self.__set_pion_beginning("red")
        self.__set_pion_beginning("black")
        
        # Enable resize
        self.resizable(width = False, height = False) 
   
    def next_turn(self):
        """Switch turn order keeper
        """
        self.turn = self.turn[-1: ]
        
    def click(self, event = None):
        """Get info of mouse click.

        Args:
            event : Click of the mouse. Defaults to None.
        """
        infos = event.widget.grid_info()
        square = self.damier.get_square(x=infos['row'], y=infos['column'])
        print(square.get_occupancy())
    
    def __set_pion_beginning(self, team_color):
        """Set pions for a team for the beginning of play

        Args:
            team_color (str): name of the team color
        """
        # Get image, canvas side length and rows of team starts position
        img = Equipe.get_images(team_color=team_color, piece_category='reg')
        length = self.side / self.number_of_squares
        beg_x, end_x = (0, 4) if team_color == 'black' else (6, 10)
        
        for i in range(beg_x, end_x):
            for j in range(0, 10):
                if (i + j) % 2 == 0 : continue
                
                index = int(str(i) + str(j))
                canvas = self.board[index]

                # Create an image item on the Canvas
                canvas.create_image(length/2, length/2, anchor=CENTER, image=img)

                # Bind the click event to the Canvas
                canvas.bind("<Button-1>", self.click)

                # Store the image reference in the canvas (optional but can be useful)
                canvas.image = img
                
                # Set occupancy of square on damier
                square = self.damier.get_square(x=i, y=j)
                square.switch_occupancy()
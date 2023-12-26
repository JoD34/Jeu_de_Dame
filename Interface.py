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
                
                # Bind the click event to the Canvas
                if (i + j) % 2 != 0 : canvas.bind("<Button-1>", self.click)
                
                # Append canvas to canvas list
                self.board.append(canvas)
        
        # Set every canvas on main frame
        self.main_frame.pack()
        
        # Set pions on initial positions
        self.__set_pion_beginning("red")
        self.__set_pion_beginning("black")
        
        # Disable resize
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
        x, y = infos['row'], infos['column']
        square = self.damier.get_square(x=x, y=y)
        if (square.get_occupancy()): self.highlight_moves(x=x, y=y)
    
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

                # Store the image reference in the canvas (optional but can be useful)
                canvas.image = img
                
                # Set occupancy of square on damier
                square = self.damier.get_square(x=i, y=j)
                square.switch_occupancy()
                
    def highlight_moves(self, x, y, team_color):
        """Highlight squares with corresponding moves

        Args:
            x (int): number for the row
            y (int): number for the column
        """
        diags = self.damier.get_diagonal_squares(x=x, y=y, team_color=team_color)
        self.__highlight_square(square=diags['left'])
        self.__highlight_square(square=diags['right'])

    def __highlight_square(self, square):
        """Highlight squares for moves

        Args:
            square (Case): square in damier
        """
        # Get index data
        x = square.get_x()
        y = square.get_y()
        index = int(str(x) + str(y))
        
        # Assigned highlight
        canva = self.board[index]
        canva.highlightbackground('yellow')
    
    def delete_highlight(self,square):
        pass
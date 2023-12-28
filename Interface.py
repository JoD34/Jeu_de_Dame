from tkinter import *
from Damier import Damier
from Equipe import Equipe

class JeuDeDame(Tk):
    def __init__(self, titre):
        super().__init__()
        self.title(titre)
        self.side = 650
        self.number_of_squares = 10
        self.colors = {'pale' : "#edd2a7", 'fonce' : "#a24e31", 'highlighted' : 'lightblue'}
        self.select_piece = False
        self.selected = None
        self.highlighted = []
        self.board = []
        
        # Generate attributes with relation to other classes
        self.damier = Damier()
        self.main_frame = Frame(master = self, width = self.side, height = self.side)
        
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
        self.__init_positions()
        
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
        
        self.click_select(event.widget.grid_info())
        
    def  click_highlighted(self):
        self.remove_highlight()
    
    def click_select(self, infos):
        """Select the square that has been clicked on.

        Args:
            infos (dict): Information about the canvas that has been clicked on.
        """
        x, y = infos['row'], infos['column']
        square = self.damier.get_square(x=x, y=y)
        self.selected = square

        if (square.is_occupied()): self.highlight_moves(x=x, y=y, 
                                                        team_color=square.get_jeton().get_color(),
                                                        square = square)
    
    def __init_positions(self):
        for square in self.damier.get_squares():
            # If no jeton present on square , go to next square
            if not square.is_occupied(): continue
            
            # Get informations on Jeton object present on current square
            team_color = square.get_jeton().get_color()
            x, y = square.get_x(), square.get_y()
            
            # Get information for the Jeton's images
            length = self.side / self.number_of_squares
            img = Equipe.get_images(team_color=team_color, piece_category='reg')
            
            # Retrieve corresponding canvas
            canvas = self.board[int(str(x) + str(y))]
            
            # Create an image item on the Canvas
            canvas.create_image(length/2, length/2, anchor=CENTER, image=img)

            # Store the image reference in the canvas (optional but can be useful)
            canvas.image = img
                
    def highlight_moves(self, x, y, team_color, square):
        """Highlight squares with corresponding moves

        Args:
            x (int): number for the row
            y (int): number for the column
        """
        diags = self.damier.get_diagonal_squares(x=x, y=y, 
                                                 team_color=team_color, 
                                                 square=square)
        left, right = diags['left'], diags['right']
        if left is not None : self.__highlight_square(square=left)
        if right is not None : self.__highlight_square(square=right)

    def __highlight_square(self, square):
        """Highlight squares for moves

        Args:
            square (Case): square in damier
        """
        # Get index data
        index = int(str(square.get_x()) + str(square.get_y()))
        
        # Assigned highlight
        canva = self.board[index]
        canva.config(bg=self.colors["highlighted"])
        self.highlighted.append(canva)
        
    def remove_highlight(self):
        """remove highlight on square
        """
        for canvas in self.highlighted: canvas.config(bg = self.colors['fonce'])
        
    def move(self):
        pass
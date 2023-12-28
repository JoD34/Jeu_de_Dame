from tkinter import *
from Damier import Damier
from Equipe import Equipe

class JeuDeDame(Tk):
    def __init__(self, titre):
        super().__init__()
        
        # Generate general attributes
        self.title(titre)
        self.side = 650
        self.number_of_squares = 10
        self.length_img = self.side / self.number_of_squares
        self.colors = {'pale' : "#edd2a7", 'fonce' : "#a24e31", 'highlighted' : 'lightblue'}
        self.selected = None
        self.highlighted = []
        self.board = []
        
        # Generate attributes with relation to other classes
        self.damier = Damier()
        self.main_frame = Frame(master = self, width = self.side, height = self.side)
        
        # Generati attributes depending on other classes
        self.turn = self.damier.get_turn()
        
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
        # Get square info
        infos = event.widget.grid_info()
        x, y = infos['row'], infos['column']
        square = self.damier.get_square(x=x, y=y)
        
        canvas = self.board[int(str(x) + str(y))]
        
        if canvas in self.highlighted : self.click_highlighted(new_square=square)
        elif canvas not in self.highlighted : self.click_select(square=square)       
        
    def click_highlighted(self, new_square):
        """Action to follow if the click was on an highlighted square
        """
        self.damier.move_pieces(current_square=self.selected, new_square=new_square)
        self.remove_highlight()
        self.move_image(index_remove = int(str(self.selected.get_x()) + str(self.selected.get_y())), 
                        index_add = int(str(new_square.get_x()) + str(new_square.get_y())),
                        team_color=new_square.get_jeton().get_color())
    
    def click_select(self, square):
        """Select the square that has been clicked on.

        Args:
            infos (dict): Information about the canvas that has been clicked on.
        """
        self.remove_highlight()
        if square.get_jeton().get_color() != self.turn: 
            self.remove_highlight()
            return
        self.selected = square
        if (square.is_occupied()): self.highlight_moves(x=square.get_x(), y=square.get_y(), 
                                                        team_color=square.get_jeton().get_color(),
                                                        square = square)
    
    def __init_positions(self):
        for square in self.damier.get_squares():
            # If no jeton present on square , go to next square
            if not square.is_occupied(): continue
            
            # Get informations on Jeton object present on current square
            team_color = square.get_jeton().get_color()
            x, y = square.get_x(), square.get_y()
            
            # Retrieve corresponding canvas
            canvas = self.board[int(str(x) + str(y))]
            
            # Add image on a given canvas
            self.add_image(canvas=canvas, team_color=team_color, piece_category='reg')
                
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
        self.highlighted = []
    
    def remove_selected(self):
        self.selected = None
        
    def move_image(self, index_remove, index_add, team_color):
        """ List of command to move a given image from a canvas to another

        Args:
            index_remove (int): index of the canvas on which to remove an image
            index_add (int): index of the canvas on which to add an image
            team_color (str): black or red, represent the team color
        """
        self.remove_image(canvas = self.board[index_remove])
        self.add_image(canvas = self.board[index_add], 
                       team_color = team_color,
                       piece_category='reg')
        self.update_canvas(to_updates = [self.board[index_add], self.board[index_remove]])
        self.update_turn()
        
    def remove_image(self, canvas):
        """Remove image from a given canvas

        Args:
            canvas (Canvas): canvas on which the image will be deleted
        """
        canvas.delete('all')
    
    def add_image(self, canvas, team_color, piece_category):
        """Add image on a given canvas

        Args:
            canvas (Canvas): canvas on which to add the image
            team_color (str): black or red, represent the team color
            piece_category (str): type of piece. Either Pion or Dame.
        """
        img = Equipe.get_images(team_color=team_color, piece_category=piece_category)
        canvas.create_image(self.length_img/2, self.length_img/2, anchor=CENTER, image=img)
        canvas.image = img
        
    def update_canvas(self, to_updates):
        """Update de canvas which add changes on their image

        Args:
            to_updates (list): Canvas to update
        """
        for canvas in to_updates : canvas.update()
        
    def update_turn(self):
        """Update who's turn it is
        """
        self.turn = self.damier.get_turn()
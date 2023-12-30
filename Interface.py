from tkinter import *
from Damier import Damier
from Equipe import Equipe

class JeuDeDame(Tk):
    def __init__(self, titre):
        super().__init__()
        
        # Generate general attributes
        self.title(titre)
        self.iconphoto(False, Equipe.get_images(team_color='red', piece_category='queen'))
        self.side = 650
        self.number_of_squares = 10
        self.length_img = self.side / self.number_of_squares
        self.colors = {'pale' : "#edd2a7", 'fonce' : "#a24e31", 'move' : '#B5EDF9', 'take' : '#F7A2A1'}
        self.selected = None
        self.moves = []
        self.takes = []
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
        """Centrer la fenêtre avec l'écran
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
                                width = SIDE_SQUARE, 
                                height = SIDE_SQUARE, 
                                highlightthickness = 0,
                                background = self.colors["pale" if (i + j) % 2 == 0 else "fonce"])

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
        
    def click(self, event = None):
        """Get info of mouse click.

        Args:
            event : Click of the mouse. Defaults to None.
        """
        # Get square info
        infos = event.widget.grid_info()
        x, y = infos['row'], infos['column']
        square = self.damier.get_square(x=x, y=y)

        # Get corresponding canvas
        canvas = self.board[int(f"{x}{y}")]
        
        # Bloke move to only those with takes possibility
        if self.takes:
            if canvas in self.takes and not square.is_occupied():
                print(self.selected)
                self.click_take(canvas = canvas, square = square)
                self.remove_selected()

        # Clicks for moving pieces
        elif canvas in self.moves : self.click_highlighted(new_square=square)
        
        # Clicks to see move possibilities
        elif canvas not in self.moves :
            if (square.get_jeton() is None) or not self.check_jeton_color(case = square, color = self.turn):
                self.moves = self.remove_highlight(list_to_empty = self.moves)
                return
            self.click_select(square=square)

        # Refreshed images on the canvas
        self.refresh_board()
        # Get next turn
        self.__update_turn()
        
    def click_highlighted(self, new_square):
        """Action to follow if the click was on an highlighted square
        """
        # Move piece between 2 squares
        self.damier.move_pieces(current_square=self.selected, new_square=new_square)
        
        # Remove highlight of piece after moving
        self.moves = self.remove_highlight(list_to_empty = self.moves)
        
        # move the image of a piece between 2 canvas
        self.move_image(index_remove = int(f"{self.selected.get_x()}{self.selected.get_y()}"), 
                        index_add = int(f"{new_square.get_x()}{new_square.get_y()}"),
                        team_color = new_square.get_jeton().get_color())
        
        # Check for forced moves once the table have turns
        self.set_highlight_forced_moves()
    
    def click_select(self, square):
        """
        Action to follow if the click was for selecting a piece
        :param square: Case object, the square on which the click event happened
        :return: None
        """
        # Remove the highlighted squares following the clicked
        self.moves = self.remove_highlight(list_to_empty=self.moves)
        
        # Set the selected piece so it can be referred by the class itself
        self.selected = square

        # Once the piece has been selected, highlight its possible moves
        if square.is_occupied(): self.highlight_moves(square=square)
    
    def __init_positions(self):
        """Initiat the position of pieces for the beginning of play
        """
        for square in self.damier.get_squares():
            # If no jeton present on square , go to next square
            if not square.is_occupied(): continue
            
            # Get informations on Jeton object present on current square
            team_color = square.get_jeton().get_color()
            x, y = square.get_x(), square.get_y()
            
            # Retrieve corresponding canvas
            canvas = self.board[int(str(x) + str(y))]
            
            # Add image on a given canvas
            self.__add_image(canvas=canvas, team_color=team_color, piece_category='reg')
                
    def highlight_moves(self, square):
        """
        Highlight background of canvas presenting valid moves
        :param square: square of self.damier presenting a valid moves
        """
        
        # Get diagonal squares presenting possible moves
        diags = self.damier.get_diagonal_squares(x=square.get_x(),
                                                 y=square.get_y(),
                                                 team_color=self.turn)
        
        # Highlight square if the move is available
        for value in diags.values():
            if value :
                self.__highlight_square(square=value, action='move')

    def __highlight_square(self, square, action):
        """Highlight squares for moves

        Args:
            square (Case): square in damier
        """
        # Get corresponding canvas to highlight
        canva = self.board[int(f"{square.get_x()}{square.get_y()}")]
        
        # Switch configuration to highlight
        canva.config(bg=self.colors[action])
        
        # add the canvas to highlighted canvas
        self.moves.append(canva) if action == 'move' else self.takes.append(canva)
        
    def remove_highlight(self, list_to_empty):
        """remove highlight on square
        """
        # Get canvas present in a given list
        for canvas in list_to_empty: 
            
            # Remove the highlighted background
            canvas.config(bg = self.colors['fonce'])
        
        # Return an empty list 
        return []
    
    def remove_selected(self):
        """Empty the selected attribute
        """
        self.selected = None
        
    def move_image(self, index_remove, index_add, team_color):
        """ List of command to move a given image from a canvas to another

        Args:
            index_remove (int): index of the canvas on which to remove an image
            index_add (int): index of the canvas on which to add an image
            team_color (str): black or red, represent the team color
        """
        # Do corresponding action to the canvas
        self.__remove_image(canvas = self.board[index_remove])
        self.__add_image(canvas = self.board[index_add],
                         team_color = team_color, piece_category='reg')
        
        # Update the image presented to the user
        self.__update_canvas()
        
        # Update turns
        self.__update_turn()
        
    def __remove_image(self, canvas):
        """Remove image from a given canvas

        Args:
            canvas (Canvas): canvas on which the image will be deleted
        """
        canvas.delete('all')
    
    def __add_image(self, canvas, team_color, piece_category='reg'):
        """Add image on a given canvas

        Args:
            canvas (Canvas): canvas on which to add the image
            team_color (str): black or red, represent the team color
            piece_category (str): type of piece. Either Pion or Dame.
        """
        # Get image
        img = Equipe.get_images(team_color=team_color, piece_category=piece_category)
        
        # Create image
        canvas.create_image(self.length_img/2, self.length_img/2, anchor=CENTER, image=img)
        
        # Set image on canvas
        canvas.image = img
        
    def __update_canvas(self):
        """Update de canvas which add changes on their image

        Args:
            to_updates (list): Canvas to update
        """
        for canvas in range(len(self.board)) :
            if self.damier.get_squares()[canvas].is_occupied():
                self.board[canvas].update()
        
    def __update_turn(self):
        """Update who's turn it is
        """
        self.turn = self.damier.get_turn()
        
    def check_jeton_color(self, case, color):
        """Check if the jeton's color correspond to a given color

        Args:
            case (Case): Case to check the jeton that's on
            color (str): team color. Either red or black

        Returns:
            bool: True if the jeton's color is the same as the color argument. False otherwise
        """
        return case.get_jeton().get_color() == color
    
    def set_highlight_forced_moves(self):
        """ Get forced take squares to highlight
        """
        # Get the squares corresponding to forced moves
        cases = self.damier.get_forced_moves()
        
        # If the list isn't empty
        if cases: 
            # highlight square with the appropriate color
            for case in cases: self.__highlight_square(square = case, action='take')
            
    def get_origin_and_mid_piece_take(self, canvas):
        """Intermediate function, get square to make move

        Args:
            canvas (Canvas): canvas on witch the click event happended

        Returns:
            Case: The square on which the canvas correspond
        """
        # Get canvas corresponding to the given take
        index = self.takes.index(canvas)
        canvas_res = self.takes[index - 1]
        
        # Get infos for both the canvas
        canvas = canvas.grid_info()
        canvas_mid = canvas_res.grid_info()

        # Get Case object of origin
        case = self.damier.get_square(x = canvas_mid['row'] - (canvas['row'] - canvas_mid['row']),
                                      y = canvas_mid['column'] - (canvas['column'] - canvas_mid['column']))
        # Assign self.selected to origin pion
        self.selected = case.get_jeton()

        # Return corresponding square
        return canvas_res, case
        
    def click_take(self, canvas, square):
        """Action to follow when the click event correspond to taking a piece

        Args:
            canvas (Canvas): _description_
            square (Case): _description_
        """
        # Get information on mid and origin square of the move
        mid_canvas, self.selected = self.get_origin_and_mid_piece_take(canvas = canvas)
        color = self.selected.get_jeton().get_color()

        # Move images
        self.__remove_image(mid_canvas)
        self.move_image(index_remove = int(f"{self.selected.get_x()}{self.selected.get_y()}"), 
                        index_add = int(f"{square.get_x()}{square.get_y()}"),
                        team_color = color)
        
        # Remove Jeton from list of team
        taker_jeton = self.selected.get_jeton()
        self.damier.take_pion(taker=taker_jeton,
                              taken=self.get_case_from_canvas(mid_canvas).get_jeton(),
                              team_color=color)
        
        # Switch turn
        self.turn = self.damier.get_turn()
        
        # Correct the argument to remove_highlight
        self.takes = self.remove_highlight(list_to_empty=self.takes)
        
        # Reiterate the force move if necessary
        self.set_highlight_forced_moves()

        
    def get_case_from_canvas(self, canvas):
        """Get Case object corresponding to the canvas pass as argument

        Args:
            canvas (Canvas): Canvas on witch action of taking begins

        Returns:
            Case: Case corresponding to the canvas
        """
        return self.damier.get_squares()[self.board.index(canvas)]

    def refresh_board(self):
        for i in range(10):
            for j in range (10):
                index = int(f"{i}{j}")
                canvas = self.board[index]
                square = self.damier.get_squares()[index]
                if not square.is_occupied():
                    if not self.is_canvas_empty(canvas):
                        canvas.delete('all')
                        canvas.update()
                    continue
                color = square.get_jeton().get_color()
                self.__add_image(canvas=canvas, team_color=color)
                canvas.update()

    def is_canvas_empty(self, canvas):
        items = canvas.find_enclosed(0, 0, canvas.winfo_reqwidth(), canvas.winfo_reqheight())
        return not items

from tkinter import *
from Damier import Damier
from Dame import Dame
from Equipe import Equipe
from itertools import product

class JeuDeDame(Tk):
    def __init__(self, titre):
        super().__init__()
        
        # Generate general attributes
        self.title(titre)
        self.iconphoto(False, Equipe.get_images(team_color='red', piece_category='Dame'))
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
                canvas = Canvas(master = self.main_frame,
                                width = SIDE_SQUARE, 
                                height = SIDE_SQUARE, 
                                highlightthickness = 0,
                                background = self.colors["pale" if (i + j) % 2 == 0 else "fonce"])

                # Place canvas widget on grid
                canvas.grid(row = i, column = j)
                
                # Bind the click event to the Canvas
                if (i + j) % 2 != 0 :
                    canvas.bind("<Button-1>", self.click)
                    case = self.damier.get_square(x=i, y=j)
                    case.set_canvas(canvas)
                
                # Append canvas to canvas list
                self.board.append(canvas)
        
        # Set every canvas on main frame
        self.main_frame.pack()
        
        # Set pions on initial positions
        self.__init_positions()
        
        # Disable resize
        self.resizable(width = False, height = False) 
        
    def click(self, event = None):
        """
        List of command depending on the user input
        :param event: Click of the mouse. Defaults to None.
        """
        # Get square info
        infos = event.widget.grid_info()
        x, y = infos['row'], infos['column']
        square = self.damier.get_square(x=x, y=y)

        # Restricted moves to the forced moves
        if self.damier.restricted:

            # Make sure a piece has been selected
            if self.selected is None:
                if square.is_occupied() and square.get_jeton().get_color() == self.turn: self.selected = square

            else:
                # Get the taking path that has been selected by the click event
                for path in self.damier.restricted[self.selected]:
                    if path['land']  == square or path['take'] == square:
                        self.click_take(path=path)
                        break
                self.remove_selected()

        # Clicks for moving pieces
        elif square.get_canvas() in self.moves :
            self.click_highlighted(new_square=square)
            self.remove_selected()
        
        # Clicks to see move possibilities
        elif square.get_canvas() not in self.moves :
            if (square.get_jeton() is None or square.get_jeton().get_color() != self.turn):
                self.moves = self.remove_highlight(list_to_empty = self.moves)
                return
            self.click_select(square=square)

        # Switch images for new queens
        self.set_queens()
        # Get next turn
        self.__update_turn()

    def click_highlighted(self, new_square):
        """
        Action to follow if the click was on an highlighted square
        :param new_square: square on which to move the piece on self.selected
        """
        jeton = self.selected.get_jeton()

        # Move piece between 2 squares
        self.damier.move_pieces(current_square=self.selected, new_square=new_square)
        
        # Remove highlight of piece after moving
        self.moves = self.remove_highlight(list_to_empty = self.moves)
        
        # move the image of a piece between 2 canvas
        self.move_image(case_remove = self.selected, case_add = new_square)
        
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

    def click_take(self, path):
        """
        List of command when the click event correspond to taking a piece
        :param square: Case object of the click event
        """
        jeton = self.selected.get_jeton()
        # Get needed info on all squares present in a take
        color = self.selected.get_jeton().get_color()

        # Remove Jeton from list of team
        self.damier.take_pion(taker=self.selected, path=path, team_color=color)

        # Move images
        self.__remove_image(path['take'].get_canvas())
        self.move_image(case_remove=self.selected, case_add=path['land'])

        # Switch turn
        self.turn = self.damier.get_turn()

        # Correct the argument to remove_highlight
        self.takes = self.remove_highlight(list_to_empty=self.takes)

        # Reiterate the force move if necessary
        self.set_highlight_forced_moves()

    def __init_positions(self):
        """
        Initialize the pieces for the beginning of play
        """
        for square in self.damier.get_squares():
            if not square.is_occupied(): continue
            
            # Add image on a given canvas
            self.__add_image(case=square)
                
    def highlight_moves(self, square):
        """
        Highlight background of canvas presenting valid moves
        :param square: square of self.damier presenting a valid moves
        """
        # Get diagonal squares presenting possible moves
        moves = self.damier.get_diagonal_squares(case=square)

        # Highlight square if the move is available
        for value in moves:
                if value : self.__highlight_square(square=value, action='move')

    def __highlight_square(self, square, action):
        """
        Highlight canvas representing a possible move
        :param square: square analogue of canvas to be highlighted
        :param action: Either 'take' or 'move; Affect the highlighted color used
        """
        # Get corresponding canvas to highlight
        canva = square.get_canvas()
        
        # Switch configuration to highlight
        canva.config(bg=self.colors[action])
        
        # add the canvas to highlighted canvas
        self.moves.append(canva) if action == 'move' else self.takes.append(canva)
        
    def remove_highlight(self, list_to_empty):
        """
        Remove highlight on canvas of a given list
        :param list_to_empty: list to empty. Either the takes list or the moves list
        """
        for canvas in list_to_empty: canvas.config(bg = self.colors['fonce'])
        return []
    
    def remove_selected(self):
        """
        Empty the selected attribute
        """
        self.selected = None
        
    def move_image(self, case_remove, case_add):
        """
        List of command to move a given image from a canvas to another.
        :param canvas_remove: Canvas object on which to remove an image.
        :param canvas_add: Canvas object on which to add an image.
        """
        jeton = case_add.get_jeton()

        self.__remove_image(canvas = case_remove.get_canvas())
        self.__add_image(case = case_add)

        self.__update_canvas()
        self.__update_turn()
        
    def __remove_image(self, canvas):
        """
        Remove image from a given canvas
        :param canvas: Canvas object on which the image will be deleted
        """
        canvas.delete('all')
    
    def __add_image(self, case):
        """
        Add image on a given canvas
        :param canvas: Canvas object on which to add the image
        :param team_color: Either black or red
        :param piece_category: type of piece. Either Pion or Dame
        """
        # Get image
        jeton = case.get_jeton()
        canvas = case.get_canvas()

        img = Equipe.get_images(team_color=jeton.get_color(), piece_category=type(jeton).__name__)

        # Create image
        canvas.create_image(self.length_img/2, self.length_img/2, anchor=CENTER, image=img)
        
        # Set image on canvas
        canvas.image = img
        
    def __update_canvas(self):
        """
        Update de canvas which add changes on their image
        """
        for canvas in range(len(self.board)):
            if self.damier.get_squares()[canvas].is_occupied():
                self.board[canvas].update()
        
    def __update_turn(self):
        """
        Get matching turn as the Damier object
        """
        self.turn = self.damier.get_turn()
    
    def set_highlight_forced_moves(self):
        """
        Highlight squares corresponding to all forced moves
        """
        for key, paths in self.damier.restricted.items():
            self.__highlight_square(square=key, action='take')
            for path in paths:
                for _, case in path.items():
                        self.__highlight_square(square=case, action='take')

    def set_queens(self):
        """
        Check if a Pion object has reached a row to get promoted to a queen
        """
        # Get all the queens in a given team
        queens = [pion for pion in self.damier.teams[self.turn].get_pions() if isinstance(pion, Dame)]
        if not queens: return
        queen_canvas = [queen.get_case() for queen in queens]

        # Switch image for each queen canvas
        for case in queen_canvas:
            self.__remove_image(canvas=case.get_canvas())
            self.__add_image(case=case)
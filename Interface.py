from tkinter import *
from Damier import Damier
from Equipe import Equipe

class JeuDeDame(Tk):
    def __init__(self, titre):
        super().__init__()
        self.title(titre)
        self.side = 500
        self.main_frame = None
        self.teams = {"white": Equipe("#FFFFFF"), "noir": Equipe("#000000")}
        self.board = self.make_board()
        self.damier = Damier()
        self.make_board()
        self.resizable(width = False, height = False) 
    
    def center_ecran(self):
        """Centrer la fenêtre au centre de l'écran
        """
        # Calculate appropriate width
        position_droite = int((self.winfo_screenwidth() - self.winfo_reqwidth()) / 2)
        
        # Calculate appropriate height
        position_bas = int((self.winfo_screenheight() - self.winfo_reqheight()) / 2)
        
        # Applied geometry
        self.geometry(f"+{position_droite}+{position_bas}")
    
    def make_board(self):
        NUMBER_OF_SQUARES = 10
        # Make Frame
        self.main_frame = Frame(master = self, background =  "#FFFFFF")
        
        for i in range(NUMBER_OF_SQUARES):
            for j in range(NUMBER_OF_SQUARES):
                Frame(master = self.main_frame, background="#000")
        # Make Canvas
        #self.canvas = Canvas(master = self.main_frame, 
        #                     width = self.side, height = self.side)
        
        # Draw squares
        #for i in range(NUMBER_OF_SQUARES):
        #    for j in range(NUMBER_OF_SQUARES):
        #        color = Damier().get_colors()
        #        self.canvas.create_rectangle(x0 = i, x1 = i * 50,
        #                                     y0 = j, y1 = j * 50,
        #                                     fill = color['pale' if((i + j) % 2 != 0) else 'fonce'])
        self.center_ecran()
from tkinter import *
from Damier import Damier
from Equipe import Equipe

class JeuDeDame(Tk):
    def __init__(self, titre):
        super().__init__()
        self.title(titre)
        self.side = 750
        self.main_frame = None
        self.teams = {"white": Equipe("white"), "noir": Equipe("black")}
        self.board = self.make_board()
        self.damier = Damier()
        self.resizable(width = False, height = False) 
        self.center_ecran()
    
    def center_ecran(self):
        """Centrer la fenêtre au centre de l'écran
        """
        # Calculate appropriate width
        position_droite = int((self.winfo_screenwidth() - self.side) / 2)
        
        # Calculate appropriate height
        position_bas = int((self.winfo_screenheight() - self.side) / 2) + 100        
        # Applied geometry
        self.geometry(f"+{position_droite}+{position_bas}")
    
    def make_board(self):
        NUMBER_OF_SQUARES = 10
        SIDE_SQUARE = self.side / NUMBER_OF_SQUARES
        # Make Frame
        self.main_frame = Frame(master = self, background =  "#FFFFFF", width = self.side, height = self.side)
        
        for i in range(NUMBER_OF_SQUARES):
            for j in range(NUMBER_OF_SQUARES):
                frame = Frame(master = self.main_frame, 
                              background="#FFFFFF",
                              width = SIDE_SQUARE, 
                              height = SIDE_SQUARE,
                              highlightbackground = "#000000", 
                              highlightthickness = 0.5)
                frame.grid(row = i, column = j)
        self.main_frame.pack()
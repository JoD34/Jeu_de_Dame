from tkinter import *
from Damier import Damier
from Equipe import Equipe

class JeuDeDame(Tk):
    def __init__(self, titre):
        super().__init__()
        self.title(titre)
        self.side = 650
        self.main_frame = None
        self.colors = {'pale' : "#edd2a7", 'fonce' : "#a24e31"}
        self.teams = {"white": Equipe("white"), "noir": Equipe("black")}
        self.board = self.make_board()
        self.damier = Damier()
        self.resizable(width = False, height = False) 
        self.set_event()
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
        NUMBER_OF_SQUARES = 10
        SIDE_SQUARE = self.side / NUMBER_OF_SQUARES

        # Make main Frame
        self.main_frame = Frame(master = self, width = self.side, height = self.side)
        
        # Make frames for various squares
        for i in range(NUMBER_OF_SQUARES):
            for j in range(NUMBER_OF_SQUARES):
                frame = Frame(master = self.main_frame, 
                              background= self.colors["pale" if (i + j) % 2 == 0 else "fonce"],
                              width = SIDE_SQUARE, 
                              height = SIDE_SQUARE,
                              highlightbackground = "#000000", 
                              highlightthickness = 0.5)
                frame.grid(row = i, column = j)
        self.main_frame.pack()
        
    def click(self, event = None):
        grid_info = event.widget.grid_info()
        print("row:", grid_info["row"], "column:", grid_info["column"])
        
    def set_event(self):
        self.bind("<Button-1>", self.click)
from Case import Case
from Equipe import Equipe
from Pion import Pion


class Damier():
    def __init__(self) -> None:
        # Constant attributes
        self.square_per_side = 10
        self.restricted = {}

        # Attributes for generating runnin the game
        self.squares = self.create_board()
        self.turn = ['red', 'black']
        self.teams = {"red": Equipe(color="red"), "black": Equipe(color="black")}

        # Set pions
        self.init_pions('red')
        self.init_pions('black')

    def get_square(self, x, y):
        """
        Access a specific Case object in the Damier class
        :param x: (int) position in x on the board.
        :param y: (int) position in y on the board
        :return: Case object at the given position
        """
        return self.squares[int(f"{x}{y}")]

    def get_squares(self):
        """
        Get the list of Case objects representing the damier
        :return: (list) All Case objects making up the damier
        """
        return self.squares

    def create_board(self):
        """
        Create the entire board with the squares
        :return: (list) all the Case objects representing the board
        """
        return [Case(x=i, y=j) for i in range(self.square_per_side) for j in range(self.square_per_side)]

    def get_diagonal_squares(self, x, y, team_color):
        """
        Get diagonal squares of a given square.
        :param x: (int) row of the damier
        :param y: (int) column of the damier
        :param team_color: (str) color of team; either red or black
        :return: (dict) squares retrieved
        """
        # Correction of x depending on team's color
        x = x + 1 if team_color == 'black' else x - 1

        # Get squares that should be available
        return {'left': self.__retrieve_valid_square(x=x, y=(y - 1)),
                'right': self.__retrieve_valid_square(x=x, y=(y + 1))}

    def __retrieve_valid_square(self, x, y):
        """
        Retrieve the diagonal moves that are valid for a given square
        :param x: x coordinate of the new Case object.
        :param y: y coordinate of the new Case object.
        :return: Case object if move is valide. None otherwise.
        """
        # Check if column index is out of bound
        if (y >= 10) or (y < 0): return

        # Get square
        square = self.get_square(x=x, y=y)

        # Return if square should be highlighted
        return None if square.is_occupied() else square

    def init_pions(self, team_color):
        """
        Initialize pions, there position and there relation to a case
        :param team_color: (str) color of either team; red or black
        """
        beg_x, end_x = (0, 4) if team_color == 'black' else (6, 10)

        for i in range(beg_x, end_x):
            for j in range(10):

                # Only set Pions on dark squares
                if (i + j) % 2 == 0: continue

                # Get corresponding square
                square = self.get_square(x=i, y=j)

                # Generate jeton
                pion = Pion(x=i, y=j, case=square, color=team_color)

                # Add pion to square
                square.set_jeton(pion)

                # Add new pion to team
                self.teams[team_color].add_jeton(pion)

    def get_turn(self):
        """
        Get which team color is it to play.
        :return: (str) color of the team.
        """
        return self.turn[0]

    def next_turn(self):
        """
        Switch turn.
        """
        self.turn.reverse()

    def move_pieces(self, current_square, new_square):
        """
        List of actions representing a move
        :param current_square: Case object where the move begin
        :param new_square: Case object where the move end
        """
        # Remove jeton from current square
        jeton = current_square.get_jeton()
        current_square.remove_jeton()

        # Add jeton to new square
        new_square.set_jeton(jeton)
        jeton.set_case(new_case=new_square)

        # Update move to jeton coordinates
        jeton.set_x(new_square.get_x())
        jeton.set_y(new_square.get_y())

        # Switch turns
        self.next_turn()

        # Get forced moves for the next team to play
        self.get_forced_moves()

        self.print_game()

    def take_pion(self, taker, path, team_color):
        """
        Changes jetons position for a take movement
        :param taker: Case object from which originate the take
        :param path: Dict; Case object presented in the taking
        :param team_color: red or black; color of the taker
        """
        # Get move modification to add to the current position of taker
        self.teams[self.turn[1]].remove_jeton(path['take'].get_jeton())

        # Remove taken jeton from cases
        path['take'].remove_jeton()
        path['land'].set_jeton(taker.get_jeton())
        taker.remove_jeton()

        # Check if team has lost
        self.teams[team_color].has_lost()

        # Get extra take
        self.get_extra_take(square=path['land'])
        # Switch turn
        if not self.restricted: self.next_turn()

        # Get forced moves for the next team to play
        self.get_forced_moves()

        self.print_game()

    def get_forced_moves(self):
        """
        Get a dictionary of available takes
        """
        self.restricted = {}
        move_x = 1 if self.turn[0] == 'black' else -1

        for square in self.squares:
            # Interact with squares that contain pion of a given team only
            if not square.is_occupied() or square.get_jeton().get_color() != self.turn[0]: continue
            self.generate_dict_taking(square=square, move_x=move_x)

    def __get_square_takes(self, x, y, next_x, next_y, current):
        """
        Get the detail of the squares in a valid take
        :param x: position in x of taken square
        :param y: position in y of taken square
        :param next_x: x variation for the landing spot
        :param next_y: y variation for the landing spot
        :param current:  Square from which the move originates
        :return: (Dict) path of a valid take for a jeton of origin
        """
        # Check if column index is out of bound
        if (y + 1 >= 10) or (y - 1 < 0) or (x - 1 < 0) or (x + 1 >= 10): return {}

        # Get squares
        square_to_take = self.get_square(x=x, y=y)
        square_to_land = self.get_square(x=x + next_x, y=y + next_y)

        # Check if take is valid
        valid = (square_to_take.is_occupied() and
                 not square_to_land.is_occupied() and
                 not current.get_jeton().is_mate(other=square_to_take.get_jeton()))

        # Return the dict of a valid take
        return {current: {'take': square_to_take, 'land': square_to_land}} if valid else {}

    def print_game(self):
        """
        Prints the present pieces in the terminal. Rudimentale visualiztion of the game
        :return: None
        """
        for i in range(self.square_per_side):
            row = "|"
            for j in range(self.square_per_side):
                case = self.squares[int(f"{i}{j}")]
                if case.is_occupied():
                    row += "O" if case.get_jeton().get_color() == 'black' else "X"
                else:
                    row += " "
                row += "|"
            print(row)
        print('-' * 21)

    def get_extra_take(self, square):
        """
        Refresh restricted attribute if an extra take from an obligatory move is possible
        :param square: Case object on which the first take landed
        """
        self.restricted = {}
        move_x = 1 if self.turn[0] == 'black' else -1
        self.generate_dict_taking(square=square, move_x=move_x)

    def generate_dict_taking(self, square, move_x):
        """
        Make a dictionary of available moves and update the dictionary restricted attributes
        :param square: Case object from where the takes beginning
        :param move_x: Movement of the piece in the x-axis
        """
        for i in [1, -1]:
            x, y = square.get_x() + move_x, square.get_y() + i
            dict_take = self.__get_square_takes(x=x, y=y, next_x=move_x, next_y=i, current=square)
            # If a valid move exist: add the origin to the obligatory moves and update the dict accordingly
            if dict_take:
                if not (square in self.restricted.keys()):
                    self.restricted.update(dict_take)
                else:
                    self.restricted[square].update(dict_take[square])
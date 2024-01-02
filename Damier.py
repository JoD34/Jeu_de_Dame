from Case import Case
from Equipe import Equipe
from Pion import Pion
from Dame import Dame


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

    def get_diagonal_squares(self, case):
        """
        Get diagonal squares of a given square.
        :param case: Case object where the click event happened
        :return: dict of moves
        """
        # Switch if jeton is a Dame object
        if isinstance(case.get_jeton(), Dame): return self.get_queen_moves(case)

        # Get information on moves
        mod = case.get_jeton().get_move()
        x = case.get_jeton().get_x()
        y = case.get_jeton().get_y()

        # Get pions moves
        return ([self.__retrieve_valid_square(x=(x + i), y=(y - i)) for i in mod] +
                [self.__retrieve_valid_square(x=(x + i), y=(y + i)) for i in mod])

    def __retrieve_valid_square(self, x, y):
        """
        Retrieve the diagonal moves that are valid for a given square
        :param x: x coordinate of the new Case object.
        :param y: y coordinate of the new Case object.
        :return: Case object if move is valide. None otherwise.
        """
        # Check if column index is out of bound
        if (y >= 10) or (y < 0) or (x >= 10) or (x < 0):
            return

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

        # Check if a new queen has come
        self.check_if_queened(pion=new_square.get_jeton())

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

        # Set new x and y coordinates as well as the new Case object to the taker piece
        jeton = path['land'].get_jeton()
        jeton.set_x(path['land'].get_x())
        jeton.set_y(path['land'].get_y())
        jeton.set_case(new_case=path['land'])

        # Check if team has lost
        self.teams[team_color].has_lost()

        # Get extra take
        self.get_extra_take(square=path['land'])

        # Switch turn
        if not self.restricted:
            self.next_turn()
            self.get_forced_moves()

        self.check_if_queened(pion=path['land'].get_jeton())
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
        return {current: [{'take': square_to_take, 'land': square_to_land}]} if valid else {}

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
                if square in self.restricted.keys():

                    # Check if path is already in the dictionary
                    new_path = dict_take[square][0]
                    path_already_exists = any(
                        value['land'] == new_path['land'] and value['take'] != new_path['take']
                        for value in self.restricted[square]
                    )

                    # Only append if the take path doesn't already exist
                    if not path_already_exists:
                        self.restricted[square].append(new_path)

                else:
                    # Append a new path to the dictionary
                    self.restricted.update(dict_take)

    def check_if_queened(self, pion):
        """
        Check if the pion has reach the last row for queening
        :param pion: Pion object to check if queening
        """
        # If already a queen, don't mind me
        if isinstance(pion, Dame): return

        # Get infos on a pion
        x, way = pion.get_x(), pion.get_direction()

        # Check if queening
        if (way == 'up' and x == 0) or (way == 'down' and x == 9):
            team = self.teams[pion.get_color()]
            team.pion_to_queen(pion=pion)

    def get_queen_moves(self, case):
        """
        Get valid moves for a queen on the board.
        :param case: Case object representing the current position of the queen.
        :return: List of Case objects representing valid moves for the queen.
        """
        x = case.get_x()
        y = case.get_y()
        mod = case.get_jeton().get_max_move()

        # Get all possible moves
        moves = [[self.__retrieve_valid_square(x=(x + i*k),
                                               y=(y + i*j)) for i in range(1, mod)] for j in [1, -1] for k in [1, -1]]
        moves = [self.restrict_queen_move(path=move) for move in moves]

        return self.flatten_and_filter(moves)

    @staticmethod
    def restrict_queen_move(path):
        """
        Restrict the queen moves to stop before a double enemy
        :param path: One of the four ways a queen can move
        :return: List of moves the queen can take in  a given direction
        """
        for i, case in enumerate(path):

            if i == len(path):
                return path

            elif case is None and path[i + 1] is None:
                if i > 0:
                    return path[0:i]
                return

    def flatten_and_filter(self, lst):
        """
        Remove None elements from a list moves
        :param lst: List of moves possible for the queen
        :return: a given list without the none elements
        """
        result = []
        for item in lst:

            if isinstance(item, list):
                result.extend(self.flatten_and_filter(item))

            elif item is not None:
                result.append(item)

        return result

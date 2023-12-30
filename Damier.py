from Case import Case
from Equipe import Equipe
from Pion import Pion


class Damier():
    def __init__(self) -> None:
        # Constant attributes
        self.square_per_side = 10
        self.allowed_selected = []
        # Attributes for generating runnin the game
        self.squares = self.create_board()
        self.turn = ['red', 'black']
        self.teams = {"red": Equipe("red"), "black": Equipe("black")}
        self.token_to_play = []
        self.forced_moves = {}

        # Set pions
        self.init_pions('red')
        self.init_pions('black')

    def get_square(self, x, y):
        """Access a given square on the board.

        Args:
            x (int): position in x on the board.
            y (int): position in y on the board.

        Returns:
            Case: case on the board.
        """
        return self.squares[int(f"{x}{y}")]

    def get_squares(self):
        """Get the list of squares present in the damier

        Returns:
            list: All Case objects making up the damier
        """
        return self.squares

    def create_square(self, x, y):
        """Create a square

        Args:
            x (int): position in x on the board.
            y (int): position in y on the board.
            color (str): set color of the square.
        """
        return Case(x=x, y=y)

    def create_board(self):
        """Create the entire board with the squares
        """
        return [self.create_square(x=i, y=j) for i in range(self.square_per_side) for j in range(self.square_per_side)]

    def get_diagonal_squares(self, x, y, team_color):
        """Get diagonal squares of a given square.

        Args:
            x (int): row in the damier
            y (int): column in the damier
            team_color (str): color of team

        Returns:
            dict: squares retrieved
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
        """Initiate pions, there position and there relation to a case

        Args:
            team_color (str): color corresponding to one of two teams
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
        """Get which team color is it to play.

        Returns:
            str: color of the team.
        """
        return self.turn[0]

    def next_turn(self):
        """Switch turn.
        """
        self.turn.reverse()

    def move_pieces(self, current_square, new_square):
        """List of actions representing a move

        Args:
            current_square (_type_): _description_
            new_square (_type_): _description_
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

        self.print_game()

    def take_pion(self, taker, taken, team_color):
        """Changes jetons position for a take movement

        Args:
            taker (Jeton): Jeton that is capturing the other jeton
            taken (Jeton): Jeton that is being taken
            team_color (str): information about the movement of the current pion
        """
        # Get move modification to add to the current position of taker
        move_y = (taken.get_y() - taker.get_y()) * 2
        move_x = 2 if team_color == 'black' else -2

        # Remove taken jeton from cases
        taken.get_case().remove_jeton()
        taker.get_case().remove_jeton()

        # Get infos to remove the pion from the stake
        team_color = taken.get_color()
        self.teams[team_color].remove_jeton(taken)

        # Set new information to the taker pion
        new_x, new_y = taker.get_x() + move_x, taker.get_y() + move_y
        taker.set_x_y(new_x, new_y)
        self.get_square(x=new_x, y=new_y).set_jeton(taker)
        taken.delete_jeton()
        # Check if team has lost
        self.teams[team_color].has_lost()

        for key, value in self.teams.items():
            print(f"{key}: {len(value.get_pions())}")
        print(sum([1 for pion in self.squares if pion.is_occupied()]))

        # Switch turn
        self.next_turn()

        self.print_game()

    def get_forced_moves(self):
        """Get square for takes

        Args:
            team_color (str): color of pion

        Returns:
            list: all square which can be taken
        """
        res, self.allowed_selected = [], []
        move_x = 1 if self.turn[0] == 'black' else -1

        # Parse all square on the board
        for square in self.squares:

            # Interact with squares that contain pion of a given team only
            if not square.is_occupied() or square.get_jeton().get_color() != self.turn[0]: continue

            # set x on which to look upon
            x = square.get_x() + move_x

            # Parse the two columns to looks
            for i in [1, -1]:
                takes = self.__get_square_takes(x=x, y=square.get_y() + i, next_x=move_x, next_y=i, current=square)
                if takes and square not in self.allowed_selected:
                    res.extend(takes)
                    self.allowed_selected.append(square)
        return res

    def __get_square_takes(self, x, y, current, next_x, next_y):
        """_summary_

        Args:
            x (int): position in x of taken square
            y (int): position in y of taken square
            current (Case): Square from which the move originates
            next_x (int): x changes in for the x value for the landing strip
            next_y (int): y changes in for the y value for the landing strip

        Returns:
            list: Case for valid moves
        """
        # Check if column index is out of bound
        if (y + 1 >= 10) or (y - 1 < 0): return []

        my_jeton = current.get_jeton()
        # Get squares
        square_to_take = self.get_square(x=x, y=y)
        jeton_to_take = square_to_take.get_jeton()
        square_to_land = self.get_square(x=x + next_x, y=y + next_y)

        # Check if take is valid
        valid = (square_to_take.is_occupied() and
                 not square_to_land.is_occupied() and
                 not my_jeton.check_mate(other=jeton_to_take ))

        # Return the list of squares in the valid take
        return [] if not valid else [square_to_land, square_to_take]

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



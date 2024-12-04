import sys
import copy
import random


class Board:
    """
    Board class saves and modifies board during game

    This class initializes, prints, and updates the game board

    Attributes:
        board (list): 2D array for the board, 6x7

    Methods:
        __init__(state, game=None): Initializes New or Old Board
        print_board(): Prints the state of the game board.
        valid_move(row, col): Checks for valid move based on the provided row and column.
        move(row, col, token): Places a player's token at the specified row and column.
        board_full(): Checks if the board is completely filled with tokens.

    """
    def __init__(self, state, game=None):
        """
        Constructor for Board Class

        Parameters:
        state (str): Accepts state if board is new or old
        game (list, optional): Accepts an existing board if old
        """
        if state == "New":
            self.board = [
                [0 for number in range(7)]
                for num in range(6)
            ]
        elif state == "Old":
            self.board = game

    def print_board(self):
        """
        Prints the state of the board
        """
        for nested_list in self.board:  # this will print the board
            print(' '.join(map(str, nested_list)))

    def valid_move(self, row, col):
        """
        Checks if a move is valid

        Parameters:
        row (int): Row of the move
        col (int): Column of the move

        Returns:
        bool: If Move valid, True, otherwise False
        """
        if row == 6:
            if self.board[row - 1][col - 1] == 0:
                return True
            else:
                return False

        if self.board[row - 1][col - 1] == 0 and self.board[row][col - 1] != 0:
            return True

        return False

    def move(self, row, col, token):
        """
        Places a player's token at the row/col on board

        Parameters:
        row (int): Row of the move
        col (int): Column of the move
        token (int): Plauer's Token Choice
        """
        self.board[row - 1][col - 1] = token

    def board_full(self):
        """
        Checks if the board is full

        Returns:
        bool: True if Full, False if Not
        """
        for row in self.board:
            for col in row:
                if col == 0:
                    return False
        return True


class Player:
    """
    Player class for ConnectFour game

    Manages the player's name and selected token, including ensuring the token is unique and valid.

    Attributes:
        available_tokens (list): List of available token numbers (1-9) for players
        player (str): Player name
        token (int): Token number

    Methods:
        __init__(name, token): Initializes a player with a name and a unique token.
        player: Getter and setter for the player's name.
        token: Getter and setter for the player's token, ensuring it's not zero and is available.
        __str__(): Returns a string representation of the player with their name and token.

    """
    available_tokens = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    def __init__(self, name, token):
        """
        Initializes a player with a name and a token.

        Parameters:
        name (str): Player's name
        token (str): Player's token name
        """
        self.player = name
        self.token = token

    @property
    def player(self):
        """Getter for Player Name"""
        return self._player

    @player.setter
    def player(self, name):
        """
        Setter for Player Name

        Parameters:
        name (str): Player's name

        Raises:
        ValueError: If not a string
        """
        if isinstance(name, str):
            self._player = name
        else:
            raise ValueError("Please input a proper name of the string type.\n")

    @property
    def token(self):
        """Getter for Token"""
        return self._token

    @token.setter
    def token(self, token_num):
        """
        Setter for token, ensuring uniqueness

        Parameters:
        token_num (int): Token number player selects

        Raises:
        ValueError: If token is 0, or its already taken
        """
        if token_num == 0 or token_num not in Player.available_tokens:
            raise ValueError("Please input a one number token that is not 0 or presently taken.\n")
        else:
            Player.available_tokens.remove(token_num)
            self._token = token_num

    def __str__(self):
        """Returns a string representation of the player"""
        return f"Player {self._player} is using token {self._token}!\n"


class Game:
    """
    Game class handles flow of a two-player or AI-versus-player game.

    This class manages the game state, player initialization, gameplay loop, win-checking, saving, and loading of game states
    for either AI or 2 player game.

    Attributes:
        loaded_game (bool): Indicates if flag was from a saved state
        board (Board): The board instance representing the game state.
        p1 (Player): Initializing player object for p1
        p2 (Player or AI): Initializing player object for player or AI
        cur_player (str): Name of current player
        game_status (bool): Indicates status of game

    Methods:
        __init__(state, is_ai=False): Initializes or Loads Board and Players
        init_players(): Initializes the two players, getting names and tokens
        init_ai_game(): Initializes the game with AI
        ai_game(): AI-versus-player gameplay
        switch_player(): Switches the current player between Player 1 and Player 2.
        get_token(): Returns the token of the current player.
        win_check(token): Checks if player has won the game by verifying for a horizontal, vertical, or diagonal line of 4 tokens.
        play_game(): Player-versus-player gameplay
        save_game(): Saves game state for later playing
        load_game(): Loads previously saved game
    """
    #Used to Remove Content from Game if it's Loaded then Ended
    loaded_game = False

    def __init__(self, state, is_ai=False):
        """
        Constructor for the Game Class

        Parameters:
        state (str): 'New' for a new game, 'Old' to load an existing game
        is_ai (bool): Optional input for whether the game will involve AI
        """
        if state == "New":
            if is_ai:
                self.board = Board(state)
                self.init_ai_game()
            else:
                self.board = Board(state)
                self.init_players()
        elif state == "Old":
            self.load_game()

        self.game_status = False

    def init_players(self):
        """
        Initializes the two players by prompting for their names and tokens.
        """
        player1 = str(input("Please enter player one's name:\n"))
        player1_token = int(input("Please enter player one's token:\n"))
        while not isinstance(player1, str) or not isinstance(player1_token, int):
            player1 = str(input("Please enter a string name for player 1:\n"))
            player1_token = int(input("Please enter a valid digit token for player 1:\n"))
        player2 = str(input("Please enter player two's name\n"))
        player2_token = int(input("Please enter player two's token:\n"))
        while not isinstance(player2, str) or not isinstance(player2_token, int) or player1_token == player2_token:
            player2 = str(input("Please enter a string name for player 2:\n"))
            player2_token = int(input("Please enter a valid, unique, digit token for player 2:\n"))

        # Initialize Players
        self.p1 = Player(player1, player1_token)
        self.p2 = Player(player2, player2_token)

        # Let Player 1 be the first player
        self.cur_player = self.p1.player

        self.play_game()

    def init_ai_game(self):
        """
        Initializes the game when playing against an AI opponent. AI is always token 1.
        """
        player1 = str(input("Please enter player one's name:\n"))
        player1_token = int(input("Please enter player one's token:\n"))
        while not isinstance(player1, str) or not isinstance(player1_token, int) or player1_token == 1:
            player1 = str(input("Please enter a string name for player 1:\n"))
            player1_token = int(input("Please enter a valid digit token for player 1:\n"))
        self.p1 = Player(player1, player1_token)
        self.p2 = AI('AI', 1, player1_token)
        self.cur_player = self.p1.player
        self.ai_game()

    def ai_game(self):
        """
        Runs the game when one player is an AI. The AI makes moves automatically.
        """
        while not self.win_check(self.get_token()) or self.board.board_full():
            self.board.print_board()
            if self.cur_player == 'AI':
                depth = 5
                best_spot = self.p2.minimax(self.board.board, depth, -99999, 99999, False)[0]
                best_spot[0] += 1
                best_spot[1] += 1
                self.board.move(best_spot[0], best_spot[1], self.get_token())
            else:
                move_row = int(input(f"Please enter the row, {self.cur_player}, you'd like to move to:\n"))
                move_col = int(input(f"Please enter the column, {self.cur_player}, you'd like to move to:\n"))
                while not self.board.valid_move(move_row, move_col) or self.board.board_full():
                    move_row = int(input(f"Please enter a valid row, {self.cur_player}:\n"))
                    move_col = int(input(f"Please enter a valid column, {self.cur_player}:\n"))

                self.board.move(move_row, move_col, self.get_token())

            if (self.win_check(self.get_token()) or self.board.board_full()) and Game.loaded_game:
                with open('game_pause.txt', 'w') as file:
                    pass

            if self.win_check(self.get_token()):
                history = GameHistory()
                history.add_history(self.cur_player)
                print(f"{self.cur_player} Wins")
                print("Game Over")
                sys.exit()

            if self.board.board_full():
                print("The Board is Full, There is No Winner. Restart Game.")
                history = GameHistory()
                history.add_history("Tie")
                print("Game Over")
                sys.exit()

            self.switch_player()

            pause = int(input("Press 1 if You would like to pause the game, 0 to continue:\n"))
            if pause:
                print("Saving Game...\n")
                self.save_game()
            else:
                print("Continuing...\n")

    def switch_player(self):
        """
        Switches the current player between Player 1 and Player 2.
        """
        self.cur_player = self.p1.player if self.cur_player == self.p2.player else self.p2.player

    def get_token(self):
        """
        Returns the token of the current player.

        Returns:
        int: The token of the current player.
        """
        if self.cur_player == self.p1.player:
            return self.p1.token
        else:
            return self.p2.token

    def win_check(self, token):
        """
        Checks if the current player has won the game by verifying for a horizontal, vertical, or diagonal line of 4 tokens.

        Parameters:
        token (int): The token of the player whose victory is being checked.

        Returns:
        bool: True if the player has won, False otherwise.
        """
        for row in range(6):
            for col in range(7):
                if self.board.board[row][col] == token:
                    if col < 4 and self.board.board[row][col + 1] == token and self.board.board[row][
                        col + 2] == token and self.board.board[row][col + 3] == token:
                        return True
                    if row < 3 and self.board.board[row + 1][col] == token and self.board.board[row + 2][
                        col] == token and self.board.board[row + 3][col] == token:
                        return True
                    if row < 3 and col < 4 and self.board.board[row + 1][col + 1] == token and \
                            self.board.board[row + 2][col + 2] == token and self.board.board[row + 3][col + 3] == token:
                        return True
                    if row > 2 and col < 4 and self.board.board[row - 1][col + 1] == token and \
                            self.board.board[row - 2][col + 2] == token and self.board.board[row - 3][col + 3] == token:
                        return True
        return False
    def play_game(self):
        '''
        Controls regular 2 player gameplay

        :return:
        Will end the program through either pausing or a winner or a draw
        '''
        while not self.win_check(self.get_token()) or self.board.board_full():
            self.board.print_board()
            move_row = int(input(f"Please enter the row, {self.cur_player}, you'd like to move to:\n"))
            move_col = int(input(f"Please enter the column, {self.cur_player}, you'd like to move to:\n"))
            while not self.board.valid_move(move_row, move_col) or self.board.board_full():
                move_row = int(input(f"Please enter a valid row, {self.cur_player}:\n"))
                move_col = int(input(f"Please enter a valid column, {self.cur_player}:\n"))

            self.board.move(move_row, move_col, self.get_token())

            if (self.win_check(self.get_token()) or self.board.board_full()) and Game.loaded_game:
                with open('game_pause.txt', 'w') as file:
                    pass
            if self.win_check(self.get_token()):
                if Game.loaded_game:
                    with open('game_pause.txt', 'w') as file:
                        pass
                history = GameHistory()
                history.add_history(self.cur_player)
                print(f"{self.cur_player} Wins")
                print("Game Over")
                sys.exit()

            if self.board.board_full():
                if Game.loaded_game:
                    with open('game_pause.txt', 'w') as file:
                        pass
                print("The Board is Full, There is No Winner. Restart Game.")
                history = GameHistory()
                history.add_history("Tie")
                print("Game Over")
                sys.exit()

            self.switch_player()

            pause = int(input("Press 1 if You would like to pause the game, 0 to continue:\n"))
            if pause:
                print("Saving Game...\n")
                self.save_game()
            else:
                print("Continuing...\n")
    def save_game(self, savegame="game_pause.txt"):
        """
        Saves the current game state to a file for later loading.
        """
        with open(savegame, 'w') as game_state:
            game_state.write(f"{self.p1.player} : {self.p1.token}\n")
            game_state.write(f"{self.p2.player} : {self.p2.token}\n")
            game_state.write(f"Turn : {self.get_token()}\n")
            for row in self.board.board:
                game_state.write(f"{row}\n")
        print("Closing Game. Open Loaded Game Next Time to Resume.")
        sys.exit()

    def load_game(self, loadgame="game_pause.txt"):
        """
        Loads a saved game from a file.
        """
        Game.loaded_game = True
        game = []
        try:
            with open(loadgame, 'r') as game_state:
                for line in game_state:
                    game.append(line.strip())
        except FileNotFoundError:
            print("No Old Game File Found")

        p1, p1_token = game[0].strip().split(":")
        p1_token = p1_token.strip()
        p1 = p1.strip()
        # print(p1, p1_token)
        self.p1 = Player(p1, int(p1_token))

        p2, p2_token = game[1].strip().split(":")
        p2_token = p2_token.strip()
        p2 = p2.strip()
        if p2 == "AI":
            self.p2 = AI('AI', 1, p1_token)

            self.cur_player = self.p1.player if self.p1.token == int(game[2].split(":")[1]) else self.p2.player

            load_board = []
            for row in game[3:9]:  # Skip the first three lines which are player data
                # Remove the square brackets and split by commas, then convert to integers
                row = row.strip()[1:-1]  # Strip off the surrounding brackets
                row_list = [int(x.strip()) for x in row.split(',')]  # Split by commas and convert to integers
                load_board.append(row_list)  # Add the row to the board
            self.board = Board("Old", load_board)
            self.ai_game()

        else:
            self.p2 = Player(p2, int(p2_token))

            self.cur_player = self.p1.player if self.p1.token == int(game[2].split(":")[1]) else self.p2.player

            load_board = []
            for row in game[3:9]:  # Skip the first three lines which are player data
                # Remove the square brackets and split by commas, then convert to integers
                row = row.strip()[1:-1]  # Strip off the surrounding brackets
                row_list = [int(x.strip()) for x in row.split(',')]  # Split by commas and convert to integers
                load_board.append(row_list)  # Add the row to the board
            self.board = Board("Old", load_board)

            self.play_game()

        print("Game Loaded.")

class GameHistory:
    '''
    Class for managing and storing a previous game

    This class handles the reading, updating, and displaying of game history stored in a file. It allows tracking
    player names along with their total wins.

    Attributes:
        file_name (str): Default is "game_history.txt", file for reading data
        history (dict): Dictionary mapping players to their wins

    Methods:
        load_history(): Loads the game history from the file and returns it as a dictionary
        add_history(player): Adds a win for the given player or updates existing count
        disp_history(): Displays the game history, showing each players wins
    '''
    def __init__(self, file_name="game_history.txt"):
        """
        GameHistory class constructor

        Parameters:
        file_name (str): Default name of the file that stores the game history
        """
        self.file_name = file_name
        self.history = self.load_history()

    def load_history(self):
        """
        Loads the game history from the file

        Returns:
        dict: Player names and their wins
        """
        try:
            with open(self.file_name, "r") as game_hist:
                history = {}

                i = 0
                for line in game_hist:
                    if i == 0:
                        i += 1
                    else:
                        player, wins = line.strip().split(" : ")
                        history[player] = int(wins)
                return history
        except FileNotFoundError:
            return {}

    def add_history(self, player):
        """
        Adds the given player to the game history or increases their count.

        Parameters:
        player (str): The name of the player whose win to add

        Raises:
        ValueError: If the provided player is not a string
        """
        if not isinstance(player, str):
            raise ValueError("Incorrect type, unable to add to history")
        else:
            with open(self.file_name, "w") as game_add:
                game_add.write(f"Player : # Wins\n")
                if player in self.history:
                    self.history[player] += 1
                    for player, wins in self.history.items():
                        game_add.write(f"{player} : {wins}\n")
                else:
                    self.history[player] = 1
                    for player, wins in self.history.items():
                        game_add.write(f"{player} : {wins}\n")

    def disp_history(self):
        """
        Displays the game history showing each player and their win count.
        """
        print("Here's the Past Winners and Their Totals:")
        for player, wins in self.history.items():
            if wins == 1:
                print(f"{player} has {wins} win.")
            else:
                print(f"{player} has {wins} wins.")


class AI(Player):
    '''
    """
    AI class for automated ConnectFour Moves

    AI uses a minimax algorithm with alpha-beta pruning, based on a custom heuristic function
    to determine optimal moves.

    Attributes:
        human_token (int): Token for opponent
        token (int): AI's Token (1)
        name (str): AI name (AI)

    Methods:
        transpose(s): Transposes the board to check moves
        valid_moves(s): Returns a list of valid moves for AI
        switch_nested_values(nested_lists): Switches column and row values for valid move checking
        win_check(s): Checks the board for a winner (horizontal, vertical, or diagonal)
        count_score(s): Evaluates the game board with heuristic and returns a score difference
        minimax(board, depth, alpha, beta, player_bool): Implements the minimax algorithm with alpha-beta pruning
    """
    '''
    def __init__(self, name, token, human):
        """
        AI Class Initialization, Inheritance of Player attributes

        Parameters:
        name (str): AI name (AI)
        token (int): AI token (1)
        human (int): Human token used for minimax algorithm
        """
        super().__init__(name, token)
        self.human_token = human

    def transpose(self, s):
        """
        Transposes a 2D array for move checking

        Parameters:
        s (list): Board to transpose

        Returns:
        list: 2D transposed array
        """
        return [[s[j][i] for j in range(len(s))] for i in range(len(s[0]))]

    def valid_moves(self, s):
        """
        Checks for valid moves in each column of the board.

        Parameters:
        s (list): 2D board to check for moves

        Returns:
        list: List of possible moves, each represented by a list of coordinates [col, row]
        """
        new_s = self.transpose(s)
        possible_moves = []
        for col in range(len(new_s)):
            for row in range(len(new_s[0]) - 1, -1, -1):
                if new_s[col][row] == 0:
                    possible_moves.append([col, row])
                    break
        self.switch_nested_values(possible_moves)
        return possible_moves

    def switch_nested_values(self, nested_lists):
        """
        Switches the values from col, row to row, col to be implemented onto board

        Parameters:
        nested_lists (list): List of pairs to switch
        """
        for nested_list in nested_lists:
            nested_list[0], nested_list[1] = nested_list[1], nested_list[0]

    def win_check(self, s):
        """
        Checks the board for a winner:
            four in a row, diagonal, or column

        Parameters:
        s (list): Board being checked

        Returns:
        int: Token for the winner, if any
        """
        # Horizontal Checks
        for row in range(len(s)):
            for col in range(len(s[0]) - 3):
                if s[row][col] == s[row][col + 1] == s[row][col + 2] == s[row][col + 3] and s[row][col] != 0:
                    return s[row][col]

        # Vertical Checks
        for y in range(len(s) - 3):
            for z in range(len(s[0])):
                if s[y][z] == s[y + 1][z] == s[y + 2][z] == s[y + 3][z] and s[y][z] != 0:
                    return s[y][z]

        # Two sets of Diagonal checks
        for a in range(len(s) - 3):
            for b in range(len(s[0]) - 3):
                if s[a][b] == s[a + 1][b + 1] == s[a + 2][b + 2] == s[a + 3][b + 3] and s[a][b] != 0:
                    return s[a][b]
                elif s[a][6 - b] == s[a + 1][5 - b] == s[a + 2][4 - b] == s[a + 3][3 - b] and s[a][b] != 0:
                    return s[a][b]
        return False

    def count_score(self, s):
        """
        Custom heuristic function to evaluate moves based on AI and opponent move potential.

        Parameters:
        s (list): Board to eval

        Returns:
        int: Potential score difference between player and AI
        """
        player1Score = 0
        player2Score = 0
        # Check horizontally
        for row in range(len(s)):
            for col in range(len(s[0]) - 3):
                if s[row][col:col + 4].count([self.token]) == 4:
                    player1Score += 100
                elif s[row][col:col + 4].count([self.token]) == 3:
                    player1Score += 5
                elif s[row][col:col + 4].count([self.token]) == 2:
                    player1Score += 2
                if s[row][col:col + 4].count([self.human_token]) == 4:
                    player2Score += 100
                elif s[row][col:col + 4].count([self.human_token]) == 3:
                    player2Score += 5
                elif s[row][col:col + 4].count([self.human_token]) == 2:
                    player2Score += 2

        # Check vertically
        for col in range(len(s[0])):
            for row in range(len(s) - 3):
                if [s[row + i][col] for i in range(4)].count([self.token]) == 4:
                    player1Score += 100
                elif [s[row + i][col] for i in range(4)].count([self.token]) == 3:
                    player1Score += 5
                elif [s[row + i][col] for i in range(4)].count([self.token]) == 2:
                    player1Score += 2
                if [s[row + i][col] for i in range(4)].count([self.human_token]) == 4:
                    player2Score += 100
                elif [s[row + i][col] for i in range(4)].count([self.human_token]) == 3:
                    player2Score += 5
                elif [s[row + i][col] for i in range(4)].count([self.human_token]) == 2:
                    player2Score += 2

        # Check diagonally
        for row in range(len(s) - 3):
            for col in range(len(s[0]) - 3):
                if [s[row + i][col + i] for i in range(4)].count([self.token]) == 4:
                    player1Score += 100
                elif [s[row + i][col + i] for i in range(4)].count([self.token]) == 3:
                    player1Score += 5
                elif [s[row + i][col + i] for i in range(4)].count([self.token]) == 2:
                    player1Score += 2
                if [s[row + i][col + i] for i in range(4)].count([self.human_token]) == 4:
                    player2Score += 100
                elif [s[row + i][col + i] for i in range(4)].count([self.human_token]) == 3:
                    player2Score += 5
                elif [s[row + i][col + i] for i in range(4)].count([self.human_token]) == 2:
                    player2Score += 2
                if [s[row + i][col + 3 - i] for i in range(4)].count([self.token]) == 4:
                    player1Score += 100
                elif [s[row + i][col + 3 - i] for i in range(4)].count([self.token]) == 3:
                    player1Score += 5
                elif [s[row + i][col + 3 - i] for i in range(4)].count([self.token]) == 2:
                    player1Score += 2
                if [s[row + i][col + 3 - i] for i in range(4)].count([self.human_token]) == 4:
                    player2Score += 100
                elif [s[row + i][col + 3 - i] for i in range(4)].count([self.human_token]) == 3:
                    player2Score += 5
                elif [s[row + i][col + 3 - i] for i in range(4)].count([self.human_token]) == 2:
                    player2Score += 2

        for rows in range(3, 6):
            for cols in range(2, 5):
                if s[rows][cols] == self.human_token:
                    player2Score += 2
                elif s[rows][cols] == self.token:
                    player1Score += 2

        return player1Score - player2Score

    def minimax(self, board, depth, alpha, beta, player_bool):
        """
        Minimax algorithm with alpha-beta pruning to choose the best move for the AI.

        Parameters:
        board (list): The current game board.
        depth (int): The search depth for the minimax algorithm.
        alpha (int): The current best score for the maximizing player.
        beta (int): The current best score for the minimizing player.
        player_bool (bool): A boolean indicating whether it is the AI's turn (True) or the player's turn (False).

        Returns:
        list: The optimal move for the AI along with the score.
        """
        possibles = self.valid_moves(board)
        # Base Case
        if depth == 0 or self.win_check(board):
            if self.win_check(board):
                if self.win_check(board) == self.token:
                    return [None, 99999]
                elif self.win_check(board) == self.human_token:
                    return [None, -99999]
                else:
                    return [None, self.count_score(board)]
            else:
                return [None, self.count_score(board)]

        if player_bool:
            value = -99999
            best_position = random.choice(possibles)
            for possible in possibles:
                board_copy = copy.deepcopy(board)
                board_copy[possible[0]][possible[1]] = self.token
                value = max(value, self.minimax(board_copy, depth - 1, alpha, beta, False)[1])
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return best_position, value
        else:
            value = 99999
            best_position = random.choice(possibles)
            for possible in possibles:
                board_copy = copy.deepcopy(board)
                board_copy[possible[0]][possible[1]] = self.human_token
                value = min(value, self.minimax(board_copy, depth - 1, alpha, beta, True)[1])
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return best_position, value


# Main Game Loop
if __name__ == "__main__":
    history = GameHistory()
    if len(history.history) > 0:
        history.disp_history()

    game_state = str(input('''Welcome to ConnectFour! 
Type 'New' if this is a new game. Type 'Old' if you are loading a
previous game.\n'''))

    ai_ans = ""
    if game_state == "Old":
        ai_ans = str(input("Type 'Yes' if you played with AI, and 'No' if you didn't.\n"))
    if game_state == "New":
        ai_ans = str(input("Type 'Yes' if you want to play against an AI, and 'No' if you don't.\n"))
    if ai_ans == "No":
        game = Game(game_state)
    elif ai_ans == "Yes":
        game = Game(game_state, True)


















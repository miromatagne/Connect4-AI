from copy import deepcopy
import random
import uuid
import numpy as np
from observable import Observable
from bot import Bot
from file_recording import FileRecording
from event import Event
from monte_carlo import MonteCarlo
from minimax import MiniMax

EMPTY = 0
ROW_COUNT = 6
COLUMN_COUNT = 7
WINDOW_LENGTH = 4

MONTE_CARLO = "MONTE_CARLO"
MINIMAX = "MINIMAX"
RANDOM = "RANDOM"
RANDOM_IMPR = "RANDOM_IMPR"


class Connect4Game(Observable):

    def __init__(self, player1, player2, bot1_model=None, bot2_model=None, rows=6, cols=7, iteration=None, depth1=None, depth2=None, pruning1=True, pruning2=True):
        """
            Constructor of the Connect4Game class.

            :param player1: first player, can be a bot of any type
            :param player2: second player, can be a bot of any type
            :param bot1_model: model used, if necessary, with the bot of player1
            :param bot2_model: model used, if necessary, with the bot of player2
            :param rows: number of rows in the game
            :param cols: number of columns in the game
            :param iteration: number of iterations used by the players using MCTS
            :param depth1: depth used in the MiniMax algorithm of player1, it is uses MiniMax
            :param depth2: depth used in the MiniMax algorithm of player2, it is uses MiniMax
        """
        super().__init__()
        self._rows = rows
        self._cols = cols
        self._board = None
        self._turn = None
        self._won = None
        self._round = 0
        self.bot = None
        self.moves = {1: [], -1: []}
        self.file_recording = FileRecording()
        self.reset_game()
        if player1 == MONTE_CARLO:
            self._player1 = MonteCarlo(self, iteration=iteration)
        elif player1 == MINIMAX:
            self._player1 = MiniMax(self, depth=depth1, pruning=pruning1)
        else:
            if bot1_model is not None:
                self._player1 = Bot(self, model=bot1_model)
            else:
                self._player1 = Bot(self, bot_type=player1)
        if player2 == MONTE_CARLO:
            self._player2 = MonteCarlo(self, iteration=iteration)
        elif player2 == MINIMAX:
            self._player2 = MiniMax(self, depth=depth2, pruning=pruning2)
        else:
            if bot2_model is not None:
                self._player2 = Bot(self, model=bot2_model)
            else:
                self._player2 = Bot(self, bot_type=player2)
        self.last_move = None

    def reset_game(self):
        """
        Resets the game state (board and variables)
        """
        # print("reset")
        self._board = [[0 for _ in range(self._rows)]
                       for _ in range(self._cols)]
        self._starter = random.choice([-1, 1])
        # print(self._starter)
        self._turn = self._starter
        # (self._turn)
        self._won = None
        self.notify(Event.GAME_RESET)

    def place(self, c, save=True):
        """
            Tries to place the playing colour on the c-th column

            :param c: column to place on
            :return: position of placed colour or None if not placeable
        """
        # print(self._board)
        for r in range(self._rows):
            if self._board[c][r] == 0:
                self._board[c][r] = self._turn
                self.last_move = [c, r]
                self.notify(Event.PIECE_PLACED, (c, r))
                if save == True:
                    self.file_recording.write_to_history(self._round, self._board)
                self.moves[self._turn].append(c)

                exists_winner = self.check_win((c, r))
                if exists_winner:
                    b = 0
                    if self._turn == self._starter:  # Winner is the player that started
                        b = 1
                    if save == True:
                        self.file_recording.write_to_winning_moves(
                            b, self._turn, self.moves[self._turn])
                    self._won = self._turn
                    self.notify(Event.GAME_WON, self._won)

                if self._turn == 1:
                    self._turn = -1
                else:
                    self._turn = 1

                self._round = self._round + 1
                return c, r
        return None

    def check_win(self, pos):
        """
            Checks for win/draw from newly added disc

            :param pos: position from which to check the win
            :return: player number if a win occurs, 0 if a draw occurs, None otherwise
        """
        c = pos[0]
        r = pos[1]
        player = self._board[c][r]

        min_col = max(c-3, 0)
        max_col = min(c+3, self._cols-1)
        min_row = max(r - 3, 0)
        max_row = min(r + 3, self._rows - 1)

        # Horizontal check
        count = 0
        for ci in range(min_col, max_col + 1):
            if self._board[ci][r] == player:
                count += 1
            else:
                count = 0
            if count == 4:
                # print("Horizontal win")
                # self._won = player
                # self.notify(Event.GAME_WON, self._won)
                # return self._won
                return True

        # Vertical check
        count = 0
        for ri in range(min_row, max_row + 1):
            if self._board[c][ri] == player:
                count += 1
            else:
                count = 0
            if count == 4:
                # print("Vertical win")
                # self._won = player
                # self.notify(Event.GAME_WON, self._won)
                # return self._won
                return True

        count1 = 0
        count2 = 0
        # Diagonal check
        for i in range(-3, 4):
            # bottom-left -> top-right
            if 0 <= c + i < self._cols and 0 <= r + i < self._rows:
                if self._board[c + i][r + i] == player:
                    count1 += 1
                else:
                    count1 = 0
                if count1 == 4:
                    # print("Diagonal BL-TR win")
                    # self._won = player
                    # self.notify(Event.GAME_WON, self._won)
                    # return self._won
                    return True
            # bottom-right -> top-let
            if 0 <= c + i < self._cols and 0 <= r - i < self._rows:
                if self._board[c + i][r - i] == player:
                    count2 += 1
                else:
                    count2 = 0
                if count2 == 4:
                    # print("Diagonal BR-TL win")
                    # self._won = player
                    # self.notify(Event.GAME_WON, self._won)
                    # return self._won
                    return True

        # Draw check
        if sum([x.count(0) for x in self._board]) == 0:
            # print("5")
            # self._won = 0
            # self.notify(Event.GAME_WON, self._won)
            # return self._won
            return True

        return False

    def get_cols(self):
        """
            :return: The number of columns of the game
        """
        return self._cols

    def get_rows(self):
        """
            :return: The number of rows of the game
        """
        return self._rows

    def get_win(self):
        """
            :return: If one play won or not
        """
        return self._won

    def get_turn(self):
        """
            :return: To which player is the turn
        """
        return self._turn

    def get_board(self):
        """
            :return: A copy of the game board
        """
        return self._board.copy()

    def board_at(self, c, r):
        """
            :param: c, the column
            :param: r, the row
            :return: What value is held at column c, row r in the board
        """
        return self._board[c][r]

    def copy_state(self):
        """
            Use this instead of the copy() method. Useful as we don't want our graphical interface (viewed as an Observer in this class)
            to be updated when we are playing moves in our tree search.
        """

        # Temporary removes the
        temporary_observers = self._observers
        self._observers = []

        new_one = deepcopy(self)
        new_one._observers.clear()  # Clear observers, such as GUI in our case.

        # Reassign the observers after deepcopy
        self._observers = temporary_observers

        return new_one

    def bot_place(self):
        """
            Calls the bots whenever they need to play their moves
        """
        if self._turn == 1:
            self._player1.make_move()
        else:
            self._player2.make_move()

    def get_valid_locations(self):
        """
            Returns the indices of the columns that are not full, aka the column where
            the user can play his next move
        """
        free_cols = []
        for i in range(COLUMN_COUNT):
            if self._board[i][ROW_COUNT-1] == 0:
                free_cols.append(i)

        return free_cols

import numpy as np
import random
from observer import Observer
import tensorflow as tf
import math
from copy import copy, deepcopy
YELLOW_PLAYER = 1
RED_PLAYER = -1

PLAYERS = {1: "Yellow", -1: "Red"}

EMPTY = 0
ROW_COUNT = 6
COLUMN_COUNT = 7
WINDOW_LENGTH = 4

class Bot(Observer):

    def __init__(self, game, bot_type=None, model=None):
        self._game = game
        # Bot type determines how the bot picks his moves
        self._type = bot_type

        #print("Created bot of type " + str(self._type))
        self._model = None
        if model is not None:
            self._model = model

    def update(self, obj, event, *argv):
        print(obj)

    def drop_piece(self,board, row, col, piece):
        # print(col,row)
        board[col][row] = piece

    def get_next_open_row(self,board, col):
    	for r in range(ROW_COUNT):
            if board[col][r] == 0:
                return r

    def winning_move(self,board, piece):
            # Check horizontal locations for win
        for c in range(COLUMN_COUNT-3):
            for r in range(ROW_COUNT):
                if board[c][r] == piece and board[c+1][r] == piece and board[c+2][r] == piece and board[c+3][r] == piece:
                    # print("horizontal")
                    return True

        # Check vertical locations for win
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT-3):
                if board[c][r] == piece and board[c][r+1] == piece and board[c][r+2] == piece and board[c][r+3] == piece: 
                    # print("vertical")
                    return True

        # Check positively sloped diaganols
        for c in range(COLUMN_COUNT-3):
            for r in range(ROW_COUNT-3):
                if board[c][r] == piece and board[c+1][r+1] == piece and board[c+2][r+2] == piece and board[c+3][r+3] == piece:
                    # print("pdiago")
                    return True

        # Check negatively sloped diaganols
        for c in range(COLUMN_COUNT-3):
            for r in range(3, ROW_COUNT):
                if board[c][r] == piece and board[c+1][r-1] == piece and board[c+2][r-2] == piece and board[c+3][r-3] == piece:
                    # print("ndiago")
                    return True
        return False

    def is_terminal_node(self,board):
        # print(self.winning_move(board, self._game._turn*-1) or self.winning_move(board, self._game._turn ) or self.get_valid_locations() is None)
        return self.winning_move(board, self._game._turn*-1) or self.winning_move(board, self._game._turn ) or self.get_valid_locations() is None
    
    def evaluate_window(self,window, piece):
        score = 0
        opp_piece = self._game._turn*-1
        if piece == self._game._turn*-1:
            opp_piece = self._game._turn

        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(EMPTY) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(EMPTY) == 2:
            score += 2

        if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
            score -= 4

        return score
    def score_position(self,board, piece):
        score = 0
        ## Score center column
        center_array = [int(i) for i in list(board[COLUMN_COUNT//2][:])]
        center_count = center_array.count(piece)
        score += center_count * 3

        ## Score Horizontal
        for r in range(ROW_COUNT):
            row_array = [int(i) for i in list(board[:][r])]
            for c in range(COLUMN_COUNT-3):
                window = row_array[c:c+WINDOW_LENGTH]
                score += self.evaluate_window(window, piece)

        ## Score Vertical
        for c in range(COLUMN_COUNT):
            col_array = [int(i) for i in list(board[c][:])]
            for r in range(ROW_COUNT-3):
                window = col_array[r:r+WINDOW_LENGTH]
                score += self.evaluate_window(window, piece)

        ## Score posiive sloped diagonal
        for r in range(ROW_COUNT-3):
            for c in range(COLUMN_COUNT-3):
                window = [board[c+i][r+i] for i in range(WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece)

        for r in range(ROW_COUNT-3):
            for c in range(COLUMN_COUNT-3):
                window = [board[c+i][r+3-i] for i in range(WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece)

        return score

    def minimax(self,board, depth, alpha, beta, maximizingPlayer):
        valid_locations = self.get_valid_locations()
        is_terminal = self.is_terminal_node(board)
        if depth == 0 or is_terminal:
            if is_terminal:
                if self.winning_move(board, self._game._turn):
                    return (None, 100000000000000)
                elif self.winning_move(board, self._game._turn*-1):
                    return (None, -10000000000000)
                else: # Game is over, no more valid moves
                    return (None, 0)
            else: # Depth is zero
                return (None, self.score_position(board, self._game._turn))
        if maximizingPlayer:
            # print("depth ",depth)
            value = -math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = self.get_next_open_row(board, col)
                b_copy=[]
                for i in range (0,len(board)):
                    b_copy.append(board[i].copy())
                # b_copy = deepcopy(board)
                if(row is not None and col is not None):
                    self.drop_piece(b_copy, row, col, self._game._turn)
                new_score = self.minimax(b_copy, depth-1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value

        else: # Minimizing player
            value = math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = self.get_next_open_row(board, col)
                b_copy=[]
                for i in range (0,len(board)):
                    b_copy.append(board[i].copy())
                # b_copy = deepcopy(board)
                if(row is not None and col is not None):
                    self.drop_piece(b_copy, row, col, self._game._turn*-1)
                new_score = self.minimax(b_copy, depth-1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value

    def make_move(self):
        """
            Picks the column in which the bot should place the next disc.
            The considered moving options depend on the bot type.

            :return: the column number where the bot should play the next move
        """
        #print(PLAYERS[self._game._turn] + " is about to play :")
        column = None
        # In case the bot type is 0, the bot checks for winning moves, and if there aren't,
        # then picks a valid random move.
        if self._type == 0:
            win_col = self.get_winning_move()
            if win_col is not None:
                column = win_col
            else:
                column = self.get_random_move()
        # In case the bot type is 1, the bot checks for winning moves, and if there aren't,
        # then checks if there is any move that blocks a direct winning move for the opponent.
        # If there is no such move, it picks a valid random move.
        elif self._type == 1:
            win_col = self.get_winning_move()
            if win_col is not None:
                #print("Winning column :", win_col)
                column = win_col
            else:
                def_move = self.get_defensive_move()
                if def_move is not None:
                    #print("Defensive column :", def_move)
                    column = def_move
                else:
                    column = self.get_random_move()
                    #print("Random move", column)
        elif self._type == 2:
            column, minimax_score = self.minimax(self._game._board, 5, -math.inf, math.inf, True)
            # print(column)
        else:
            flat_board = [
                [item for sublist in self._game._board for item in sublist]]
            # print(flat_board)
            output = self._model.predict(flat_board)
            output = output[0]
            free_cols = []
            for i in range(len(self._game._board)):
                if self._game._board[i][self._game._rows-1] == 0:
                    free_cols.append(i)

            found = False
            while not found:
                column = np.argmax(output)
                if sum(output) == 0:
                    column = self.get_random_move()
                if column in free_cols:
                    found = True
                else:
                    output[column] = 0

        # print("-------------------------")
        self._game.place(column)

    def get_winning_move(self):
        """
            Checks whether there is a winning column available for the next
            move of the bot.

            :return: winning column
        """
        column = None
        for c_win in range(self._game._cols):
            for r in range(self._game._rows):
                if self._game._board[c_win][r] == 0:
                    self._game._board[c_win][r] = self._game._turn
                    is_winner = self._game.check_win((c_win, r))
                    self._game._board[c_win][r] = 0
                    if is_winner:
                        column = c_win
                        return column
                    break
        return column
    def get_valid_locations(self):
        free_cols = []
        for i in range(len(self._game._board)):
            if self._game._board[i][self._game._rows-1] == 0:
                free_cols.append(i)
        if len(free_cols) == 0:
            return None
        return free_cols

    def get_random_move(self):
        """
            Picks a valid random column where the bot can play his next move.

            :return: valid random column 
        """
        free_cols = self.get_valid_locations()
        column = random.choice(free_cols)
        return column

    def get_defensive_move(self):
        """
            Checks whether the bot could play a move that blocks a direct winning
            move from the opponent.

            :return: column to be played to avoid losing immediatly
        """
        column = None
        for c_win in range(self._game._cols):
            for r in range(self._game._rows):
                if self._game._board[c_win][r] == 0:
                    self._game._board[c_win][r] = -1*self._game._turn
                    is_winner = self._game.check_win((c_win, r))
                    self._game._board[c_win][r] = 0
                    if is_winner:
                        column = c_win
                        return column
                    break
        return column

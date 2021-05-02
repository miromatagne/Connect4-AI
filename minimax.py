from bot import Bot
import random
import math
from copy import copy, deepcopy
import numpy as np


EMPTY = 0
ROW_COUNT = 6
COLUMN_COUNT = 7
WINDOW_LENGTH = 4

MINIMAX = "MINIMAX"


class MiniMax(Bot):
    def __init__(self, game):
        super().__init__(game, bot_type=MINIMAX)

    def drop_piece(self, board, row, col, piece):
        # print(col, row)
        board[col][row] = piece

    def get_next_open_row(self, board, col):
        for r in range(ROW_COUNT):
            if board[col][r] == 0:
                return r

    def winning_move(self, board, piece):
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

    def is_terminal_node(self, board):
        # print(self.winning_move(board, self._game._turn*-1) or self.winning_move(board,
        #                                                                          self._game._turn) or self.get_valid_locations(board) is None)
        return self.winning_move(board, self._game._turn*-1) or self.winning_move(board, self._game._turn) or self.get_valid_locations(board) is None

    def evaluate_window(self, window, piece):
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

    def score_position(self, board, piece):
        score = 0
        # Score center column
        center_array = [int(i) for i in list(board[COLUMN_COUNT//2][:])]
        center_count = center_array.count(piece)
        score += center_count * 3

        # Score Horizontal
        for r in range(ROW_COUNT):
            row_array = [int(i) for i in list(board[:][r])]
            for c in range(COLUMN_COUNT-3):
                window = row_array[c:c+WINDOW_LENGTH]
                score += self.evaluate_window(window, piece)

        # Score Vertical
        for c in range(COLUMN_COUNT):
            col_array = [int(i) for i in list(board[c][:])]
            for r in range(ROW_COUNT-3):
                window = col_array[r:r+WINDOW_LENGTH]
                score += self.evaluate_window(window, piece)

        # Score posiive sloped diagonal
        for r in range(ROW_COUNT-3):
            for c in range(COLUMN_COUNT-3):
                window = [board[c+i][r+i] for i in range(WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece)

        for r in range(ROW_COUNT-3):
            for c in range(COLUMN_COUNT-3):
                window = [board[c+i][r+3-i] for i in range(WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece)

        return score

    def minimax(self, board, depth, alpha, beta, maximizingPlayer):
        valid_locations = self.get_valid_locations(board)
        is_terminal = self.is_terminal_node(board)

        if depth == 0 or is_terminal:
            if is_terminal:
                if self.winning_move(board, self._game._turn):
                    return (None, math.inf)
                elif self.winning_move(board, self._game._turn*-1):
                    return (None, -math.inf)
                else:  # Game is over, no more valid moves
                    # print("WHAT 3")
                    return (None, 0)
            else:  # Depth is zero
                # print("kaka")
                return (None, self.score_position(board, self._game._turn))
        elif maximizingPlayer:
            # print("depth ", depth)
            value = -math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = self.get_next_open_row(board, col)

                b_copy = []
                for i in range(0, len(board)):
                    b_copy.append(board[i].copy())
                # b_copy = deepcopy(board)
                # if(row is not None and col is not None):
                self.drop_piece(b_copy, row, col, self._game._turn)
                new_score = self.minimax(
                    b_copy, depth-1, alpha, beta, False)[1]
                # print(new_score)
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value

        else:  # Minimizing player
            value = math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = self.get_next_open_row(board, col)
                b_copy = []
                for i in range(0, len(board)):
                    b_copy.append(board[i].copy())
                # b_copy = deepcopy(board)
                # if(row is not None and col is not None):
                self.drop_piece(b_copy, row, col, self._game._turn*-1)
                new_score = self.minimax(b_copy, depth-1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value

import numpy as np
import random
from observer import Observer

YELLOW_PLAYER = 1
RED_PLAYER = -1

PLAYERS = {1: "Yellow", -1: "Red"}


class Bot(Observer):

    def __init__(self, game, bot_type):
        self._game = game
        self._type = bot_type
        print("Created bot of type " + str(self._type))

    def update(self, obj, event, *argv):
        print(obj)

    def make_move(self):
        print(PLAYERS[self._game._turn] + " is about to play :")
        column = None
        if self._type == 0:
            win_col = self.get_winning_move()
            if win_col is not None:
                column = win_col
            else:
                column = self.get_random_move()
        elif self._type == 1:
            win_col = self.get_winning_move()
            if win_col is not None:
                print("Winning column :", win_col)
                column = win_col
            else:
                def_move = self.get_defensive_move()
                if def_move is not None:
                    print("Defensive column :", def_move)
                    column = def_move
                else:
                    column = self.get_random_move()
                    print("Random move", column)

        #print("Play :", column)
        self._game.place(column)

    def get_winning_move(self):
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

    def get_random_move(self):
        free_cols = []
        for i in range(len(self._game._board)):
            if self._game._board[i][self._game._rows-1] == 0:
                free_cols.append(i)
        if len(free_cols) == 0:
            return None
        column = random.choice(free_cols)
        return column

    def get_defensive_move(self):
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

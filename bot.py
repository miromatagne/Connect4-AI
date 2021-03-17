import numpy as np
import random
from observer import Observer

class Bot(Observer):

    def __init__(self, game):
        self._game = game
        self._board = self._game._board
        self._cols = self._game._cols
        self._rows = self._game._rows
        self._round = self._game._round
        self._turn = self._game._turn
        self._won = self._game._won

    def update(self, obj, event, *argv):
        print(obj)

    def make_move(self):
        # if (self._game._round == 0):
        #     file_content = np.zeros((42, 7, 6))
        # else:
        #     file_content = np.load(self._game.winner_filename)

        # TODO : choose only between available columns
        column = random.randint(0, self._game._cols-1)
        while (self._game._board[column][self._game._rows-1] != 0):
            column = random.randint(0, self._game._cols-1)

        # Find winning column, if exists
        found = False
        for c_win in range(self._game._cols):
            for r in range(self._game._rows):
                if self._game._board[c_win][r] == 0:
                    self._game._board[c_win][r] = self._game._turn
                    is_winner = self._game.check_win((c_win, r))
                    self._game._board[c_win][r] = 0
                    if is_winner:
                        column = c_win
                        found = True
                        break
            if(found):
                break

        self._game.place(column)

        #file_content[self._round] = self._board
        #np.save(self._game.winner_filename, file_content)


import numpy as np
import random
from observer import Observer
import tensorflow as tf

YELLOW_PLAYER = 1
RED_PLAYER = -1

PLAYERS = {1: "Yellow", -1: "Red"}


class Bot(Observer):

    def __init__(self, game, bot_type):
        self._game = game
        # Bot type determines how the bot picks his moves
        self._type = bot_type

        #print("Created bot of type " + str(self._type))
        self._model = None
        if self._type == 2:
            self._model = self.load_model()

    def update(self, obj, event, *argv):
        print(obj)

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
            flat_board = [[item for sublist in self._game._board for item in sublist]]
            print(flat_board)
            output = self._model.predict(flat_board)
            output = output[0]
            free_cols = []
            for i in range(len(self._game._board)):
                if self._game._board[i][self._game._rows-1] == 0:
                    free_cols.append(i)

            found = False
            while not found:
                print(output)
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

    def get_random_move(self):
        """
            Picks a valid random column where the bot can play his next move.

            :return: valid random column 
        """
        free_cols = []
        for i in range(len(self._game._board)):
            if self._game._board[i][self._game._rows-1] == 0:
                free_cols.append(i)
        if len(free_cols) == 0:
            return None
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

    def load_model(self):
        model = tf.keras.models.load_model('./saved_model/my_model')
        #model.summary()
        return model
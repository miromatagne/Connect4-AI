import tensorflow as tf
from connect4game import Connect4Game
from connect4viewer import Connect4Viewer
import pygame

class Evaluation():

    def __init__(self, model_filename):
        self._model = tf.keras.models.load_model(model_filename)

    def evaluate_model(self, nb_rep, game_mode):
        """
            Evaluates the model by playing a certain amounts of games
            against a certain bot, and returns the percentage of games won.

            :param nb_rep: number of games
            :param game_mode: bot against who the model will play
            :return: percentage of games won
        """
        total_games_won = 0
        for i in range(nb_rep):
            game = Connect4Game(player1=None, player2=game_mode,
                                bot1_model=self._model)
            view = Connect4Viewer(game=game)
            view.initialize()
            running = True
            while running:
                if ((game._turn == 1) and (game.get_win() is None)):
                    game.bot_place()
                elif ((game._turn == -1) and (game.get_win() is None)):
                    game.bot_place()

                elif game.get_win() is not None:
                    if game.get_win() == 1:
                        total_games_won += 1
                        # print("won")
                        running = False
                    else:
                        # print("loss")
                        running = False
                pygame.time.wait(1000)
        percentage = (total_games_won/nb_rep)*100
        print("Won games : " + str(percentage) + "%")
        return percentage

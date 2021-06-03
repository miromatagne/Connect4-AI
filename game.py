import pygame
import pygame.gfxdraw
import numpy as np
import time
from observable import Observable
from observer import Observer
from bot import Bot
from file_recording import FileRecording
from model import Model
from evaluation import Evaluation
from connect4game import Connect4Game
from connect4viewer import Connect4Viewer
from event import Event
import time
import multiprocessing

SQUARE_SIZE = 100

MONTE_CARLO = "MONTE_CARLO"
MINIMAX = "MINIMAX"
RANDOM = "RANDOM"
RANDOM_IMPR = "RANDOM_IMPR"

"""
    One can run games of connect 4 between different types of bot and algorithms by giving as argument to the constructor
    Connect4Game the variables above.
"""

if __name__ == '__main__':
    nb_Games = 1
    total_games_won = 0
    total_games_won2 = 0
    # Change to True if one wants to play
    want_to_play = True

    for i in range(nb_Games):
        game = Connect4Game(MINIMAX, MONTE_CARLO, iteration=300, depth1=4)
        view = Connect4Viewer(game=game)
        view.initialize()

        running = True
        while running:
            if ((game._turn == 1) and (game.get_win() is None)):
                if not want_to_play:
                    game.bot_place()
                else:
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                            game.place(pygame.mouse.get_pos()
                                       [0] // SQUARE_SIZE)

            elif ((game._turn == -1) and (game.get_win() is None)):
                game.bot_place()
            elif game.get_win() is not None:
                if game.get_win() == 1:
                    total_games_won += 1
                    running = False
                elif game.get_win() == -1:
                    total_games_won2 += 1
                    running = False
                else:
                    running = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

    pygame.quit()

    if not want_to_play:
        print("Win rate of Minimax: ", 100 *
              (total_games_won/nb_Games), "%")  # Minimax
    else:
        print("You won with a win rate of: ",
              100*(total_games_won/nb_Games), "%")
    print("Win rate of Monte Carlo: ", 100 *
          (total_games_won2/nb_Games), "%")  # MonteCarlo

    # Uncomment the following lines to create and train a deep neural network model
    # f = FileRecording()
    # f.generate_training_set('./Game_History_MM_vs_MC/')

    # Uncomment the following lines to evaluate the model
    # nbOfGames = 100
    # evaluation = Evaluation("./model_Minmax_vs_MonteCarlo_3layers_no_duplicate")
    # percentage = evaluation.evaluate_model(nbOfGames, RANDOM_IMPR)
    # print(percentage)

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
from measurement import Measurement
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
    want_to_play = False

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
              (total_games_won/nb_Games), "%")
    else:
        print("You won with a win rate of: ",
              100*(total_games_won/nb_Games), "%")
    print("Win rate of Monte Carlo: ", 100 *
          (total_games_won2/nb_Games), "%")

    # Uncomment the following lines to create and train a deep neural network model
    # Note that in order to train the model, some games (preferable to have a large amount of games) have to be played first
    # in order to have a dataset used for the training and the evaluation.

    # f = FileRecording()
    # f.generate_training_set('./Game_History_MM_vs_MC/')

    # Uncomment the following lines to evaluate the model
    # nbOfGames = 100
    # evaluation = Evaluation("./model_Minmax_vs_MonteCarlo_3layers_no_duplicate")
    # percentage = evaluation.evaluate_model(nbOfGames, RANDOM_IMPR)
    # print(percentage)

    # Measurements: uncomment the following lines in order to run the tests performed discussed in the report.
    # Note that the following measures take a lot of time to run.

    # measurement = Measurement()

    # depths = [3, 4, 5, 6, 7]
    # iteration = [i for i in range(100, 999, 100)]

    # # Comparison for non pruning Minimax
    # arguments = []
    # for depth in depths:
    #     arguments.append(("Minimax_no_pruning_depth_"+str(depth)+".txt", 200, depth))

    # # multiprocessing
    # pool = multiprocessing.Pool()
    # start = time.perf_counter()
    # pool.starmap(measurement.comparison_pruning, arguments)
    # pool.close()
    # print(time.perf_counter() - start)

    # Comparison for pruning Minimax
    # arguments2 = []
    # for depth in depths:
    #     arguments2.append(("Minimax_depth_"+str(depth)+".txt", depth))

    # # multiprocessing
    # pool = multiprocessing.Pool()
    # start = time.perf_counter()
    # pool.starmap(comparison_of_MM, arguments2)
    # pool.close()

    # Measurement of the  Monte Carlo by varying the iteration parameter

    # arguments3 = []
    # for i in iteration:
    #     arguments3.append(("MonteCarlo_iter_"+str(i)+".txt", i))

    # multiprocessing
    # pool = multiprocessing.Pool()
    # start = time.perf_counter()
    # pool.starmap(comparison_of_MC, arguments3)
    # pool.close()
    # print(time.perf_counter() - start)

    # Comparison between Minimax and Monte Carlo based on the previous measurement

    # arguments4 = []
    # depth_iter = [[3, 20], [4, 100], [4, 300], [5, 350], [5,400], [5,700], [5,750], [5,800], [5,950], [5,1000], [6,1250],
    #                     [6,1300], [6,1500], [6,1750], [6,2000], [6,2250], [6,2500], [6,2750], [6,3000]]
    # for i in range(len(depth_iter)):
    #     arguments4.append(("d=" + str(depth_iter[i][0]) + "_iter=" + str(depth_iter[i][1]) + ".txt", depth_iter[i][1], depth_iter[i][0]))

    # # multiprocessing
    # pool = multiprocessing.Pool()
    # start = time.perf_counter()
    # pool.starmap(comparison, arguments4)
    # pool.close()
    # print(time.perf_counter() - start)

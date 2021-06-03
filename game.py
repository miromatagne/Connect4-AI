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


if __name__ == '__main__':
    total_games_won = 0
    total_games_won2 = 0
    start = time.perf_counter()
    for i in range(1):
        game = Connect4Game(MINIMAX, MONTE_CARLO, iteration=100, depth1=3)
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
                    running = False
                elif game.get_win() == -1:
                    total_games_won2 += 1
                    running = False
                else:
                    running = False

            # for event in pygame.event.get():
            #     if event.type == pygame.QUIT:
            #         running = False
            #     if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            #         if game.get_win() is None:
            #             game.place(pygame.mouse.get_pos()
            #                        [0] // SQUARE_SIZE)
            #         else:
            #             game.reset_game()
    # pygame.quit()

    # print(total_games_won/10)  # Minimax
    # print(total_games_won2/10)  # MonteCarlo

    # Evaluation of the model
    # nbOfGames = 100
    # evaluation = Evaluation("./model_Minmax_vs_MonteCarlo_3layers_no_duplicate")
    # percentage = evaluation.evaluate_model(nbOfGames, RANDOM_IMPR)
    # print(percentage)


    # f = FileRecording()
    # f.generate_training_set('./Game_History_MM_vs_MC/')

    
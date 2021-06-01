import pygame
import pygame.gfxdraw
import random
import enum
from copy import deepcopy
import uuid
import numpy as np
import time
from observable import Observable
from observer import Observer
from bot import Bot
from file_recording import FileRecording
from training import Training
from model import Model
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


# Measures
def comparison(filename, iteration, depth):
    nbOfGames = 400
    f = open(filename, 'w')
    f.write("\n"+str(nbOfGames) + " games\n" + "iteration of MonteCarlo=" +
            str(iteration) + " depth of Minimax="+str(depth)+"\n")
    f.write("Accuracy , Average time per game , Average max time per move , Accuracy , Average time per game , Average max time per move\n")
    total_games_won = 0
    total_games_won2 = 0
    time_single_moveMin_list = []
    time_single_moveMC_list = []
    max_time_move_MC = 0
    max_time_move_Min = 0
    start = time.perf_counter()
    for i in range(nbOfGames):
        game = Connect4Game(MINIMAX, MONTE_CARLO,
                            iteration=iteration, depth1=depth)
        running = True
        while running:
            if ((game._turn == 1) and (game.get_win() is None)):
                start_single_moveMin = time.perf_counter()
                game.bot_place()
                chronometer_single_moveMin = time.perf_counter() - start_single_moveMin
                time_single_moveMin_list.append(chronometer_single_moveMin)
                # counter_Min += 1
            elif ((game._turn == -1) and (game.get_win() is None)):
                start_single_moveMC = time.perf_counter()
                game.bot_place()
                chronometer_single_moveMC = time.perf_counter() - start_single_moveMC
                time_single_moveMC_list.append(chronometer_single_moveMC)
                # counter_MC += 1
            elif game.get_win() is not None:
                if game.get_win() == 1:
                    total_games_won += 1
                    running = False
                elif game.get_win() == -1:
                    total_games_won2 += 1
                    running = False
                else:
                    running = False
        max_time_move_MC += max(time_single_moveMC_list)
        max_time_move_Min += max(time_single_moveMin_list)

    chronometer = time.perf_counter() - start
    percentage_min = (total_games_won/nbOfGames)*100
    percentage_mc = (total_games_won2/nbOfGames)*100
    average_time = chronometer/nbOfGames
    average_time_single_moveMin = max_time_move_Min/nbOfGames
    average_time_single_moveMC = max_time_move_MC/nbOfGames
    f.write("        %.2f ,        %.3f ,        %.3f," %
            (percentage_mc, average_time, average_time_single_moveMC))
    f.write("        %.2f ,        %.3f ,        %.3f\n" %
            (percentage_min, average_time, average_time_single_moveMin))


def comparison_of_MC(filename, iteration):
    nbOfGames = 100
    f = open(filename, 'w')
    f.write("\n"+str(nbOfGames) + " games\n" +
            "iteration of MonteCarlo="+str(iteration)+"\n")
    total_games_won = 0
    total_games_won2 = 0
    time_single_moveMin_list = []
    time_single_moveMC_list = []
    max_time_move_MC = 0
    max_time_move_Min = 0
    start = time.perf_counter()
    for i in range(nbOfGames):
        game = Connect4Game(MINIMAX, MONTE_CARLO,
                            iteration=iteration, depth1=7)
        running = True
        while running:
            if ((game._turn == 1) and (game.get_win() is None)):
                start_single_moveMin = time.perf_counter()
                game.bot_place()
                chronometer_single_moveMin = time.perf_counter() - start_single_moveMin
                time_single_moveMin_list.append(chronometer_single_moveMin)
                # counter_Min += 1
            elif ((game._turn == -1) and (game.get_win() is None)):
                start_single_moveMC = time.perf_counter()
                game.bot_place()
                chronometer_single_moveMC = time.perf_counter() - start_single_moveMC
                time_single_moveMC_list.append(chronometer_single_moveMC)
                # counter_MC += 1
            elif game.get_win() is not None:
                if game.get_win() == 1:
                    total_games_won += 1
                    running = False
                elif game.get_win() == -1:
                    total_games_won2 += 1
                    running = False
                else:
                    running = False
        max_time_move_MC += max(time_single_moveMC_list)
        max_time_move_Min += max(time_single_moveMin_list)

    chronometer = time.perf_counter() - start
    percentage_min = (total_games_won/nbOfGames)*100  # minimax 7
    percentage_mc = (total_games_won2/nbOfGames)*100
    average_time = chronometer/nbOfGames
    average_time_single_moveMin = max_time_move_Min/nbOfGames
    average_time_single_moveMC = max_time_move_MC/nbOfGames
    f.write(
        "Minimax Accuracy , Average time per game , Average max time for single move\n")
    f.write("        %.2f ,        %.3f ,        %.3f\n" %
            (percentage_min, average_time, average_time_single_moveMin))
    f.write("MonteCarlo Accuracy , Average time per game , Average max time for single move  (param of MonteCarlo: explo=2.0)\n")
    f.write("        %.2f ,        %.3f ,        %.3f\n" %
            (percentage_mc, average_time, average_time_single_moveMC))


def comparison_of_MM(filename, depth):
    nbOfGames = 100
    f = open(filename, 'w')
    f.write("\n"+str(nbOfGames) + " games\n" +
            "iteration of Minimax="+str(depth)+"\n")
    total_games_won = 0
    total_games_won2 = 0
    time_single_moveMin_list = []
    time_single_moveennemy_list = []
    max_time_move_ennemy = 0
    max_time_move_Min = 0
    start = time.perf_counter()
    for i in range(nbOfGames):
        game = Connect4Game(MINIMAX, MINIMAX, depth1=depth, depth2=7)
        running = True
        while running:
            if ((game._turn == 1) and (game.get_win() is None)):
                start_single_moveMin = time.perf_counter()
                game.bot_place()
                chronometer_single_moveMin = time.perf_counter() - start_single_moveMin
                time_single_moveMin_list.append(chronometer_single_moveMin)

            elif ((game._turn == -1) and (game.get_win() is None)):
                start_single_moveennemy = time.perf_counter()
                game.bot_place()
                chronometer_single_moveennemy = time.perf_counter() - start_single_moveennemy
                time_single_moveennemy_list.append(
                    chronometer_single_moveennemy)

            elif game.get_win() is not None:
                if game.get_win() == 1:
                    total_games_won += 1
                    running = False
                elif game.get_win() == -1:
                    total_games_won2 += 1
                    running = False
                else:
                    running = False
        max_time_move_ennemy += max(time_single_moveennemy_list)
        max_time_move_Min += max(time_single_moveMin_list)

    chronometer = time.perf_counter() - start
    percentage_min = (total_games_won/nbOfGames)*100
    percentage_ennemy = (total_games_won2/nbOfGames)*100  # minimax 7
    average_time = chronometer/nbOfGames
    average_time_single_moveMin = max_time_move_Min/nbOfGames
    average_time_single_moveennemy = max_time_move_ennemy/nbOfGames
    f.write(
        "Minimax Accuracy , Average time per game , Average max time for single move\n")
    f.write("        %.2f ,        %.3f ,        %.3f\n" %
            (percentage_min, average_time, average_time_single_moveMin))
    f.write("Ennemy Accuracy , Average time per game , Average max time for single move (Minimax depth=7)\n")
    f.write("        %.2f ,        %.3f ,        %.3f\n" %
            (percentage_ennemy, average_time, average_time_single_moveennemy))


if __name__ == '__main__':
    total_games_won = 0
    total_games_won2 = 0
    start = time.perf_counter()
    for i in range(10):
        game = Connect4Game(MINIMAX, MONTE_CARLO, iteration=500, depth1=6)
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
    # chronometer = time.perf_counter() - start
    #         # pygame.time.wait(1000)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if game.get_win() is None:
                        game.place(pygame.mouse.get_pos()
                                   [0] // SQUARE_SIZE)
                    else:
                        game.reset_game()
    #     counter += 1
    #     print(counter)
    # pygame.quit()

    # nbOfGames = 100
    # model = Model("./model_Minmax_vs_MonteCarlo_3layers_no_duplicate")
    # # # # model = Model("./saved_model/my_model")
    # percentage = model.evaluate_model(nbOfGames, RANDOM_IMPR)
    # print(percentage)

    print(total_games_won/10)  # Minimax
    print(total_games_won2/10)  # MonteCarlo
    print(chronometer/10)

    # f = FileRecording()
    # f.generate_training_set()

    # nbOfGames = 50
    # # algorithms = [MINIMAX, MONTE_CARLO]
    # # f = open("Measures_Minimax_VS_MonteCarlo.txt", 'a')
    # # f.write("\n"+str(nbOfGames) +" games\n" + "iteration of MonteCarlo=3000 and depth of minimax=7\n")
    # # # for algo in algorithms:
    # total_games_won = 0
    # total_games_won2 = 0
    # counter_Min = 0
    # counter_MC = 0
    # average_time_single_moveMin = 0
    # average_time_single_moveMC = 0
    # start = time.perf_counter()
    # for i in range(nbOfGames):
    #     game = Connect4Game(MINIMAX, MONTE_CARLO, iteration=90, depth1=4)
    #     # view = Connect4Viewer(game=game)
    #     # view.initialize()
    #     running = True
    #     while running:
    #         if ((game._turn == 1) and (game.get_win() is None)):
    #             start_single_moveMin = time.perf_counter()
    #     game.bot_place()
    #     chronometer_single_moveMin = time.perf_counter() - start_single_moveMin
    #     average_time_single_moveMin += chronometer_single_moveMin
    #     counter_Min += 1
    # elif ((game._turn == -1) and (game.get_win() is None)):
    #     start_single_moveMC = time.perf_counter()
    #     game.bot_place()
    #     chronometer_single_moveMC = time.perf_counter() - start_single_moveMC
    #     average_time_single_moveMC += chronometer_single_moveMC
    #     counter_MC += 1

    # elif game.get_win() is not None:
    #     if game.get_win() == 1:
    #         total_games_won += 1
    #         running = False
    #     elif game.get_win() == -1:
    #         total_games_won2 += 1
    #         running = False
    #     else:
    #         running = False

    # pygame.time.wait(500)

    #         # for event in pygame.event.get():
    #         #     if event.type == pygame.QUIT:
    #         #         running = False
    #         #     if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
    #         #         if game.get_win() is None:
    #         #             game.place(pygame.mouse.get_pos()[0] // SQUARE_SIZE)
    #         #         else:
    #         #             game.reset_game()

    # chronometer = time.perf_counter() - start
    # percentage_min = (total_games_won/nbOfGames)*100
    # percentage_mc = (total_games_won2/nbOfGames)*100
    # average_time = chronometer/nbOfGames
    # average_time_single_moveMin /= counter_Min
    # average_time_single_moveMC /= counter_MC
    # f.write("Minimax Accuracy , Average time per game , Average time , for single move\n")
    # f.write("        %.2f ,        %.3f ,        %.3f\n" %(percentage_min, average_time, average_time_single_moveMin))
    # f.write("MonteCarlo Accuracy , Average time per game , Average time , for single move  (param of MonteCarlo: explo=2.0)\n")
    # f.write("        %.2f ,        %.3f ,        %.3f\n" %(percentage_mc, average_time, average_time_single_moveMC))
    # print(average_time_single_moveMC, average_time_single_moveMin)
    # print(percentage_mc)

    # depths = [3, 4, 5, 6]
    # iteration = [i for i in range(100, 999, 100)]
    # arguments = []

    # for i in iteration:
    #     arguments.append(("MonteCarlo_iter_"+str(i)+".txt", i))

    # # # multiprocessing
    # pool = multiprocessing.Pool()
    # start = time.perf_counter()
    # pool.starmap(comparison_of_MC, arguments)
    # pool.close()
    # print(time.perf_counter() - start)

    # arguments2 = []
    # for depth in depths:
    #     arguments2.append(("Minimax_depth_"+str(depth)+".txt", depth))
    # comparison_of_MM("Minimax_depth_7.txt", 7)
    # # multiprocessing
    # pool = multiprocessing.Pool()
    # start = time.perf_counter()
    # pool.starmap(comparison_of_MM, arguments2)
    # pool.close()
    # print(time.perf_counter() - start)
    # arguments = []
    # depth_iter = [[3, 20], [4, 100], [4, 300], [5, 350], [5,400], [5,700], [5,750], [5,800], [5,950], [5,1000], [6,1250],
    #                     [6,1300], [6,1500], [6,1750], [6,2000], [6,2250], [6,2500], [6,2750], [6,3000]]
    # for i in range(len(depth_iter)):
    #     arguments.append(("d=" + str(depth_iter[i][0]) + "_iter=" + str(depth_iter[i][1]) + ".txt", depth_iter[i][1], depth_iter[i][0]))

    # # multiprocessing
    # pool = multiprocessing.Pool()
    # start = time.perf_counter()
    # pool.starmap(comparison, arguments)
    # pool.close()
    # print(time.perf_counter() - start)

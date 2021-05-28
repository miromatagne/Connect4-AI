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


### Measures
def comparison(filename, iteration, depths):
    nbOfGames = 200
    f = open(filename, 'w')
    f.write("\n"+str(nbOfGames) +" games\n" + "iteration of MonteCarlo="+str(iteration)+"\n")
    for depth in depths:
        total_games_won = 0
        total_games_won2 = 0
        counter_Min = 0
        counter_MC = 0
        average_time_single_moveMin = 0
        average_time_single_moveMC = 0
        start = time.perf_counter()
        for i in range(nbOfGames):
            game = Connect4Game(MINIMAX, MONTE_CARLO, iteration=iteration, depth=depth)
            running = True
            while running:
                if ((game._turn == 1) and (game.get_win() is None)):
                    start_single_moveMin = time.perf_counter()
                    game.bot_place()
                    chronometer_single_moveMin = time.perf_counter() - start_single_moveMin
                    average_time_single_moveMin += chronometer_single_moveMin
                    counter_Min += 1 
                elif ((game._turn == -1) and (game.get_win() is None)):
                    start_single_moveMC = time.perf_counter()
                    game.bot_place()
                    chronometer_single_moveMC = time.perf_counter() - start_single_moveMC
                    average_time_single_moveMC += chronometer_single_moveMC
                    counter_MC += 1 

                elif game.get_win() is not None:
                    if game.get_win() == 1:
                        total_games_won += 1
                        running = False
                    elif game.get_win() == -1:
                        total_games_won2 += 1
                        running = False
                    else:
                        running = False

        chronometer = time.perf_counter() - start
        percentage_min = (total_games_won/nbOfGames)*100
        percentage_mc = (total_games_won2/nbOfGames)*100
        average_time = chronometer/nbOfGames
        average_time_single_moveMin /= counter_Min
        average_time_single_moveMC /= counter_MC
        f.write("depth="+str(depth)+"\n")
        f.write("Minimax Accuracy , Average time per game , Average time , for single move\n")
        f.write("        %.2f ,        %.3f ,        %.3f\n" %(percentage_min, average_time, average_time_single_moveMin))
        f.write("MonteCarlo Accuracy , Average time per game , Average time , for single move  (param of MonteCarlo: explo=2.0)\n")
        f.write("        %.2f ,        %.3f ,        %.3f\n" %(percentage_mc, average_time, average_time_single_moveMC))


def comparison_of_MC(filename, iteration):
    nbOfGames = 10
    # f = open(filename, 'w')
    # f.write("\n"+str(nbOfGames) +" games\n" + "iteration of MonteCarlo="+str(iteration)+"\n")
    total_games_won = 0
    total_games_won2 = 0
    time_single_moveMin_list = []
    time_single_moveMC_list = []
    max_time_move_MC = 0
    max_time_move_Min = 0
    start = time.perf_counter()
    for i in range(nbOfGames):
        game = Connect4Game(MINIMAX, MONTE_CARLO, iteration=iteration, depth1=7)
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
    percentage_min = (total_games_won/nbOfGames)*100  #minimax 7
    percentage_mc = (total_games_won2/nbOfGames)*100
    average_time = chronometer/nbOfGames
    average_time_single_moveMin = max_time_move_Min/nbOfGames
    average_time_single_moveMC = max_time_move_MC/nbOfGames
    # f.write("Minimax Accuracy , Average time per game , Average max time for single move\n")
    # f.write("        %.2f ,        %.3f ,        %.3f\n" %(percentage_min, average_time, average_time_single_moveMin))
    # f.write("MonteCarlo Accuracy , Average time per game , Average max time for single move  (param of MonteCarlo: explo=2.0)\n")
    # f.write("        %.2f ,        %.3f ,        %.3f\n" %(percentage_mc, average_time, average_time_single_moveMC))
    print("Minimax Accuracy , Average time per game , Average max time for single move")
    print("        %.2f ,        %.3f ,        %.3f\n" %(percentage_min, average_time, average_time_single_moveMin))
    print("MonteCarlo Accuracy , Average time per game , Average max time for single move")
    print("        %.2f ,        %.3f ,        %.3f\n" %(percentage_mc, average_time, average_time_single_moveMC))

def comparison_of_MM(filename, depth):
    nbOfGames = 2
    f = open(filename, 'w')
    f.write("\n"+str(nbOfGames) +" games\n" + "iteration of Minimax="+str(depth)+"\n")
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
                print("ME")
                start_single_moveMin = time.perf_counter()
                game.bot_place()
                chronometer_single_moveMin = time.perf_counter() - start_single_moveMin
                time_single_moveMin_list.append(chronometer_single_moveMin)
                
            elif ((game._turn == -1) and (game.get_win() is None)):
                start_single_moveennemy = time.perf_counter()
                game.bot_place()
                chronometer_single_moveennemy = time.perf_counter() - start_single_moveennemy
                time_single_moveennemy_list.append(chronometer_single_moveennemy)

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
    percentage_ennemy = (total_games_won2/nbOfGames)*100 #minimax 7
    average_time = chronometer/nbOfGames
    average_time_single_moveMin = max_time_move_Min/nbOfGames
    average_time_single_moveennemy = max_time_move_ennemy/nbOfGames
    f.write("Minimax Accuracy , Average time per game , Average max time for single move\n")
    f.write("        %.2f ,        %.3f ,        %.3f\n" %(percentage_min, average_time, average_time_single_moveMin))
    f.write("Ennemy Accuracy , Average time per game , Average max time for single move (Minimax depth=7)\n")
    f.write("        %.2f ,        %.3f ,        %.3f\n" %(percentage_ennemy, average_time, average_time_single_moveennemy))


if __name__ == '__main__':
    # for i in range(2):
    #     game = Connect4Game(3, 0)
    #     view = Connect4Viewer(game=game)
    #     view.initialize()

    #     running = True
    #     while running:
    #         if ((game._turn == 1) and (game.get_win() is None)):
    #             game.bot_place()
    #         elif ((game._turn == -1) and (game.get_win() is None)):
    #             game.bot_place()
    #         elif game.get_win() is not None:
    #             running = False

    #         pygame.time.wait(1000)

    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 running = False
    #             if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
    #                 if game.get_win() is None:
    #                     game.place(pygame.mouse.get_pos()[0] // SQUARE_SIZE)
    #                 else:
    #                     game.reset_game()

    # pygame.quit()

    # nbOfGames = 500
    # model = Model("./model_better_bot_type2_4layersbis")
    # # # model = Model("./saved_model/my_model")
    # percentage = model.evaluate_model(nbOfGames, RANDOM_IMPR)
    # print(percentage)
    # f = open("Measures.txt", 'a')
    # f.write("\nmodel better bot type 2 4layers bis VS random improvement (number of games = %d)" %nbOfGames)
    # f.write("\n%.2f" % percentage)
    # f.close()

    
    # f = FileRecording()
    # f.generate_training_set()



    

    # nbOfGames = 2
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
    #     game = Connect4Game(MINIMAX, MONTE_CARLO, iteration=3000, depth1=6)
    #     # view = Connect4Viewer(game=game)
    #     # view.initialize()
    #     running = True
    #     while running:
    #         if ((game._turn == 1) and (game.get_win() is None)):
    #             start_single_moveMin = time.perf_counter()
    #             game.bot_place()
    #             chronometer_single_moveMin = time.perf_counter() - start_single_moveMin
    #             average_time_single_moveMin += chronometer_single_moveMin
    #             counter_Min += 1 
    #         elif ((game._turn == -1) and (game.get_win() is None)):
    #             start_single_moveMC = time.perf_counter()
    #             game.bot_place()
    #             chronometer_single_moveMC = time.perf_counter() - start_single_moveMC
    #             average_time_single_moveMC += chronometer_single_moveMC
    #             counter_MC += 1 

    #         elif game.get_win() is not None:
    #             if game.get_win() == 1:
    #                 total_games_won += 1
    #                 running = False
    #             elif game.get_win() == -1:
    #                 total_games_won2 += 1
    #                 running = False
    #             else:
    #                 running = False

    #         # pygame.time.wait(500)

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
    # print(chronometer)
    # print(percentage_min)


    depths = [3, 4, 5, 6]
    iteration = [i for i in range(250, 3001, 250)]
    arguments = []
    # for i in iteration:
    #     arguments.append(("MmvsMc_iter_"+str(i)+".txt", i, depth))
    
    # for i in iteration:
    #     arguments.append(("MonteCarlo_iter_"+str(i)+".txt", i))

    # # # multiprocessing
    # pool = multiprocessing.Pool()
    # start = time.perf_counter()   
    # pool.starmap(comparison_of_MC, arguments)
    # pool.close()
    # print(time.perf_counter() - start)
    comparison_of_MC("a.txt", 250)

    arguments2 = []
    for depth in depths:
        arguments2.append(("Minimax_depth_"+str(depth)+".txt", depth))
    
    # # multiprocessing
    # pool = multiprocessing.Pool()
    # start = time.perf_counter()   
    # pool.starmap(comparison_of_MM, arguments2)
    # pool.close()
    # print(time.perf_counter() - start)


import time
from connect4game import Connect4Game
import multiprocessing

class Measurement():
    def __init__(self):
        self._MONTE_CARLO = "MONTE_CARLO"
        self._MINIMAX = "MINIMAX"
        self._RANDOM = "RANDOM"
        self._RANDOM_IMPR = "RANDOM_IMPR"
        pass


    def comparison(self, filename, nbOfGames, iteration, depth):
        """
            Compute the win rate, average execution time per game and average maximum execution time per move for each algorithm
            resulting from their games.
            Write the results in the given file.

            :param filename: file to be written
            :param iteration: iteration parameter used for the Monte Carlo algorithm
            :param depth: depth parameter used for the Minima algorithm
        """
        # nbOfGames = 4000
        # f = open(filename, 'w')
        # f.write("\n"+str(nbOfGames) + " games\n" + "iteration of MonteCarlo=" +
        #         str(iteration) + " depth of Minimax="+str(depth)+"\n")
        # f.write("Accuracy , Average time per game , Average max time per move , Accuracy , Average time per game , Average max time per move\n")
        total_games_won = 0
        total_games_won2 = 0
        time_single_moveMin_list = []
        time_single_moveMC_list = []
        max_time_move_MC = 0
        max_time_move_Min = 0
        start = time.perf_counter()
        for i in range(nbOfGames):
            game = Connect4Game(self._MINIMAX, self._MONTE_CARLO,
                                iteration=iteration, depth1=depth)
            running = True
            while running:
                if ((game._turn == 1) and (game.get_win() is None)):
                    start_single_moveMin = time.perf_counter()
                    game.bot_place()
                    chronometer_single_moveMin = time.perf_counter() - start_single_moveMin
                    time_single_moveMin_list.append(chronometer_single_moveMin)
                elif ((game._turn == -1) and (game.get_win() is None)):
                    start_single_moveMC = time.perf_counter()
                    game.bot_place()
                    chronometer_single_moveMC = time.perf_counter() - start_single_moveMC
                    time_single_moveMC_list.append(chronometer_single_moveMC)
                elif game.get_win() is not None:
                    if game.get_win() == 1:
                        total_games_won += 1
                        running = False
                    elif game.get_win() == -1:
                        total_games_won2 += 1
                        running = False
                    else:
                        running = False
            # max_time_move_MC += max(time_single_moveMC_list)
            # max_time_move_Min += max(time_single_moveMin_list)

        # chronometer = time.perf_counter() - start
        # percentage_min = (total_games_won/nbOfGames)*100
        # percentage_mc = (total_games_won2/nbOfGames)*100
        # average_time = chronometer/nbOfGames
        # average_time_single_moveMin = max_time_move_Min/nbOfGames
        # average_time_single_moveMC = max_time_move_MC/nbOfGames
        # f.write("        %.2f ,        %.3f ,        %.3f," %
        #         (percentage_mc, average_time, average_time_single_moveMC))
        # f.write("        %.2f ,        %.3f ,        %.3f\n" %
        #         (percentage_min, average_time, average_time_single_moveMin))


    def comparison_of_MC(self, filename, iteration):
        """
            Compute the win rate, average execution time per game and average maximum execution time per move for each algorithm
            resulting from their games.
            Write the results in the given file.

            :param filename: file to be written
            :param iteration: iteration parameter used for the Monte Carlo algorithm
        """
        nbOfGames = 1
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
            game = Connect4Game(self._MINIMAX, self._MONTE_CARLO,
                                iteration=iteration, depth1=7)
            running = True
            while running:
                if ((game._turn == 1) and (game.get_win() is None)):
                    start_single_moveMin = time.perf_counter()
                    game.bot_place()
                    chronometer_single_moveMin = time.perf_counter() - start_single_moveMin
                    time_single_moveMin_list.append(chronometer_single_moveMin)
                elif ((game._turn == -1) and (game.get_win() is None)):
                    start_single_moveMC = time.perf_counter()
                    game.bot_place()
                    chronometer_single_moveMC = time.perf_counter() - start_single_moveMC
                    time_single_moveMC_list.append(chronometer_single_moveMC)
                    print(chronometer_single_moveMC)
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
            print(max_time_move_MC)
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
        print(chronometer)


    def comparison_of_MM(self, filename, depth):
        """
            Compute the win rate, average execution time per game and average maximum execution time per move for each algorithm
            resulting from their games.
            Write the results in the given file.

            :param filename: file to be written
            :param depth: depth parameter used for the Minima algorithm
        """
        nbOfGames = 5
        f = open(filename, 'w')
        f.write("\n"+str(nbOfGames) + " games\n" +
                "iteration of Minimax="+str(depth)+"\n")
        total_games_won = 0
        total_games_won2 = 0
        time_single_moveMin_list = []
        time_single_moveennemy_list = []
        max_time_move_ennemy = 0
        max_time_move_Min = 0
        start = time.process_time()
        for i in range(nbOfGames):
            game = Connect4Game(self._MINIMAX, self._MINIMAX, depth1=depth, depth2=7)
            running = True
            while running:
                if ((game._turn == 1) and (game.get_win() is None)):
                    start_single_moveMin = time.process_time()
                    game.bot_place()
                    chronometer_single_moveMin = time.process_time() - start_single_moveMin
                    time_single_moveMin_list.append(chronometer_single_moveMin)

                elif ((game._turn == -1) and (game.get_win() is None)):
                    start_single_moveennemy = time.process_time()
                    game.bot_place()
                    chronometer_single_moveennemy = time.process_time() - start_single_moveennemy
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


    def comparison_pruning(self, filename, nbOfGames, depth):
        """
            Compute the win rate, average execution time per game and average maximum execution time per move for each algorithm
            resulting from the given number of games.
            Write the results in the given file.

            :param filename: file to be written
            :param nbOfGames: number of games to be played
            :param depth: depth parameter used for the Minima algorithm
        """
        f = open(filename, 'w')
        f.write(str(nbOfGames) + " games\n")
        total_games_won = 0
        total_games_won2 = 0
        time_single_moveMin_list = []
        time_single_moveennemy_list = []
        max_time_move_ennemy = 0
        max_time_move_Min = 0
        start = time.perf_counter()
        for i in range(nbOfGames):
            game = Connect4Game(self._MINIMAX, self._MINIMAX, depth1=depth, depth2=7, pruning1=False, pruning2=True)
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
            "Minimax Acc , Av time per game , Av max time for single move , Ennemy Acc , Av time per game , Av max time for single move (Minimax depth=7)\n")
        f.write("        %.2f ,        %.3f ,        %.3f ,        %.2f ,        %.3f ,        %.3f\n" %
                (percentage_min, average_time, average_time_single_moveMin, percentage_ennemy, average_time, average_time_single_moveennemy))
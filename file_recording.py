import numpy as np
import uuid
import os
import math
from model import Model

class FileRecording():

    def __init__(self, unique_name=None):
        """
            Constructor of the FileRecording class.

            :param unique_name: file name of corresponding saved game
        """
        if unique_name == None:
            unique_name = str(uuid.uuid4())
        
        self.winning_moves_filename = './Winning_Moves/' + unique_name + '.npy'
        self.history_filename = './Game_History/' + unique_name + '.npy'
        self.file_content = np.zeros((42, 7, 6))
    
    def write_to_history(self, round_nb, board):
        """
            Add board to the file content and save the file.

            :param round_nb: corresponding round of the given board
            :param board: board to save in the file
        """
        self.file_content[round_nb] = board
        np.save(self.history_filename, self.file_content)

    def write_to_winning_moves(self,started, turn, moves):
        """
            Save file containing the winning moves, the turn and the information whether the winner 
            was the starter of the game.

            :param started: indicate whether the winner has started the game
            :param turn: indicate who is the winner
            :param moves: the moves played by the winner
        """
        arr = np.array([started, turn, moves], dtype="object")
        np.save(self.winning_moves_filename, arr)

    def read_history_file(self,file_name):
        """
            Load the given file containing a game from the game history folder.

            :param file_name: file to be loaded
            :return: game stored in the given file
        """
        folder = './Game_History/'
        current_game = np.load(folder + file_name)
        return current_game

    def read_winning_file(self, file_name):
        """
            Load the given file containing winning moves from the winning moves folder.

            :param file_name: file containing winning moves to be loaded
            :return: winner, 1 if he started, otherwise 0 and his winning moves
        """
        folder = './Winning_Moves/'
        current_game = np.load(folder + file_name,allow_pickle=True)
        started = current_game[0]
        turn = current_game[1]
        moves = current_game[2]
        return started, turn, moves

    def read_file(self, file_name):
        """
            Load the given file from the winning moves folder and the game history folder.
            Keep the boards of the winner and discard the empty boards.
            Encode the winning moves.

            :param file_name: file to be loaded
            :return: winner boards, winner moves encoded, round where the last move is played
        """
        started, turn, moves = self.read_winning_file(file_name)
        current_game = self.read_history_file(file_name)   # current_game.shape = (42, 7, 6)
        winner_boards = np.zeros((21, 7, 6))
        last_round = 0

        if started == 0: #The winner did not start the game
            winner_boards[:len(current_game),:,:] = current_game[::2,:,:]
        else: #The winner started the game
            winner_boards[:len(current_game),:,:] = current_game[1::2,:,:]
        if turn == -1: #Ensure that winner pieces are set to 1
            winner_boards *= -1
        #Detect the last board of the current game 
        for round in range(1, winner_boards.shape[0]):  #Skip first round
            current_board = np.all(winner_boards[round] == 0)
            if current_board:
                last_round = round #Round where the last coin is placed
                break

        encoding = []
        for i in range(7):
            row = []
            for j in range(i):
                row.append(0)
            row.append(1)
            
            for j in range(6-i):
                row.append(0)    
            encoding.append(row)
        encoded_moves = [encoding[moves[i]] for i in range(len(moves))]
        #Return only the relevant arrays
        return winner_boards[:last_round], encoded_moves[:last_round], last_round
        
    def generate_training_set(self, game_history_folder):
        """
            Read the files from the winning moves folder and the game history folder by the read_file function.
            Creating input samples by concatenating the winner boards of each game and by discarding the duplicate games.
            Creating output sample by concatenating the winning moves of each game and by discarding the duplicate games.
            Create a deep neural network model and train it based on the input and output samples generated.
            Save and evaluate the deep NN model. 

            :param game_history_folder: folder of games history to load the contained files
        """
        history_games = os.listdir(game_history_folder)
        input_samples = np.zeros((len(history_games)*21, 7, 6))
        output_samples = np.zeros((len(history_games)*21, 7))
        total_rounds = 0
        
        for g in range(len(history_games)):
            winner_boards, encoded_moves, last_round = self.read_file(history_games[g]) 

            if last_round != 0:
                nb_of_boards = len(winner_boards)
                for i in range(math.floor(len(input_samples)/nb_of_boards)):
                    comparison = input_samples[i*nb_of_boards:(i+1)*nb_of_boards] == winner_boards
                    duplicate = comparison.all()
                    if duplicate:
                        break

            if last_round != 0 and not duplicate:
                input_samples[total_rounds:total_rounds + last_round] = winner_boards
                output_samples[total_rounds:total_rounds + last_round] = encoded_moves  
            if not duplicate:
                total_rounds += last_round
                
        input_samples = input_samples[:total_rounds]
        output_samples = output_samples[:total_rounds]

        #Create and train a deep NN model
        test_split = 0.2
        model = Model()
        #Create the neural network model
        model.create_NN()
        #Split the data 
        train_input_data, train_output_data, eval_input_data, eval_output_data = model.split_data(input_samples, output_samples, test_split)
        #Fit the model
        model.train_model(train_input_data, train_output_data)
        #Save the model
        model.save_model()
        #Evauate the model
        model.evaluate_model(eval_input_data, eval_output_data)

        
import numpy as np
import uuid
import os
from training import Training

class FileRecording():

    def __init__(self,unique_name=None):
        if unique_name == None:
            unique_name = str(uuid.uuid4())
        
        self.winning_moves_filename = './Winning_Moves/' + unique_name + '.npy'
        self.history_filename = './Game_History/' + unique_name + '.npy'
        self.file_content = np.zeros((42, 7, 6))
    
    def write_to_history(self,round_nb,board):
        self.file_content[round_nb] = board
        np.save(self.history_filename, self.file_content)

    def write_to_winning_moves(self,started, turn, moves):
        arr = np.array([started, turn, moves], dtype="object")
        np.save(self.winning_moves_filename, arr)

    def read_history_file(self,file_name):
        folder = './Game_History/'
        current_game = np.load(folder + file_name)
        return current_game

    def read_winning_file(self, file_name):
        folder = './Winning_Moves/'
        current_game = np.load(folder + file_name,allow_pickle=True)
        started = current_game[0]
        turn = current_game[1]
        moves = current_game[2]
        return started, turn, moves

    def read_file(self, file_name):
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
            # print(-winner_boards[round])
            # print(current_board)
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
     
        # for i in range(21-len(moves)):
        #     encoded_moves.append([0 for j in range(7)])
        
        # print(len(winner_boards), len(encoded_moves), last_round, winner_boards[:last_round].shape)
        return winner_boards[:last_round], encoded_moves[:last_round], last_round  #return only the relevant arrays 

        

    def generate_training_set(self):
        games_history_folder = './Game_History/'
        history_games = os.listdir(games_history_folder)
        input_samples = np.zeros((len(history_games)*21, 7, 6))
        output_samples = np.zeros((len(history_games)*21, 7))
        total_rounds = 0

        for g in range(len(history_games)):
            winner_boards, encoded_moves, last_round = self.read_file(history_games[g]) 
            
            if last_round != 0:
                input_samples[total_rounds:total_rounds + last_round] = winner_boards
                output_samples[total_rounds:total_rounds + last_round] = encoded_moves  

            total_rounds += last_round
        input_samples = input_samples[:total_rounds]
        output_samples = output_samples[:total_rounds]

        # print(input_samples[-5:], output_samples[-5:], input_samples.shape, output_samples.shape)

    
        test_split = 0.2
        training = Training()

        #split the data first 
        training.create_NN()
        
        train_input_data, train_output_data, eval_input_data, eval_output_data = training.split_data(input_samples, output_samples, test_split)
        training.train_model(train_input_data, train_output_data, test_split)
        training.save_model()
        
        training.evaluate_model(eval_input_data, eval_output_data)

        
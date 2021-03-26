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
        arr = np.array([started,turn, moves],dtype="object")
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
        current_game = self.read_history_file(file_name)
        boards = np.zeros((21, 7, 6))

        if started == 0:
            boards[:len(current_game),:,:] = current_game[::2,:,:]
        else:
            boards[:len(current_game),:,:] = current_game[1::2,:,:]
        if turn == -1:
            boards *= -1
            
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
     
        for i in range(21-len(moves)):
            encoded_moves.append([0 for j in range(7)])

        #print(len(boards), len(moves))
        return boards, encoded_moves

        #print(encoded_moves)
        # print(boards)

    def generate_training_set(self):
        games_history_folder = './Game_History/'
        history_games = os.listdir(games_history_folder)
        training_input = np.zeros((len(history_games)*21, 7, 6))
        training_output = np.zeros((len(history_games)*21, 7))

        for g in range(len(history_games)):
            boards, encoded_moves = self.read_file(history_games[g])
            training_input[g:g+21] = boards
            training_output[g:g+21] = encoded_moves

        training = Training()
        training.train_model(training_input, training_output)

#1  [[1, 0, 0, 0, 0, 0], [1, 1, -1, 0, 0, 0], [1, 0, 0, 0, 0, 0], [-1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [-1, 0, 0, 0, 0, 0], [1, -1, -1, 0, 0, 0]]
#-1 [[1, 0, 0, 0, 0, 0], [1, 1, -1, 0, 0, 0], [1, 0, 0, 0, 0, 0], [-1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [-1, 0, 0, 0, 0, 0], [1, -1, -1, 0, 0, 0]]
#1  [[1, 0, 0, 0, 0, 0], [1, 1, -1, 0, 0, 0], [1, 0, 0, 0, 0, 0], [-1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [-1, 0, 0, 0, 0, 0], [1, -1, -1, -1, 0, 0]]
#-1 [[1, 0, 0, 0, 0, 0], [1, 1, -1, 0, 0, 0], [1, 0, 0, 0, 0, 0], [-1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [-1, 0, 0, 0, 0, 0], [1, -1, -1, -1, 0, 0]]
#1  [[1, 0, 0, 0, 0, 0], [1, 1, -1, 1, 0, 0], [1, 0, 0, 0, 0, 0], [-1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [-1, 0, 0, 0, 0, 0], [1, -1, -1, -1, 0, 0]]

# [0/1,[2,5,3,1,2,3]]
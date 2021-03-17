import numpy as np
import uuid
import os

class FileRecording():

    def __init__(self,unique_name=None):
        if unique_name == None:
            unique_name = str(uuid.uuid4())
        
        self.winning_moves_filename = './Winning_Moves/' + unique_name + '.npy'
        self.history_filename = './Game_History/' + unique_name + '.npy'
        self.file_content = np.zeros((42, 7, 6))
    
    def write_to_history(self,round_nb,board):
        print(board)
        self.file_content[round_nb] = board
        np.save(self.history_filename, self.file_content)

    def write_to_winning_moves(self,started,moves):
        arr = np.array([started,moves],dtype="object")
        np.save(self.winning_moves_filename, arr)

    def read_history_file(self):
        folder = './Game_History/'
        games = os.listdir(folder)
        current_game = np.load(folder + games[0])
        print('Total Games = {}'.format(len(games)))
        print('current_game shape = {}'.format(current_game.shape))
        print('current_game shape = {}'.format(current_game[5].shape))
        print(current_game[5])
    
    def read_winning_file(self):
        folder = './Winning_Moves/'
        games = os.listdir(folder)
        current_game = np.load(folder + games[0],allow_pickle=True)


#1  [[1, 0, 0, 0, 0, 0], [1, 1, -1, 0, 0, 0], [1, 0, 0, 0, 0, 0], [-1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [-1, 0, 0, 0, 0, 0], [1, -1, -1, 0, 0, 0]]
#-1 [[1, 0, 0, 0, 0, 0], [1, 1, -1, 0, 0, 0], [1, 0, 0, 0, 0, 0], [-1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [-1, 0, 0, 0, 0, 0], [1, -1, -1, 0, 0, 0]]
#1  [[1, 0, 0, 0, 0, 0], [1, 1, -1, 0, 0, 0], [1, 0, 0, 0, 0, 0], [-1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [-1, 0, 0, 0, 0, 0], [1, -1, -1, -1, 0, 0]]
#-1 [[1, 0, 0, 0, 0, 0], [1, 1, -1, 0, 0, 0], [1, 0, 0, 0, 0, 0], [-1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [-1, 0, 0, 0, 0, 0], [1, -1, -1, -1, 0, 0]]
#1  [[1, 0, 0, 0, 0, 0], [1, 1, -1, 1, 0, 0], [1, 0, 0, 0, 0, 0], [-1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [-1, 0, 0, 0, 0, 0], [1, -1, -1, -1, 0, 0]]

# [0/1,[2,5,3,1,2,3]]
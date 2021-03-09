import numpy as np
import matplotlib.pyplot as plt
import os


# Parameters for us to change
folder = './Saved_Games/'
game_num_to_plot = 0
round_to_plot = 9

# Get a list of all files in the load folder (note, only games should be in this folder)
games = os.listdir(folder)

# Assign the board to the chosen round to plot
current_game = np.load(folder + games[game_num_to_plot])

print('Total Games = {}'.format(len(games)))
print('current_game shape = {}'.format(current_game.shape))
print('current_game shape = {}'.format(current_game[5].shape))
print(current_game[5])
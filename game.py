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


if __name__ == '__main__':
    for i in range(2):
            game_mode = 2
            game = Connect4Game(2, 1)
            view = Connect4Viewer(game=game)
            view.initialize()

            running = True
            while running:
                if ((game._turn == 1) and (game.get_win() is None)):
                    game.bot_place()
                elif ((game._turn == -1) and (game.get_win() is None)):
                    game.bot_place()
                elif game.get_win() is not None:
                    running = False

                pygame.time.wait(1000)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        if game.get_win() is None:
                            game.place(pygame.mouse.get_pos()[0] // SQUARE_SIZE)
                        else:
                            game.reset_game()

    pygame.quit()

    # model = Model("./model_better_bot_type2_4layers")
    # # model = Model("./saved_model/my_model")
    # model.evaluate_model(100, 1)

    # f = FileRecording()

    # f.generate_training_set()

    # while(running and i < 100):

    #     if ((turn == AI) and (won is None)):
    #         bot()
    #     elif ((turn == PLAYER) and (won is None)):
    #         bot()
    #     else:
    #         update_view()
    #         print(state.round)
    #         nn_format()
    #         reset_game()
    #         i = i+1

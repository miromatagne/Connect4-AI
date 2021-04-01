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

PLAYERS = {1: "Yellow", -1: "Red"}

# Graphical size settings
SQUARE_SIZE = 100
DISC_SIZE_RATIO = 0.8

# Colours
BLUE_COLOR = (23, 93, 222)
YELLOW_COLOR = (255, 240, 0)
RED_COLOR = (255, 0, 0)
BACKGROUND_COLOR = (19, 72, 162)
BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)


class Event(enum.Enum):
    PIECE_PLACED = 1
    GAME_WON = 2
    GAME_RESET = 3


class Connect4Game(Observable):

    def __init__(self, player1, player2, rows=6, cols=7):
        super().__init__()
        self._rows = rows
        self._cols = cols
        self._board = None
        self._turn = None
        self._won = None
        self._round = 0
        self.bot = None
        self.moves = {1: [], -1: []}
        self.file_recording = FileRecording()
        self.reset_game()
        self._player1 = Bot(self, player1)
        self._player2 = Bot(self, player2)

        # if game_mode == 0:
        #     self.bot = Bot(self, 0)
        # elif game_mode == 1:
        #     self.bot = Bot(self, 1)
        # elif game_mode == 2:
        #     self.bot = Bot(self, 2)

    def reset_game(self):
        """
        Resets the game state (board and variables)
        """
        # print("reset")
        self._board = [[0 for _ in range(self._rows)]
                       for _ in range(self._cols)]
        self._starter = random.choice([-1, 1])
        self._turn = self._starter
        # (self._turn)
        self._won = None
        self.notify(Event.GAME_RESET)

    def place(self, c):
        """
        Tries to place the playing colour on the cth column
        :param c: column to place on
        :return: position of placed colour or None if not placeable
        """
        # print(self._board)
        for r in range(self._rows):
            if self._board[c][r] == 0:
                self._board[c][r] = self._turn
                self.notify(Event.PIECE_PLACED, (c, r))

                self.file_recording.write_to_history(self._round, self._board)
                self.moves[self._turn].append(c)

                exists_winner = self.check_win((c, r))
                if exists_winner:
                    b = 0
                    if self._turn == self._starter:  # Winner is the player that started
                        b = 1
                    self.file_recording.write_to_winning_moves(
                        b, self._turn, self.moves[self._turn])
                    self._won = self._turn
                    self.notify(Event.GAME_WON, self._won)

                if self._turn == 1:
                    self._turn = -1
                else:
                    self._turn = 1

                self._round = self._round + 1
                return c, r
        return None

    def check_win(self, pos):
        """
        Checks for win/draw from newly added disc
        :param pos: position from which to check the win
        :return: player number if a win occurs, 0 if a draw occurs, None otherwise
        """
        c = pos[0]
        r = pos[1]
        player = self._board[c][r]

        min_col = max(c-3, 0)
        max_col = min(c+3, self._cols-1)
        min_row = max(r - 3, 0)
        max_row = min(r + 3, self._rows - 1)

        # Horizontal check
        count = 0
        for ci in range(min_col, max_col + 1):
            if self._board[ci][r] == player:
                count += 1
            else:
                count = 0
            if count == 4:
                #print("Horizontal win")
                #self._won = player
                #self.notify(Event.GAME_WON, self._won)
                # return self._won
                return True

        # Vertical check
        count = 0
        for ri in range(min_row, max_row + 1):
            if self._board[c][ri] == player:
                count += 1
            else:
                count = 0
            if count == 4:
                #print("Vertical win")
                # self._won = player
                # self.notify(Event.GAME_WON, self._won)
                # return self._won
                return True

        count1 = 0
        count2 = 0
        # Diagonal check
        for i in range(-3, 4):
            # bottom-left -> top-right
            if 0 <= c + i < self._cols and 0 <= r + i < self._rows:
                if self._board[c + i][r + i] == player:
                    count1 += 1
                else:
                    count1 = 0
                if count1 == 4:
                    #print("Diagonal BL-TR win")
                    # self._won = player
                    # self.notify(Event.GAME_WON, self._won)
                    # return self._won
                    return True
            # bottom-right -> top-let
            if 0 <= c + i < self._cols and 0 <= r - i < self._rows:
                if self._board[c + i][r - i] == player:
                    count2 += 1
                else:
                    count2 = 0
                if count2 == 4:
                    #print("Diagonal BR-TL win")
                    # self._won = player
                    # self.notify(Event.GAME_WON, self._won)
                    # return self._won
                    return True

        # Draw check
        if sum([x.count(0) for x in self._board]) == 0:
            # print("5")
            # self._won = 0
            # self.notify(Event.GAME_WON, self._won)
            # return self._won
            return True

        return False

    def get_cols(self):
        """
        :return: The number of columns of the game
        """
        return self._cols

    def get_rows(self):
        """
        :return: The number of rows of the game
        """
        return self._rows

    def get_win(self):
        """
        :return: If one play won or not
        """
        return self._won

    def get_turn(self):
        """
        :return: To which player is the turn
        """
        return self._turn

    def get_board(self):
        """
        :return: A copy of the game board
        """
        return self._board.copy()

    def board_at(self, c, r):
        """
        :param: c, the column
        :param: r, the row
        :return: What value is held at column c, row r in the board
        """
        return self._board[c][r]

    def copy_state(self):
        """
        Use this instead of the copy() method. Useful as we don't want our graphical interface (viewed as an Observer in this class)
        to be updated when we are playing moves in our tree search.
        """

        # Temporary removes the
        temporary_observers = self._observers
        self._observers = []

        new_one = deepcopy(self)
        new_one._observers.clear()  # Clear observers, such as GUI in our case.

        # Reassign the observers after deepcopy
        self._observers = temporary_observers

        return new_one

    def nn_format(self):
        if win != 0:
            current_board = np.load(state.filename)
            output_move = current_board[:, :, 0]
            np.save(state.outputname, output_move)

    def bot_place(self):
        if self._turn == 1:
            self._player1.make_move()
        else:
            self._player2.make_move()


class Connect4Viewer(Observer):

    def __init__(self, game):
        super(Observer, self).__init__()
        assert game is not None
        self._game = game
        self._game.add_observer(self)
        self._screen = None
        self._font = None

    def initialize(self):
        """
        Initialises the view window
        """
        pygame.init()
        icon = pygame.image.load("icon.png")
        pygame.display.set_icon(icon)
        pygame.display.set_caption("Connect Four")
        self._font = pygame.font.SysFont(None, 80)
        self._screen = pygame.display.set_mode(
            [self._game.get_cols() * SQUARE_SIZE, self._game.get_rows() * SQUARE_SIZE])
        self.draw_board()

    def draw_board(self):
        """
        Draws board[c][r] with c = 0 and r = 0 being bottom left
        0 = empty (background colour)
        1 = yellow
        2 = red
        """
        self._screen.fill(BLUE_COLOR)

        for r in range(self._game.get_rows()):
            for c in range(self._game.get_cols()):
                colour = BACKGROUND_COLOR
                if self._game.board_at(c, r) == 1:
                    colour = YELLOW_COLOR
                if self._game.board_at(c, r) == -1:
                    colour = RED_COLOR

                # Anti-aliased circle drawing
                pygame.gfxdraw.aacircle(self._screen, c * SQUARE_SIZE + SQUARE_SIZE // 2,
                                        self._game.get_rows() * SQUARE_SIZE - r * SQUARE_SIZE - SQUARE_SIZE // 2,
                                        int(DISC_SIZE_RATIO * SQUARE_SIZE / 2),
                                        colour)

                pygame.gfxdraw.filled_circle(self._screen, c * SQUARE_SIZE + SQUARE_SIZE // 2,
                                             self._game.get_rows() * SQUARE_SIZE - r * SQUARE_SIZE - SQUARE_SIZE // 2,
                                             int(DISC_SIZE_RATIO *
                                                 SQUARE_SIZE / 2),
                                             colour)
        pygame.display.update()

    def update(self, obj, event, *argv):
        """
        Called when notified. Updates the view.
        """
        if event == Event.GAME_WON:
            won = argv[0]
            self.draw_win_message(won)
        elif event == Event.GAME_RESET:
            self.draw_board()
        elif event == Event.PIECE_PLACED:
            self.draw_board()

    def draw_win_message(self, won):
        """
        Displays win message on top of the board
        """
        if won == 1:
            img = self._font.render(
                "Yellow won", True, BLACK_COLOR, YELLOW_COLOR)
        elif won == -1:
            img = self._font.render("Red won", True, WHITE_COLOR, RED_COLOR)
        else:
            img = self._font.render("Draw", True, WHITE_COLOR, BLUE_COLOR)

        rect = img.get_rect()
        rect.center = ((self._game.get_cols() * SQUARE_SIZE) //
                       2, (self._game.get_rows() * SQUARE_SIZE) // 2)

        self._screen.blit(img, rect)
        pygame.display.update()


if __name__ == '__main__':
    # for i in range(10000):
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

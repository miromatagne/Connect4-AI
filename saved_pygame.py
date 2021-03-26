import pygame
import pygame.gfxdraw
import random
import numpy as np

import time


class State(object):
    def __init__(self):
        self.round = 0
        self.filename = './Saved_Games/' + str(int(time.time())) + '.npy'




PLAYER = 1
AI = 2
sample=True
# Game settings
rows = 6
cols = 7
square_size = 100
disc_size_ratio = 0.8

# Colours
blue = (23, 93, 222)
yellow = (255, 240, 0)
red = (255, 0, 0)
background = (19, 72, 162)
black = (0, 0, 0)
white = (255, 255, 255)

# Pygame config
pygame.init()
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Connect Four")
font = pygame.font.SysFont(None, 80)
screen = None


def init():
    """
    Initialises the view window
    """
    
    global screen
    screen = pygame.display.set_mode([cols*square_size, rows*square_size])
    


# Game state
board = [[0 for r in range(rows)] for c in range(cols)]
turn = random.randint(PLAYER, AI)
won = None


def reset_game():
    """
    Resets the game state (board and variables)
    """
    global board, turn, won
    board = [[0 for _ in range(rows)] for _ in range(cols)]
    turn = random.randint(PLAYER, AI)
    won = None
    global state
    state = State()


def place(c):
    """
    Tries to place the playing colour on the cth column
    :param c: column to place on
    :return: position of placed colour or None if not placeable
    """
    global turn, won

    for r in range(rows):
        if board[c][r] == 0:
            board[c][r] = turn

            if turn == PLAYER:
                turn = AI
            else:
                turn = PLAYER
            return c, r
    return None


def check_win(pos):
    """
    Checks for win/draw from newly added disc
    :param pos: position from which to check the win
    :return: player number if a win occurs, 0 if a draw occurs, None otherwise
    """
    global won
    if pos is None:
        return won
    c = pos[0]
    r = pos[1]
    player = board[c][r]
    min_col = max(c-3, 0)
    max_col = min(c+3, cols-1)
    min_row = max(r - 3, 0)
    max_row = min(r + 3, rows - 1)

    # Horizontal check
    count = 0
    for ci in range(min_col, max_col + 1):
        if board[ci][r] == player:
            count += 1
        else:
            count = 0
        count
        if count == 4:
            won = player
            return won

    # Vertical check
    count = 0
    for ri in range(min_row, max_row + 1):
        if board[c][ri] == player:
            count += 1
        else:
            count = 0
        if count == 4:
            won = player
            return won

    count1 = 0
    count2 = 0
    # Diagonal check
    for i in range(-3, 4):
        # bottom-left -> top-right
        if 0 <= c + i < cols and 0 <= r + i < rows:
            if board[c + i][r + i] == player:
                count1 += 1
            else:
                count1 = 0
            if count1 == 4:
                won = player
                return won
        # bottom-right -> top-let
        if 0 <= c + i < cols and 0 <= r - i < rows:
            if board[c + i][r - i] == player:
                count2 += 1
            else:
                count2 = 0
            if count2 == 4:
                won = player
                return won

    # Draw check
    if sum([x.count(0) for x in board]) == 0:
        won = 0
        return won

    won = None
    return won


def draw_board():
    """
    Draws board[c][r] with c = 0 and r = 0 being bottom left
    0 = empty (background colour)
    1 = yellow
    2 = red
    """
    screen.fill(blue)

    for r in range(rows):
        for c in range(cols):
            colour = background
            if board[c][r] == 1:
                colour = yellow
            if board[c][r] == 2:
                colour = red

            # Classical non anti-aliased circle drawing
            # pygame.draw.circle(screen, colour, (c*square_size + square_size//2, rows*square_size - r*square_size - square_size//2), int(disc_size_ratio * square_size/2))

            # Anti-aliased circle drawing
            pygame.gfxdraw.aacircle(screen, c*square_size + square_size//2, rows*square_size - r*square_size - square_size//2, int(disc_size_ratio * square_size/2), colour)
            pygame.gfxdraw.filled_circle(screen, c*square_size + square_size//2, rows*square_size - r*square_size - square_size//2, int(disc_size_ratio * square_size/2), colour)


def draw_win_message():
    """
    Displays win message on top of the board
    """
    if won is not None:
        if won == 1:
            img = font.render("Yellow won", True, black, yellow)
        elif won == 2:
            img = font.render("Red won", True, white, red)
        else:
            img = font.render("Draw", True, white, blue)

        rect = img.get_rect()
        rect.center = ((cols * square_size)//2, (rows * square_size)//2)

        screen.blit(img, rect)


def update_view():
    """
    Updates the pygame view with correct board
    """
    draw_board()
    draw_win_message()

    pygame.display.update()


def make_move(state):
    field_state = np.array(board)
    if (state.round == 0):
        current_board = np.zeros((30,6, 7))
    else:
        current_board = np.load(state.filename)
    
    c = random.randint(0, cols-1)
    while (board[c][rows-1]!=0):		
        c = random.randint(0, cols-1)
    for r in range(rows):
        if board[c][r] == 0:
            current_board[state.round][r][c]=turn
            np.save(state.filename, current_board)

    return c

def bot():
    check_win(place(make_move(state)))

if __name__ == '__main__':
    init()
    reset_game()

    running = True
    i=0
    while(running and i<200):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if won is None and turn == PLAYER:
                    check_win(place(pygame.mouse.get_pos()[0]//square_size))
                else:
                    reset_game()
            if ((turn == AI) and (won is None) and (sample)):	
                bot()
            elif ((turn == PLAYER) and (won is None) and (sample)):
                bot()
            elif won:
               
                reset_game()
                i=i+1
                
        update_view()
       

    pygame.quit()
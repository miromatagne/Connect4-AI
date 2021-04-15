from observer import Observer
import pygame
import pygame.gfxdraw
from event import Event

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

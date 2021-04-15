import enum


class Event(enum.Enum):
    PIECE_PLACED = 1
    GAME_WON = 2
    GAME_RESET = 3

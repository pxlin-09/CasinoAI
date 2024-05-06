from enum import Enum, auto


class Game(Enum):
    BLACKJACK = auto()


class Action(Enum):
    HIT = auto()
    HIT_DOUBLE = auto()
    STAND = auto()

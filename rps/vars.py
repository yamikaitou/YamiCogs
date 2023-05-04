from enum import Enum


class Result(str, Enum):
    LOSE = "Look at that, I win!"
    WIN = "Congrats, you win!"
    TIE = "Well, we must be mind-readers!"


class RPSChoice(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


class RPSLSChoice(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3
    LIZARD = 4
    SPOCK = 5


class RPSIcon(str, Enum):
    ROCK = "\U0001faa8"
    PAPER = ("\N{NEWSPAPER}",)
    SCISSORS = "\N{BLACK SCISSORS}\N{VARIATION SELECTOR-16}"


class RPSLSIcon(str, Enum):
    ROCK = "\U0001faa8"
    PAPER = ("\N{NEWSPAPER}",)
    SCISSORS = "\N{BLACK SCISSORS}\N{VARIATION SELECTOR-16}"
    LIZARD = "\N{LIZARD}"
    SPOCK = "\N{RAISED HAND WITH PART BETWEEN MIDDLE AND RING FINGERS}"

from enum import Enum

from redbot.core import app_commands
from redbot.core.i18n import Translator

_ = Translator("RPS", __file__)


class Result(str, Enum):
    LOSE = "lose"
    WIN = "win"
    TIE = "tie"

    def __str__(self) -> str:
        return self.value

    def __int__(self) -> int:
        return self.value


class RPSChoice(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

    def __str__(self) -> str:
        return self.value

    def __int__(self) -> int:
        return self.value


class RPSLSChoice(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3
    LIZARD = 4
    SPOCK = 5

    def __str__(self) -> str:
        return self.value

    def __int__(self) -> int:
        return self.value


class RPSIcon(str, Enum):
    ROCK = "\U0001faa8"
    PAPER = "\N{NEWSPAPER}"
    SCISSORS = "\N{BLACK SCISSORS}\N{VARIATION SELECTOR-16}"

    def __str__(self) -> str:
        return self.value

    def __int__(self) -> int:
        return self.value


class RPSLSIcon(str, Enum):
    ROCK = "\U0001faa8"
    PAPER = "\N{NEWSPAPER}"
    SCISSORS = "\N{BLACK SCISSORS}\N{VARIATION SELECTOR-16}"
    LIZARD = "\N{LIZARD}"
    SPOCK = "\N{RAISED HAND WITH PART BETWEEN MIDDLE AND RING FINGERS}"

    def __str__(self) -> str:
        return self.value

    def __int__(self) -> int:
        return self.value


class Icon(str, Enum):
    ROCK = "\U0001faa8"
    PAPER = "\N{NEWSPAPER}"
    SCISSORS = "\N{BLACK SCISSORS}\N{VARIATION SELECTOR-16}"
    LIZARD = "\N{LIZARD}"
    SPOCK = "\N{RAISED HAND WITH PART BETWEEN MIDDLE AND RING FINGERS}"

    def __str__(self) -> str:
        return self.value

    def __int__(self) -> int:
        return self.value


class Choice(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3
    LIZARD = 4
    SPOCK = 5

    def __str__(self) -> str:
        return self.value

    def __int__(self) -> int:
        return self.value


GameType = [
    app_commands.Choice(name="Rock, Paper, Scissors", value="RPS"),
    app_commands.Choice(name="Rock, Paper, Scissors, Lizard, Spock", value="RPSLS"),
]

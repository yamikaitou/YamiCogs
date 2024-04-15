from enum import Enum
from redbot.core.i18n import Translator

_ = Translator("RPS", __file__)

class Result(str, Enum):
    LOSE = _("Look at that, I win!")
    WIN = _("Congrats, you win!")
    TIE = _("Well, we must be mind-readers!")

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
    PAPER = ("\N{NEWSPAPER}",)
    SCISSORS = "\N{BLACK SCISSORS}\N{VARIATION SELECTOR-16}"

    def __str__(self) -> str:
        return self.value

    def __int__(self) -> int:
        return self.value


class RPSLSIcon(str, Enum):
    ROCK = "\U0001faa8"
    PAPER = ("\N{NEWSPAPER}",)
    SCISSORS = "\N{BLACK SCISSORS}\N{VARIATION SELECTOR-16}"
    LIZARD = "\N{LIZARD}"
    SPOCK = "\N{RAISED HAND WITH PART BETWEEN MIDDLE AND RING FINGERS}"

    def __str__(self) -> str:
        return self.value

    def __int__(self) -> int:
        return self.value

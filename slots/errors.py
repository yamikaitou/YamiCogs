class SlotsError(Exception):
    """Base error class for Slots-related errors."""


class MachineMissingCost(SlotsError):
    """Machine doesn't have a play cost"""


class MachineMissingName(SlotsError):
    """Machine doesn't have a name"""


class MachineMissingDescription(SlotsError):
    """Machine doesn't have a description"""


class MachineMissingReels(SlotsError):
    """Machine doesn't have any reel slots"""


class MachineMissingPrizes(SlotsError):
    """Machine doesn't have any prizes"""


class ReelSlotMissingEmoji(SlotsError):
    """Reel slot doesn't have an emoji"""


class ReelSlotMissingName(SlotsError):
    """Reel slot doesn't have a name"""


class ReelSlotEmojiUnusable(SlotsError):
    """Reel slot's Emoji cannot be used"""


class PrizeMissingName(SlotsError):
    """Prize doesn't have a name"""


class PrizeMissingPattern(SlotsError):
    """Prize doesn't have a pattern"""


class PrizeMissingAmount(SlotsError):
    """Prize doesn't have an amount"""


class ValidateTypeCost(SlotsError):
    """Cost is not an Integer"""


class ValidateTypeRandomize(SlotsError):
    """Randomize is not an Boolean"""


class ValidateTypePrizeKey(SlotsError):
    """Prize Key is not an Integer"""


class ValidateTypePrizeAmount(SlotsError):
    """Prize amount is not an Integer"""

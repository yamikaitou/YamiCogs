import discord
import random
from redbot.core import commands, Config, checks


class Hermitron(commands.Cog):
    """
    Hermitron game
    """

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=192153481165930496, force_registration=True)

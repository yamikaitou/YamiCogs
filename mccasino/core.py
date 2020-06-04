import discord
import random
from redbot.core import commands, Config, checks


class MinecraftCasino(commands.Cog):
    """
    Play Casino games with random Minecraft stuff
    """

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=582650109, force_registration=True)

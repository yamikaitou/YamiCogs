import logging
from typing import Literal
import random

import discord
from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.config import Config

log = logging.getLogger("red.yamicogs.ping")

RequestType = Literal["discord_deleted_user", "owner", "user", "user_strict"]


class Ping(commands.Cog):
    """
    Ping replace
    """

    def __init__(self, bot: Red) -> None:
        self.bot = bot
        self.config = Config.get_conf(
            self,
            identifier=582650109,
            force_registration=True,
        )

    async def red_delete_data_for_user(self, *, requester: RequestType, user_id: int) -> None:
        # this cog does not store any user data
        pass

    @commands.command(name="ping")
    async def _ping(self, ctx):
        await ctx.send(f"{random.randint(1,1000)}ms")
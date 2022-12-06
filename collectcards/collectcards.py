from typing import Literal
import json
import unicodedata

from redbot.core import commands, data_manager
from redbot.core.bot import Red
from redbot.core.config import Config
import discord

RequestType = Literal["discord_deleted_user", "owner", "user", "user_strict"]


class CollectCards(commands.Cog):
    """
    A 'card' (emoji) collecting game
    """

    def __init__(self, bot: Red) -> None:
        self.bot = bot
        self.config = Config.get_conf(
            self,
            identifier=582650109,
            force_registration=True,
        )

    async def cog_load(self):
        with open(data_manager.bundled_data_path(self) / "sets.json", "r") as f:
            self.cards = json.load(f)

    @commands.command(name="collectcards")
    async def _collectcards(self, ctx):
        """
        About the game
        """

        cardset = self.cards["sets"][0]

        embed = discord.Embed(title=f"Cards - {cardset['name']}")

        for card in cardset["cards"]:
            embed.add_field(name=card["name"], value=card["emoji"])

        await ctx.send(embed=embed)

    async def red_delete_data_for_user(self, *, requester: RequestType, user_id: int) -> None:
        # TODO: Replace this with the proper end user data removal handling.
        super().red_delete_data_for_user(requester=requester, user_id=user_id)

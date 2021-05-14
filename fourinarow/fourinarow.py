import discord
import numpy as np
from redbot.core import Config, commands
from redbot.core.utils.predicates import ReactionPredicate


class FourInARow(commands.Cog):
    """
    Four In A Row
    """

    __version__ = "0.1"

    def format_help_for_context(self, ctx):
        """Thanks Sinbad."""
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\nCog Version: {self.__version__}"

    piece = [":black_circle:", ":red_circle:", ":yellow_circle:"]

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=192153481165930496, force_registration=True)

    @commands.group(name="4row")
    async def fourrow(self, ctx):
        """Four in a Row"""

    @fourrow.command()
    async def test(self, ctx):
        """Test Command"""
        game = np.zeros((7, 6), dtype=int, order="F")
        game = [
            [0, 0, 0, 0, 0, 0],
            [1, 2, 1, 2, 0, 0],
            [1, 2, 2, 1, 0, 0],
            [2, 2, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ]
        embed = discord.Embed(title="Four in a Row", colour=await ctx.embed_color())
        embed.description = self.print_board(game)
        embed.add_field(
            name="🔴 Turn",
            value="React with the column number to place your piece or :x: to forfiet",
        )
        embed.set_footer(text="🔴 YamiKaitou#8975 | 🟡 ItazuaKaitou#5009")
        msg = await ctx.send(embed=embed)
        for k in range(1, 8):
            await msg.add_reaction(ReactionPredicate.NUMBER_EMOJIS[k])
        await msg.add_reaction("❌")

    def print_board(self, board):
        """Return a string of the game board"""

        string = "| :one:  :two:  :three:  :four:  :five:  :six:  :seven: |\n\n"

        for k in reversed(range(6)):
            string += "|"
            for j in range(7):
                string += " " + self.piece[board[j][k]] + " "
            string += "|\n"

        return string

    async def red_get_data_for_user(self, *, user_id: int):
        # this cog does not store any data
        return {}

    async def red_delete_data_for_user(self, *, requester, user_id: int) -> None:
        # this cog does not store any data
        pass

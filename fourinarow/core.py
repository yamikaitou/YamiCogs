import discord
import random
from redbot.core import commands, Config, checks
from redbot.core.utils.predicates import ReactionPredicate
import numpy as np


class FourInARow(commands.Cog):
    """
    Four In A Row
    """

    piece = [":black_circle:", ":red_circle:", ":yellow_circle:"]

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=192153481165930496, force_registration=True)
    
    @commands.group(name="4row")
    async def fourrow(self, ctx):
        """Four in a Row"""
        pass
    
    @fourrow.command()
    async def test(self, ctx):
        """Test Command"""
        game = np.zeros((7,6), dtype=int, order='F')
        game = [[0,0,0,0,0,0],[1,2,1,2,0,0],[1,2,2,1,0,0],[2,2,1,0,0,0],[0,0,0,0,0,0],[1,0,0,0,0,0],[0,0,0,0,0,0]]
        embed = discord.Embed(title="Four in a Row", colour=await ctx.embed_color())
        embed.description=self.print_board(game)
        embed.add_field(name="🔴 Turn", value="React with the column number to place your piece or :x: to forfiet")
        embed.set_footer(text="🔴 YamiKaitou#8975 | 🟡 Eevee#5009")
        msg = await ctx.send(embed=embed)
        for k in range(0,7):
            await msg.add_reaction(ReactionPredicate.NUMBER_EMOJIS[k])
        await msg.add_reaction("❌")

    
    def print_board(self, board):
        """Return a string of the game board"""

        string = "| :one:  :two:  :three:  :four:  :five:  :six:  :seven: |\n\n"

        for k in reversed(range(6)):
            string += "|"
            for j in range(7):
                string += " "+self.piece[board[j][k]]+" "
            string += "|\n"
        
        return string

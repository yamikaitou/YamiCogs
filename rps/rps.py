import logging

import discord
from redbot.core import commands
from redbot.core.bot import Red

from .rpslsview import RPSLSView
from .rpsview import RPSView

log = logging.getLogger("red.yamicogs.rps")


class RPS(commands.Cog):
    """
    Rock, Paper, Scissors (Lizard, Spock)

    More detailed docs: <https://cogs.yamikaitou.dev/rps.html>
    """

    def __init__(self, bot: Red) -> None:
        self.bot = bot

    @commands.command(name="rpsrules", aliases=["rpslsrules"])
    async def _rps_rules(self, ctx):
        """Rules of Rock, Paper, Scissors (Lizard, Spock)"""

        embed = discord.Embed()
        embed.title = "Rock, Paper, Scissors (Lizard, Spock)"
        embed.color = await ctx.embed_color()
        embed.description = (
            f"A game of skill (chance).\n"
            f"Simply select your choice and see if you can defeat the computer\n\n"
            f"2 versions are included, the rules are below\n"
        )
        embed.add_field(
            name="Rock, Paper, Scissors",
            inline=False,
            value=(
                f"Rock {ICONS_RPS['rock']} beats Scissors {ICONS_RPS['scissors']}\n"
                f"Scissors {ICONS_RPS['scissors']} beats Paper {ICONS_RPS['paper']}\n"
                f"Paper {ICONS_RPS['paper']} beats Rock {ICONS_RPS['rock']}\n\n"
                f"Play with `{ctx.prefix}rps`\n"
            ),
        )
        embed.add_field(
            name="Rock, Paper, Scissors, Lizard, Spock",
            inline=False,
            value=(
                f"Rock {ICONS_RPSLS['rock']} beats Scissors {ICONS_RPSLS['scissors']} and Lizard {ICONS_RPSLS['lizard']}\n"
                f"Paper {ICONS_RPSLS['paper']} beats Rock {ICONS_RPSLS['rock']} and Spock {ICONS_RPSLS['spock']}\n"
                f"Scissors {ICONS_RPSLS['scissors']} beats Paper {ICONS_RPSLS['paper']} and Lizard {ICONS_RPSLS['lizard']}\n"
                f"Lizard {ICONS_RPSLS['lizard']} beats Paper {ICONS_RPSLS['paper']} and Spock {ICONS_RPSLS['spock']}\n"
                f"Spock {ICONS_RPSLS['spock']} beats Rock {ICONS_RPSLS['rock']} and Scissors {ICONS_RPSLS['scissors']}\n\n"
                f"Play with `{ctx.prefix}rpsls`\n"
            ),
        )

        await ctx.send(embed=embed)

    @commands.command(name="rps")
    async def _rps(self, ctx):
        """Play a game of Rock, Paper, Scissors"""

        view = RPSView(self, ctx.author.id)
        await ctx.send(view=view)

        await view.wait()
        if view.value is None:
            await ctx.message.edit(content="Very well, maybe later", embed=None, view=None)

    @commands.command(name="rpsls")
    async def _rpsls(self, ctx):
        """Play a game of Rock, Paper, Scissors, Lizard, Spock"""

        view = RPSLSView(self, ctx.author.id)
        await ctx.send(view=view)

        await view.wait()
        if view.value is None:
            await ctx.message.edit(content="Very well, maybe later", embed=None, view=None)

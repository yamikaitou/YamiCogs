import logging

import discord
from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.i18n import Translator, cog_i18n

from .rpslsview import RPSLSView
from .rpsview import RPSView
from .vars import Result, RPSChoice, RPSIcon, RPSLSChoice, RPSLSIcon

log = logging.getLogger("red.yamicogs.rps")
_ = Translator("RPS", __file__)


@cog_i18n(_)
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
            _("A game of skill (chance).\n"
            "Simply select your choice and see if you can defeat the computer\n\n"
            "2 versions are included, the rules are below\n")
        )
        embed.add_field(
            name=_("Rock, Paper, Scissors"),
            inline=False,
            value=(
                _("Rock {ROCK} beats Scissors {SCISSORS}\n"
                "Scissors {SCISSORS} beats Paper {PAPER}\n"
                "Paper {PAPER} beats Rock {ROCK}\n\n"
                "Play with `{PREFIX}rps`\n").format(
                    ROCK=RPSIcon.ROCK, PAPER=RPSIcon.PAPER, SCISSORS=RPSIcon.SCISSORS, PREFIX=ctx.clean_prefix
                )
            ),
        )
        embed.add_field(
            name=_("Rock, Paper, Scissors, Lizard, Spock"),
            inline=False,
            value=(_(
                "Rock {ROCK} beats Scissors {SCISSORS} and Lizard {LIZARD}\n"
                "Paper {PAPER} beats Rock {ROCK} and Spock {SPOCK}\n"
                "Scissors {SCISSORS} beats Paper {PAPER} and Lizard {LIZARD}\n"
                "Lizard {LIZARD} beats Paper {PAPER} and Spock {SPOCK}\n"
                "Spock {SPOCK} beats Rock {ROCK} and Scissors {SCISSORS}\n\n"
                "Play with `{PREFIX}rpsls`\n").format(
                    ROCK=RPSLSIcon.ROCK, PAPER=RPSLSIcon.PAPER, SCISSORS=RPSLSIcon.SCISSORS, LIZARD=RPSLSIcon.LIZARD, SPOCK=RPSLSIcon.SPOCK,  PREFIX=ctx.clean_prefix
                )
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
            await ctx.message.edit(content=_("Very well, maybe later"), embed=None, view=None)

    @commands.command(name="rpsls")
    async def _rpsls(self, ctx):
        """Play a game of Rock, Paper, Scissors, Lizard, Spock"""

        view = RPSLSView(self, ctx.author.id)
        await ctx.send(view=view)

        await view.wait()
        if view.value is None:
            await ctx.message.edit(content=_("Very well, maybe later"), embed=None, view=None)
    
    async def _outcome(self, interaction: discord.Interaction, outcome, player, computer):
        if outcome == "win":
            await interaction.message.edit(
                content=_("Congrats, you win!\n\nYou {player_icon} - {computer_icon} Me").format(player_icon=player, computer_icon=computer),
                embed=None,
                view=None,
            )
        elif outcome == "lose":
            await interaction.message.edit(
                content=_("Look at that, I win!\n\nYou {player_icon} - {computer_icon} Me").format(player_icon=player, computer_icon=computer),
                embed=None,
                view=None,
            )
        elif outcome == "tie":
            await interaction.message.edit(
                content=_("Well, we must be mind-readers!\n\nYou {player_icon} - {computer_icon} Me").format(player_icon=player, computer_icon=computer),
                embed=None,
                view=None,
            )
        else:
            await interaction.message.edit(
                content=_("Well, this is embarrassing. No idea what happens now"),
                embed=None,
                view=None,
            )


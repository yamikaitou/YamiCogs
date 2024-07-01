import logging
import random
from typing import Optional

import discord
from redbot.core import app_commands, commands
from redbot.core.bot import Red
from redbot.core.i18n import Translator, cog_i18n, set_contextual_locales_from_guild

from .duelview import DuelView
from .playerview import PlayerView
from .rpslsview import RPSLSView
from .rpsview import RPSView
from .vars import Choice, GameType, Icon, Result

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
        self.games = {}

    @commands.command(name="rpsrules", aliases=["rpslsrules"])
    async def _rps_rules(self, ctx):
        """Rules of Rock, Paper, Scissors (Lizard, Spock)"""

        embed = discord.Embed()
        embed.title = "Rock, Paper, Scissors (Lizard, Spock)"
        embed.color = await ctx.embed_color()
        embed.description = _(
            "A game of skill (chance).\n"
            "Simply select your choice and see if you can defeat the computer\n\n"
            "2 versions are included, the rules are below\n"
        )
        embed.add_field(
            name=_("Rock, Paper, Scissors"),
            inline=False,
            value=(
                _(
                    "Rock {ROCK} beats Scissors {SCISSORS}\n"
                    "Scissors {SCISSORS} beats Paper {PAPER}\n"
                    "Paper {PAPER} beats Rock {ROCK}\n\n"
                    "Play with `{PREFIX}rps`\n"
                ).format(
                    ROCK=Icon.ROCK,
                    PAPER=Icon.PAPER,
                    SCISSORS=Icon.SCISSORS,
                    PREFIX=ctx.clean_prefix,
                )
            ),
        )
        embed.add_field(
            name=_("Rock, Paper, Scissors, Lizard, Spock"),
            inline=False,
            value=(
                _(
                    "Rock {ROCK} beats Scissors {SCISSORS} and Lizard {LIZARD}\n"
                    "Paper {PAPER} beats Rock {ROCK} and Spock {SPOCK}\n"
                    "Scissors {SCISSORS} beats Paper {PAPER} and Lizard {LIZARD}\n"
                    "Lizard {LIZARD} beats Paper {PAPER} and Spock {SPOCK}\n"
                    "Spock {SPOCK} beats Rock {ROCK} and Scissors {SCISSORS}\n\n"
                    "Play with `{PREFIX}rpsls`\n"
                ).format(
                    ROCK=Icon.ROCK,
                    PAPER=Icon.PAPER,
                    SCISSORS=Icon.SCISSORS,
                    LIZARD=Icon.LIZARD,
                    SPOCK=Icon.SPOCK,
                    PREFIX=ctx.clean_prefix,
                )
            ),
        )

        await ctx.send(embed=embed)

    @app_commands.command(name="rps")
    @app_commands.describe(
        user="The user you would like to duel. Leave blank to duel the bot.",
        gametype="The version of RPS to play",
    )
    @app_commands.choices(gametype=GameType)
    async def slash_rps(
        self, interaction: discord.Interaction, user: Optional[discord.User], gametype: str
    ):
        """Play a game of Rock, Paper, Scissors"""
        if user is None or user.bot:
            user = self.bot.user
            bot = True
        else:
            bot = False

        self.games[interaction.id] = {
            "p1": interaction.user,
            "p2": user,
            "gametype": gametype,
            "original": interaction,
            interaction.user.id: None,
            user.id: None,
        }
        await set_contextual_locales_from_guild(self.bot, self.games[id]["original"].guild)

        if bot:
            if gametype == "RPS":
                comp = random.choice([Choice.ROCK, Choice.PAPER, Choice.SCISSORS])
            else:
                comp = random.choice(
                    [Choice.ROCK, Choice.PAPER, Choice.SCISSORS, Choice.LIZARD, Choice.SPOCK]
                )

            await self._end_game(interaction.id, user, comp, Icon[comp.name])

            await interaction.response.send_message(
                content=_("An {choice} Duel is starting").format(choice=gametype),
            )
        else:
            await interaction.response.send_message(
                content=_("{player2}, you have been challanged to an {choice} Duel").format(
                    player2=user.mention, choice=gametype
                ),
                view=DuelView(self, interaction.id),
            )
        self.games[interaction.id]["msg"] = await interaction.original_response()

        view = PlayerView(self, interaction.id, interaction.user)
        if gametype == "RPS":
            view = view.remove_item(view.children[3]).remove_item(view.children[3])

        await interaction.followup.send(
            content="Please make your selection",
            view=view,
            ephemeral=True,
        )

    @commands.command(name="rps")
    async def _rps(self, ctx):
        """Play a game of Rock, Paper, Scissors"""

        view = RPSView(self, ctx.author.id)
        msg = await ctx.send(view=view)

        await view.wait()
        if view.value is None:
            await msg.edit(content=_("Very well, maybe later"), embed=None, view=None)

    @commands.command(name="rpsls")
    async def _rpsls(self, ctx):
        """Play a game of Rock, Paper, Scissors, Lizard, Spock"""

        view = RPSLSView(self, ctx.author.id)
        msg = await ctx.send(view=view)

        await view.wait()
        if view.value is None:
            await msg.edit(content=_("Very well, maybe later"), embed=None, view=None)

    async def _end_game(self, id: int, player: discord.User, pick: Choice, icon: Icon):
        await set_contextual_locales_from_guild(self.bot, self.games[id]["original"].guild)
        if pick is None:
            await self.games[id]["msg"].edit(
                content=_("Duel has been rejected (timed out)"), embed=None, view=None
            )
            del self.games[id]
            return

        self.games[id][player.id] = [pick, icon]

        if (
            self.games[id][self.games[id]["p1"].id] is not None
            and self.games[id][self.games[id]["p2"].id] is not None
        ):
            p1 = self.games[id][self.games[id]["p1"].id]
            p2 = self.games[id][self.games[id]["p2"].id]
            print(p1)
            print(p2)
            result = self._decide(p1[0], p2[0])

            if result == Result.WIN:
                await self.games[id]["msg"].edit(
                    content=_(
                        "{player1_mention} wins!!\n\n{player1_name} {player1_icon} - {player2_icon} {player2_name}"
                    ).format(
                        player1_mention=self.games[id]["p1"].mention,
                        player1_name=self.games[id]["p1"].display_name,
                        player1_icon=p1[1],
                        player2_name=self.games[id]["p2"].display_name,
                        player2_icon=p2[1],
                    ),
                    embed=None,
                    view=None,
                )
            elif result == Result.LOSE:
                await self.games[id]["msg"].edit(
                    content=_(
                        "{player2_mention} wins!!\n\n{player1_name} {player1_icon} - {player2_icon} {player2_name}"
                    ).format(
                        player2_mention=self.games[id]["p2"].mention,
                        player1_name=self.games[id]["p1"].display_name,
                        player1_icon=p1[1],
                        player2_name=self.games[id]["p2"].display_name,
                        player2_icon=p2[1],
                    ),
                    embed=None,
                    view=None,
                )
            elif result == Result.TIE:
                await self.games[id]["msg"].edit(
                    content=_(
                        "Well, we must be mind-readers!\n\n{player1_name} {player1_icon} - {player2_icon} {player2_name}"
                    ).format(
                        player1_name=self.games[id]["p1"].display_name,
                        player1_icon=p1[1],
                        player2_name=self.games[id]["p2"].display_name,
                        player2_icon=p2[1],
                    ),
                    embed=None,
                    view=None,
                )
            else:
                await self.games[id]["msg"].edit(
                    content=_("Well, this is embarrassing. No idea what happens now"),
                    embed=None,
                    view=None,
                )

    def _decide(self, p1, p2):
        if p1 == p2:
            return Result.TIE
        elif p1 == Choice.ROCK:
            if p2 in [Choice.SCISSORS, Choice.LIZARD]:
                return Result.WIN
            else:
                return Result.LOSE
        elif p1 == Choice.PAPER:
            if p2 in [Choice.ROCK, Choice.SPOCK]:
                return Result.WIN
            else:
                return Result.LOSE
        elif p1 == Choice.SCISSORS:
            if p2 in [Choice.PAPER, Choice.LIZARD]:
                return Result.WIN
            else:
                return Result.LOSE
        elif p1 == Choice.LIZARD:
            if p2 in [Choice.PAPER, Choice.SPOCK]:
                return Result.WIN
            else:
                return Result.LOSE
        elif p1 == Choice.SPOCK:
            if p2 in [Choice.SCISSORS, Choice.ROCK]:
                return Result.WIN
            else:
                return Result.LOSE

    async def _outcome(self, interaction, outcome, player, computer):
        await set_contextual_locales_from_guild(self.bot, interaction.guild)
        if outcome == "win":
            await interaction.message.edit(
                content=_("Congrats, you win!\n\nYou {player_icon} - {computer_icon} Me").format(
                    player_icon=player, computer_icon=computer
                ),
                embed=None,
                view=None,
            )
        elif outcome == "lose":
            await interaction.message.edit(
                content=_("Look at that, I win!\n\nYou {player_icon} - {computer_icon} Me").format(
                    player_icon=player, computer_icon=computer
                ),
                embed=None,
                view=None,
            )
        elif outcome == "tie":
            await interaction.message.edit(
                content=_(
                    "Well, we must be mind-readers!\n\nYou {player_icon} - {computer_icon} Me"
                ).format(player_icon=player, computer_icon=computer),
                embed=None,
                view=None,
            )
        else:
            await interaction.message.edit(
                content=_("Well, this is embarrassing. No idea what happens now"),
                embed=None,
                view=None,
            )

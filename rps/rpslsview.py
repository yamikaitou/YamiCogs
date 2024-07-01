import random

import discord
from redbot.core.i18n import Translator, set_contextual_locales_from_guild

from .vars import Choice, Icon, Result

_ = Translator("RPS", __file__)


class RPSLSView(discord.ui.View):
    def __init__(self, cog, user):
        super().__init__(timeout=600.0)
        self.cog = cog
        self.user = user
        self.value = None
        self.computer = random.choice(
            [Choice.ROCK, Choice.PAPER, Choice.SCISSORS, Choice.LIZARD, Choice.SPOCK]
        )

    @discord.ui.button(
        label="Rock",
        style=discord.ButtonStyle.blurple,
        custom_id="rpslsrock",
        emoji=Icon.ROCK,
        row=0,
    )
    async def rpslsrock(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        await self.cog._outcome(
            interaction,
            self._check(Choice.ROCK),
            Icon.ROCK,
            Icon[self.computer.name],
        )
        self.value = True

    @discord.ui.button(
        label="Paper",
        style=discord.ButtonStyle.blurple,
        custom_id="rpslspaper",
        emoji=Icon.PAPER,
        row=0,
    )
    async def rpslspaper(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        await self.cog._outcome(
            interaction,
            self._check(Choice.PAPER),
            Icon.PAPER,
            Icon[self.computer.name],
        )
        self.value = True

    @discord.ui.button(
        label="Scissors",
        style=discord.ButtonStyle.blurple,
        custom_id="rpslsscissors",
        emoji=Icon.SCISSORS,
        row=0,
    )
    async def rpslsscissors(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        await self.cog._outcome(
            interaction,
            self._check(Choice.SCISSORS),
            Icon.SCISSORS,
            Icon[self.computer.name],
        )
        self.value = True

    @discord.ui.button(
        label="Lizard",
        style=discord.ButtonStyle.blurple,
        custom_id="rpslslizard",
        emoji=Icon.LIZARD,
        row=0,
    )
    async def rpslslizard(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        await self.cog._outcome(
            interaction,
            self._check(Choice.LIZARD),
            Icon.LIZARD,
            Icon[self.computer.name],
        )
        self.value = True

    @discord.ui.button(
        label="Spock",
        style=discord.ButtonStyle.blurple,
        custom_id="rpslsspock",
        emoji=Icon.SPOCK,
        row=0,
    )
    async def rpslsspock(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        await self.cog._outcome(
            interaction,
            self._check(Choice.SPOCK),
            Icon.SPOCK,
            Icon[self.computer.name],
        )
        self.value = True

    @discord.ui.button(
        label="Cancel",
        style=discord.ButtonStyle.red,
        custom_id="rpslscancel",
        emoji="\N{HEAVY MULTIPLICATION X}\N{VARIATION SELECTOR-16}",
        row=1,
    )
    async def rpslscancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await set_contextual_locales_from_guild(self.bot, interaction.guild)
        await interaction.response.defer()
        await interaction.message.edit(content=_("Very well, maybe later"), embed=None, view=None)
        self.value = False

    @discord.ui.button(
        label="Rules",
        style=discord.ButtonStyle.gray,
        custom_id="rpslsrules",
        emoji="\N{MEMO}",
        row=1,
    )
    async def rpslsrules(self, interaction: discord.Interaction, button: discord.ui.Button):
        await set_contextual_locales_from_guild(self.bot, interaction.guild)
        await interaction.response.defer()
        embed = discord.Embed()
        embed.title = _("Rock, Paper, Scissors, Lizard, Spock")
        embed.color = interaction.user.color
        embed.description = _(
            "A game of skill (chance).\n"
            "Simply select your choice and see if you can defeat the computer\n\n\n"
            "Rock {ROCK} beats Scissors {SCISSORS} and Lizard {LIZARD}\n"
            "Paper {PAPER} beats Rock {ROCK} and Spock {SPOCK}\n"
            "Scissors {SCISSORS} beats Paper {PAPER} and Lizard {LIZARD}\n"
            "Lizard {LIZARD} beats Paper {PAPER} and Spock {SPOCK}\n"
            "Spock {SPOCK} beats Rock {ROCK} and Scissors {SCISSORS}\n"
        ).format(
            ROCK=Icon.ROCK,
            PAPER=Icon.PAPER,
            SCISSORS=Icon.SCISSORS,
            LIZARD=Icon.LIZARD,
            SPOCK=Icon.SPOCK,
        )
        await interaction.followup.send(embed=embed, ephemeral=True)

    async def interaction_check(self, interaction: discord.Interaction, /) -> bool:
        return self.user == interaction.user.id

    def _check(self, choice) -> str:
        if self.computer == choice:
            return Result.TIE
        elif self.computer == Choice.ROCK:
            if choice in [Choice.SCISSORS, Choice.LIZARD]:
                return Result.LOSE
            else:
                return Result.WIN
        elif self.computer == Choice.PAPER:
            if choice in [Choice.ROCK, Choice.SPOCK]:
                return Result.LOSE
            else:
                return Result.WIN
        elif self.computer == Choice.SCISSORS:
            if choice in [Choice.PAPER, Choice.LIZARD]:
                return Result.LOSE
            else:
                return Result.WIN
        elif self.computer == Choice.LIZARD:
            if choice in [Choice.PAPER, Choice.SPOCK]:
                return Result.LOSE
            else:
                return Result.WIN
        elif self.computer == Choice.SPOCK:
            if choice in [Choice.SCISSORS, Choice.ROCK]:
                return Result.LOSE
            else:
                return Result.WIN

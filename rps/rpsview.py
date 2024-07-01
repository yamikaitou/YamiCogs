import random

import discord
from redbot.core.i18n import Translator, set_contextual_locales_from_guild

from .vars import Choice, Icon, Result

_ = Translator("RPS", __file__)


class RPSView(discord.ui.View):
    def __init__(self, cog, user):
        super().__init__(timeout=600.0)
        self.cog = cog
        self.user = user
        self.value = None
        self.computer = random.choice([Choice.ROCK, Choice.PAPER, Choice.SCISSORS])

    @discord.ui.button(
        label="Rock",
        style=discord.ButtonStyle.blurple,
        custom_id="rpsrock",
        emoji=Icon.ROCK,
        row=0,
    )
    async def rpsrock(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        await self.cog._outcome(
            interaction, self._check(Choice.ROCK), Icon.ROCK, Icon[self.computer.name]
        )
        self.value = True

    @discord.ui.button(
        label="Paper",
        style=discord.ButtonStyle.blurple,
        custom_id="rpspaper",
        emoji=Icon.PAPER,
        row=0,
    )
    async def rpspaper(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        await self.cog._outcome(
            interaction, self._check(Choice.PAPER), Icon.PAPER, Icon[self.computer.name]
        )
        self.value = True

    @discord.ui.button(
        label="Scissors",
        style=discord.ButtonStyle.blurple,
        custom_id="rpsscissors",
        emoji=Icon.SCISSORS,
        row=0,
    )
    async def rpsscissors(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        await self.cog._outcome(
            interaction,
            self._check(Choice.SCISSORS),
            Icon.SCISSORS,
            Icon[self.computer.name],
        )
        self.value = True

    @discord.ui.button(
        label="Cancel",
        style=discord.ButtonStyle.red,
        custom_id="rpscancel",
        emoji="\N{HEAVY MULTIPLICATION X}\N{VARIATION SELECTOR-16}",
        row=1,
    )
    async def rpscancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await set_contextual_locales_from_guild(self.cog.bot, interaction.guild)
        await interaction.response.defer()
        await interaction.message.edit(content=_("Very well, maybe later"), embed=None, view=None)
        self.value = False

    @discord.ui.button(
        label="Rules",
        style=discord.ButtonStyle.gray,
        custom_id="rpsrules",
        emoji="\N{MEMO}",
        row=1,
    )
    async def rpsrules(self, interaction: discord.Interaction, button: discord.ui.Button):
        await set_contextual_locales_from_guild(self.cog.bot, interaction.guild)
        await interaction.response.defer()
        embed = discord.Embed()
        embed.title = _("Rock, Paper, Scissors")
        embed.color = interaction.user.color
        embed.description = _(
            "A game of skill (chance).\n"
            "Simply select your choice and see if you can defeat the computer\n\n\n"
            "Rock {ROCK} beats Scissors {SCISSORS}\n"
            "Scissors {SCISSORS} beats Paper {PAPER}\n"
            "Paper {PAPER} beats Rock {ROCK}\n"
        ).format(ROCK=Icon.ROCK, PAPER=Icon.PAPER, SCISSORS=Icon.SCISSORS)
        await interaction.followup.send(embed=embed, ephemeral=True)

    async def interaction_check(self, interaction: discord.Interaction, /) -> bool:
        return self.user == interaction.user.id

    def _check(self, choice) -> str:
        if self.computer == choice:
            return Result.TIE
        elif self.computer == Choice.ROCK:
            if choice == Choice.SCISSORS:
                return Result.LOSE
            else:
                return Result.WIN
        elif self.computer == Choice.PAPER:
            if choice == Choice.ROCK:
                return Result.LOSE
            else:
                return Result.WIN
        elif self.computer == Choice.SCISSORS:
            if choice == Choice.PAPER:
                return Result.LOSE
            else:
                return Result.WIN

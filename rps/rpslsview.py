import random

import discord

from .vars import Result, RPSLSChoice, RPSLSIcon


class RPSLSView(discord.ui.View):
    def __init__(self, cog, user):
        super().__init__(timeout=600.0)
        self.cog = cog
        self.user = user
        self.value = None
        self.computer = random.choice(list(RPSLSChoice))

    @discord.ui.button(
        label="Rock",
        style=discord.ButtonStyle.blurple,
        custom_id="rpslsrock",
        emoji=RPSLSIcon.ROCK,
        row=0,
    )
    async def rpslsrock(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        await interaction.message.edit(
            content=f"{self._check(RPSLSChoice.ROCK)}\n\nYou {RPSLSIcon.ROCK} - {RPSLSIcon[self.computer.name]} Me",
            embed=None,
            view=None,
        )
        self.value = True

    @discord.ui.button(
        label="Paper",
        style=discord.ButtonStyle.blurple,
        custom_id="rpslspaper",
        emoji=RPSLSIcon.PAPER,
        row=0,
    )
    async def rpslspaper(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        await interaction.message.edit(
            content=f"{self._check(RPSLSChoice.PAPER)}\n\nYou {RPSLSIcon.PAPER} - {RPSLSIcon[self.computer.name]} Me",
            embed=None,
            view=None,
        )
        self.value = True

    @discord.ui.button(
        label="Scissors",
        style=discord.ButtonStyle.blurple,
        custom_id="rpslsscissors",
        emoji=RPSLSIcon.SCISSORS,
        row=0,
    )
    async def rpslsscissors(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        await interaction.message.edit(
            content=f"{self._check(RPSLSChoice.SCISSORS)}\n\nYou {RPSLSIcon.SCISSORS} - {RPSLSIcon[self.computer.name]} Me",
            embed=None,
            view=None,
        )
        self.value = True

    @discord.ui.button(
        label="Lizard",
        style=discord.ButtonStyle.blurple,
        custom_id="rpslslizard",
        emoji=RPSLSIcon.LIZARD,
        row=0,
    )
    async def rpslslizard(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        await interaction.message.edit(
            content=f"{self._check(RPSLSChoice.LIZARD)}\n\nYou {RPSLSIcon.LIZARD} - {RPSLSIcon[self.computer.name]} Me",
            embed=None,
            view=None,
        )
        self.value = True

    @discord.ui.button(
        label="Spock",
        style=discord.ButtonStyle.blurple,
        custom_id="rpslsspock",
        emoji=RPSLSIcon.SPOCK,
        row=0,
    )
    async def rpslsspock(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        await interaction.message.edit(
            content=f"{self._check(RPSLSChoice.SPOCK)}\n\nYou {RPSLSIcon.SPOCK} - {RPSLSIcon[self.computer.name]} Me",
            embed=None,
            view=None,
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
        await interaction.response.defer()
        await interaction.message.edit(content="Very well, maybe later", embed=None, view=None)
        self.value = False

    @discord.ui.button(
        label="Rules",
        style=discord.ButtonStyle.gray,
        custom_id="rpslsrules",
        emoji="\N{MEMO}",
        row=1,
    )
    async def rpslsrules(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        embed = discord.Embed()
        embed.title = "Rock, Paper, Scissors"
        embed.color = interaction.user.color
        embed.description = (
            f"A game of skill (chance).\n"
            f"Simply select your choice and see if you can defeat the computer\n\n\n"
            f"Rock {RPSLSIcon.ROCK} beats Scissors {RPSLSIcon.SCISSORS} and Lizard {RPSLSIcon.LIZARD}\n"
            f"Paper {RPSLSIcon.PAPER} beats Rock {RPSLSIcon.ROCK} and Spock {RPSLSIcon.SPOCK}\n"
            f"Scissors {RPSLSIcon.SCISSORS} beats Paper {RPSLSIcon.PAPER} and Lizard {RPSLSIcon.LIZARD}\n"
            f"Lizard {RPSLSIcon.LIZARD} beats Paper {RPSLSIcon.PAPER} and Spock {RPSLSIcon.SPOCK}\n"
            f"Spock {RPSLSIcon.SPOCK} beats Rock {RPSLSIcon.ROCK} and Scissors {RPSLSIcon.SCISSORS}\n"
        )
        await interaction.followup.send(embed=embed, ephemeral=True)

    async def interaction_check(self, interaction: discord.Interaction, /) -> bool:
        return self.user == interaction.user.id

    def _check(self, choice) -> str:
        if self.computer == choice:
            return Result.TIE
        elif self.computer == RPSLSChoice.ROCK:
            if choice in [RPSLSChoice.SCISSORS, RPSLSChoice.LIZARD]:
                return Result.LOSE
            else:
                return Result.WIN
        elif self.computer == RPSLSChoice.PAPER:
            if choice in [RPSLSChoice.ROCK, RPSLSChoice.SPOCK]:
                return Result.LOSE
            else:
                return Result.WIN
        elif self.computer == RPSLSChoice.SCISSORS:
            if choice in [RPSLSChoice.PAPER, RPSLSChoice.LIZARD]:
                return Result.LOSE
            else:
                return Result.WIN
        elif self.computer == RPSLSChoice.LIZARD:
            if choice in [RPSLSChoice.PAPER, RPSLSChoice.SPOCK]:
                return Result.LOSE
            else:
                return Result.WIN
        elif self.computer == RPSLSChoice.SPOCK:
            if choice in [RPSLSChoice.SCISSORS, RPSLSChoice.ROCK]:
                return Result.LOSE
            else:
                return Result.WIN

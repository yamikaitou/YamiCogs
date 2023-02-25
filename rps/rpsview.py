import random

import discord

from .vars import Result, RPSChoice, RPSIcon


class RPSView(discord.ui.View):
    def __init__(self, cog, user):
        super().__init__(timeout=600.0)
        self.cog = cog
        self.user = user
        self.value = None
        self.computer = random.choice(list(RPSChoice))

    @discord.ui.button(
        label="Rock",
        style=discord.ButtonStyle.blurple,
        custom_id="rpsrock",
        emoji=RPSIcon.ROCK,
        row=0,
    )
    async def rpsrock(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        await interaction.message.edit(
            content=f"{self._check(RPSChoice.ROCK)}\n\nYou {RPSIcon.ROCK} - {RPSIcon[self.computer.name]} Me",
            embed=None,
            view=None,
        )
        self.value = True

    @discord.ui.button(
        label="Paper",
        style=discord.ButtonStyle.blurple,
        custom_id="rpspaper",
        emoji=RPSIcon.PAPER,
        row=0,
    )
    async def rpspaper(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        await interaction.message.edit(
            content=f"{self._check(RPSChoice.PAPER)}\n\nYou {RPSIcon.PAPER} - {RPSIcon[self.computer.name]} Me",
            embed=None,
            view=None,
        )
        self.value = True

    @discord.ui.button(
        label="Scissors",
        style=discord.ButtonStyle.blurple,
        custom_id="rpsscissors",
        emoji=RPSIcon.SCISSORS,
        row=0,
    )
    async def rpsscissors(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        await interaction.message.edit(
            content=f"{self._check(RPSChoice.SCISSORS)}\n\nYou {RPSIcon.SCISSORS} - {RPSIcon[self.computer.name]} Me",
            embed=None,
            view=None,
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
        await interaction.response.defer()
        await interaction.message.edit(content="Very well, maybe later", embed=None, view=None)
        self.value = False

    @discord.ui.button(
        label="Rules",
        style=discord.ButtonStyle.gray,
        custom_id="rpsrules",
        emoji="\N{MEMO}",
        row=1,
    )
    async def rpsrules(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        embed = discord.Embed()
        embed.title = "Rock, Paper, Scissors"
        embed.color = interaction.user.color
        embed.description = (
            f"A game of skill (chance).\n"
            f"Simply select your choice and see if you can defeat the computer\n\n\n"
            f"Rock {RPSIcon.ROCK} beats Scissors {RPSIcon.SCISSORS}\n"
            f"Paper {RPSIcon.PAPER} beats Rock {RPSIcon.ROCK}\n"
            f"Scissors {RPSIcon.SCISSORS} beats Paper {RPSIcon.PAPER}\n"
        )
        await interaction.followup.send(embed=embed, ephemeral=True)

    async def interaction_check(self, interaction: discord.Interaction, /) -> bool:
        return self.user == interaction.user.id

    def _check(self, choice) -> str:
        if self.computer == choice:
            return Result.TIE
        elif self.computer == RPSChoice.ROCK:
            if choice == RPSChoice.SCISSORS:
                return Result.LOSE
            else:
                return Result.WIN
        elif self.computer == RPSChoice.PAPER:
            if choice == RPSChoice.ROCK:
                return Result.LOSE
            else:
                return Result.WIN
        elif self.computer == RPSChoice.SCISSORS:
            if choice == RPSChoice.PAPER:
                return Result.LOSE
            else:
                return Result.WIN

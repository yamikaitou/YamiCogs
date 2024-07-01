import discord
from redbot.core.i18n import Translator, set_contextual_locales_from_guild

from .vars import Choice, Icon, Result, RPSLSChoice, RPSLSIcon

_ = Translator("RPS", __file__)


class PlayerView(discord.ui.View):
    def __init__(self, cog, _id: int, player):
        super().__init__(timeout=300.0)
        self.cog = cog
        self._id = _id
        self.player = player
        self.value = None

    @discord.ui.button(
        label="Rock",
        style=discord.ButtonStyle.blurple,
        custom_id="rock",
        emoji=Icon.ROCK,
        row=0,
    )
    async def rock(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        await self.cog._end_game(self._id, interaction.user, Choice.ROCK, Icon.ROCK)
        await interaction.delete_original_response()
        self.value = True

    @discord.ui.button(
        label="Paper",
        style=discord.ButtonStyle.blurple,
        custom_id="paper",
        emoji=Icon.PAPER,
        row=0,
    )
    async def paper(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        await self.cog._end_game(self._id, interaction.user, Choice.PAPER, Icon.PAPER)
        await interaction.delete_original_response()
        self.value = True

    @discord.ui.button(
        label="Scissors",
        style=discord.ButtonStyle.blurple,
        custom_id="scissors",
        emoji=Icon.SCISSORS,
        row=0,
    )
    async def scissors(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        await self.cog._end_game(self._id, interaction.user, Choice.SCISSORS, Icon.SCISSORS)
        await interaction.delete_original_response()
        self.value = True

    @discord.ui.button(
        label="Lizard",
        style=discord.ButtonStyle.blurple,
        custom_id="lizard",
        emoji=Icon.LIZARD,
        row=0,
    )
    async def lizard(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        await self.cog._end_game(self._id, interaction.user, Choice.LIZARD, Icon.LIZARD)
        await interaction.delete_original_response()
        self.value = True

    @discord.ui.button(
        label="Spock",
        style=discord.ButtonStyle.blurple,
        custom_id="spock",
        emoji=Icon.SPOCK,
        row=0,
    )
    async def spock(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        await self.cog._end_game(self._id, interaction.user, Choice.SPOCK, Icon.SPOCK)
        await interaction.delete_original_response()
        self.value = True

    @discord.ui.button(
        label="Cancel",
        style=discord.ButtonStyle.red,
        custom_id="cancel",
        emoji="\N{HEAVY MULTIPLICATION X}\N{VARIATION SELECTOR-16}",
        row=1,
    )
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await set_contextual_locales_from_guild(self.bot, interaction.guild)
        await interaction.response.defer()
        await interaction.message.edit(content=_("Very well, maybe later"), embed=None, view=None)
        await self.cog._end_game(self._id, interaction.user, None, None)
        self.value = False

    @discord.ui.button(
        label="Rules",
        style=discord.ButtonStyle.gray,
        custom_id="rules",
        emoji="\N{MEMO}",
        row=1,
    )
    async def rules(self, interaction: discord.Interaction, button: discord.ui.Button):
        await set_contextual_locales_from_guild(self.bot, interaction.guild)
        embed = discord.Embed()
        embed.color = self.cog.bot.get_embed_color(interaction.channel)
        if self.cog.games[self._id]["gametype"] == "RPS":
            embed.title = _("Rock, Paper, Scissors")
            embed.description = _(
                "A game of skill (chance).\n"
                "Simply select your choice and see if you can defeat the computer\n\n\n"
                "Rock {ROCK} beats Scissors {SCISSORS}\n"
                "Scissors {SCISSORS} beats Paper {PAPER}\n"
                "Paper {PAPER} beats Rock {ROCK}\n"
            ).format(ROCK=Icon.ROCK, PAPER=Icon.PAPER, SCISSORS=Icon.SCISSORS)
        elif self.cog.games[self._id]["gametype"] == "RPSLS":
            embed.title = _("Rock, Paper, Scissors, Lizard, Spock")
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
        await interaction.response.send_message(embed=embed, ephemeral=True)

    async def interaction_check(self, interaction: discord.Interaction, /) -> bool:
        return self.player.id == interaction.user.id

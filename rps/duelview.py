import discord
from redbot.core.i18n import Translator, set_contextual_locales_from_guild

from .vars import Result, RPSLSChoice, RPSLSIcon

from .playerview import PlayerView

_ = Translator("RPS", __file__)


class DuelView(discord.ui.View):
    def __init__(self, cog, _id: int):
        super().__init__(timeout=600.0)
        self.cog = cog
        self._id = _id
        self.value = None

    async def interaction_check(self, interaction: discord.Interaction, /) -> bool:
        if (
            self.cog.games[self._id]["p1"].id == interaction.user.id
            or self.cog.games[self._id]["p2"].id == interaction.user.id
        ):
            return True
        else:
            await set_contextual_locales_from_guild(self.bot, self.games[id]["original"].guild)
            await interaction.response.send_message(
                content=_("Sorry, but you are not in this duel"), ephemeral=True
            )
            return False

    @discord.ui.button(
        label="Accept",
        style=discord.ButtonStyle.green,
        custom_id="duelaccept",
        emoji="\N{HEAVY CHECK MARK}\N{VARIATION SELECTOR-16}",
        row=0,
    )
    async def duelaccept(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self.cog.games[self._id]["p1"].id:
            await set_contextual_locales_from_guild(self.bot, self.games[id]["original"].guild)
            await interaction.response.send_message(
                _("You have already accepted it by starting the duel."), ephemeral=True
            )

        view = PlayerView(self.cog, self._id, interaction.user)
        if self.cog[self._id]["gametype"] == "RPS":
            view = view.remove_item(view.children[3]).remove_item(view.children[3])

        await interaction.response.send_message(view=view, ephemeral=True)

    @discord.ui.button(
        label="Decline",
        style=discord.ButtonStyle.red,
        custom_id="dueldecline",
        emoji="\N{HEAVY MULTIPLICATION X}\N{VARIATION SELECTOR-16}",
        row=0,
    )
    async def dueldecline(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.response.defer()
        await set_contextual_locales_from_guild(self.bot, self.games[id]["original"].guild)
        await self.cog.games[self._id]["original"].edit_original_response(
            content=_("Duel has been rejected"), embed=None, view=None
        )
        del self.cog.games[self._id]

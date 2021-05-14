from typing import Literal

from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.config import Config

RequestType = Literal["discord_deleted_user", "owner", "user", "user_strict"]


class Runes(commands.Cog):
    """
    Runes of the Falrek
    A card collecting game
    """

    def __init__(self, bot: Red) -> None:
        self.bot = bot
        self.config = Config.get_conf(
            self,
            identifier=582650109,
            force_registration=True,
        )
        self.bot.loop.create_task(self.init())

    async def init(self):
        if self.bot.user.id != 812811324001615883:
            await self.bot.send_to_owners(
                "Greetings from the Runes cog!\nThis cog is not in a usable state by the public at this time, so I've unloaded myself.\nYou are welcome to submit feedback and suggestions on the cog while it is in development though.\nYou can use the cog in Red's #testing channel, just run `<runes alpha` for the usable commands."
            )
            await self.bot.get_cog("Core")._unload(["runes"])

    async def red_delete_data_for_user(self, *, requester: RequestType, user_id: int) -> None:
        # TODO: Replace this with the proper end user data removal handling.
        super().red_delete_data_for_user(requester=requester, user_id=user_id)

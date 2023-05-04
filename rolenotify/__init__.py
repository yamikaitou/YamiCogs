import json
from pathlib import Path

from redbot.core.bot import Red
from redbot.core.errors import CogLoadError

from .rolenotify import RoleNotify

with open(Path(__file__).parent / "info.json") as fp:
    __red_end_user_data_statement__ = json.load(fp)["end_user_data_statement"]


async def setup(bot: Red) -> None:
    if bot.intents.members:
        await bot.add_cog(RoleNotify(bot))
    else:
        raise CogLoadError("This cog requires the Members Intent to be enabled")

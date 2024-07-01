import json
from pathlib import Path

from redbot.core.bot import Red

from .ping import Ping

with open(Path(__file__).parent / "info.json") as fp:
    __red_end_user_data_statement__ = json.load(fp)["end_user_data_statement"]


old_ping = None

async def setup(bot: Red) -> None:
    global old_ping
    old_ping = bot.get_command("ping")
    if old_ping:
        bot.remove_command(old_ping.name)
    
    cog = Ping(bot)
    await bot.add_cog(cog)

def teardown(bot: Red) -> None:
    global old_ping
    if old_ping:
        bot.remove_command("ping")
        bot.add_command(old_ping)
import json
from asyncio import create_task
from pathlib import Path

from .rps import RPS

with open(Path(__file__).parent / "info.json") as fp:
    __red_end_user_data_statement__ = json.load(fp)["end_user_data_statement"]

old_rps = None

async def setup(bot):
    global old_rps
    old_rps = bot.get_command("rps")
    if old_rps:
        bot.remove_command(old_rps.name)
    
    cog = RPS(bot)
    await bot.add_cog(cog)

async def teardown(bot):
    global old_rps
    if old_rps:
        bot.remove_command("rps")
        bot.add_command(old_rps)

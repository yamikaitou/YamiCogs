import json
from asyncio import create_task
from pathlib import Path

from .rps import RPS

with open(Path(__file__).parent / "info.json") as fp:
    __red_end_user_data_statement__ = json.load(fp)["end_user_data_statement"]

old_rps = None

# Thanks flare


async def setup(bot):
    create_task(setup_after_ready(bot))


async def setup_after_ready(bot):
    global old_rps
    await bot.wait_until_red_ready()
    cog = RPS(bot)

    old_rps = bot.get_command("rps")
    if old_rps:
        bot.remove_command(old_rps.name)

    await bot.add_cog(cog)


async def teardown(bot):
    bot.add_command(old_rps)

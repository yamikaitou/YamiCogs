import json

import aiohttp
from discord.ext import tasks
from redbot.core import Config, commands


class PokemonGo(commands.Cog):
    """
    Pokemon Go stats
    """

    __version__ = "0.1"

    def format_help_for_context(self, ctx):
        """Thanks Sinbad."""
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\nCog Version: {self.__version__}"

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=582650109, force_registration=True)

        self.config.register_global(**{"version": 0})

        self.db_check.start()

    def cog_unload(self):
        self.db_check.cancel()

    @tasks.loop(seconds=10)
    async def db_check(self):
        async with aiohttp.ClientSession(json_serialize=json.dumps) as session:
            async with session.get(
                "https://cdn.yamikaitou.dev/cogs/pogo/timestamp.txt"
            ) as response:
                if 400 <= response.status < 600:
                    print(f"{response.status}")
                    return

                version = int(await response.content.read(1024))
                if version > await self.config.version():
                    await self.config.version.set(version)
                    print("Update found, fetching")

    @db_check.before_loop
    async def before_db_check(self):
        await self.bot.wait_until_red_ready()

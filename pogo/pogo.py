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


if "sequence_" in entry["templateId"]:
    continue
elif "camera_" in entry["templateId"]:
    continue
elif "VS_SEEKER_" in entry["templateId"]:
    continue
elif "bundle." in entry["templateId"]:
    continue
elif "itemleadermap" in entry["templateId"]:
    continue
elif "deep_linking_" in entry["templateId"]:
    continue
elif "general1." in entry["templateId"]:
    continue
elif "hometransport." in entry["templateId"]:
    continue
elif "adventure_sync_" in entry["templateId"]:
    continue
elif "STICKER_" in entry["templateId"]:
    continue
elif "SPONSORED_" in entry["templateId"]:
    continue
elif "TRAINER_" in entry["templateId"]:
    continue
elif "SPAWN_" in entry["templateId"]:
    continue
elif "V0421_CHERRIM_HOME_FORM_REVERSION" in entry["templateId"]:
    continue
elif "RECOMMENDED_" in entry["templateId"]:
    continue
elif "QUEST_" in entry["templateId"]:
    continue
elif "ITEM_" in entry["templateId"]:
    continue
elif "IAP_" in entry["templateId"]:
    continue
elif "FRIENDSHIP_" in entry["templateId"]:
    continue
elif "GYM_" in entry["templateId"]:
    continue
elif "POKEMON_SCALE" in entry["templateId"]:
    continue
elif "INVASION_" in entry["templateId"]:
    continue
elif "CHARACTER_" in entry["templateId"]:
    continue
elif "BUDDY_" in entry["templateId"]:
    continue
elif "BADGE_" in entry["templateId"]:
    continue
elif "AVATAR_" in entry["templateId"]:
    continue
elif "AWARDS_" in entry["templateId"]:
    continue
elif "EVOLUTION_QUEST" in entry["templateId"]:
    continue
elif "RAID_" in entry["templateId"]:
    continue
elif "POKECOIN_" in entry["templateId"]:
    continue
elif "PLAYER_" in entry["templateId"]:
    continue
elif "COMBAT_" in entry["templateId"]:
    continue

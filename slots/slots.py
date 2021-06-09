import pprint
import asyncio
import logging
import random
import re
import unicodedata
from collections import deque

import discord
import yaml
from redbot.core import commands, data_manager
from redbot.core.bot import Red
from redbot.core.config import Config

from . import errors

log = logging.getLogger("red.yamicogs.slots")
DISCORD_EMOJI_RE = re.compile(r"(<?(a)?:([0-9a-zA-Z\-_]+):([0-9]+)?>?)")


class Slots(commands.Cog):
    """
    Various Slot Machine games
    """

    def __init__(self, bot: Red) -> None:
        self.bot = bot
        self.config = Config.get_conf(
            self,
            identifier=582650109,
            force_registration=True,
        )

        self.config.register_global(**{"machines": ["local/fruits.yaml", "local/sports.yaml"]})

        self.slot_machines = {}
        self.bot.loop.create_task(self._load_machines())

    async def _load_machines(self):
        await self.bot.wait_until_red_ready()

        machines = await self.config.machines()
        for machine_str in machines:
            location, filename = machine_str.split("/")
            if location == "local":
                machine = yaml.safe_load(open(data_manager.bundled_data_path(self) / filename))
                print(machine_str)
                pprint.pprint(await self._validate_machine(machine))
                self.slot_machines[machine["name"].lower()] = await self._load_machine(machine)

    async def _validate_machine(self, machine):
        error = []
        if "cost" not in machine:
            error.append(errors.MachineMissingCost("Required Option is missing (cost)"))
        if not isinstance(machine["cost"], int):
            error.append(errors.ValidateTypeCost("cost must be a number"))

        if "description" not in machine:
            error.append(
                errors.MachineMissingDescription("Required Option is missing (description)")
            )

        if "name" not in machine:
            error.append(errors.MachineMissingName("Required Option is missing (name)"))

        if "randomize" in machine:
            if not isinstance(machine["randomize"], bool):
                error.append(
                    errors.ValidateTypeRandomize("randomize must be either true or false")
                )

        if "prizes" not in machine:
            error.append(errors.MachineMissingPrizes("Required Option is missing (prizes)"))
        else:
            for k, v in machine["prizes"].items():
                if not isinstance(k, int):
                    error.append(
                        errors.ValidateTypePrizeKey(f"Prize Keys should be numbers ({k})")
                    )

                if "name" not in v:
                    error.append(errors.PrizeMissingName(f"Prize is missing a name ({k})"))

                if "prize" not in v:
                    error.append(errors.PrizeMissingAmount(f"Prize is missing an amount ({k})"))
                if not isinstance(v["prize"], int):
                    error.append(
                        errors.ValidateTypePrizeAmount(f"Prize amount must be a number ({k})")
                    )

                if not (v["name"] != "Match 2" or v["name"] != "Match 3") and "pattern" not in v:
                    error.append(errors.PrizeMissingPattern(f"Prize is missing a pattern ({k})"))

        if "icons" not in machine:
            error.append(errors.MachineMissingReels("Required Option is missing (icons)"))
        else:
            for k, v in machine["icons"].items():

                if "name" not in v:
                    error.append(errors.ReelSlotMissingName(f"Icon is missing a name ({k})"))

                if "emoji" not in v:
                    error.append(errors.ReelSlotMissingEmoji(f"Icon is missing an emoji ({k})"))
                for match in DISCORD_EMOJI_RE.finditer(v["emoji"]):
                    if discord.utils.get(self.bot.emojis, name=match.group(3)) is None:
                        error.append(
                            errors.ReelSlotEmojiUnusable(f"Icon Emoji is not usable ({k})")
                        )

        return error

    async def _load_machine(self, machine):

        return

    async def _play_game(self, game):
        reel = deque()
        for slot in game["slots"].values():
            reel.append(slot["emoji"])

        reels = []
        for k in range(3):  # pylint:disable=unused-variable
            reel.rotate(random.randint(-999, 999))
            reels.append(deque(reel, maxlen=3))

        return reels

    @commands.bot_has_permissions(embed_links=True)
    @commands.group(name="slots", invoke_without_command=True)
    async def slots(self, ctx):
        embed = discord.Embed()
        embed.title = "Slot Machine Alley"
        embed.description = (
            "Welcome to Slot Machine Alley.\n\nEnjoy your stay and watch your credits."
        )

        for machine in self.slot_machines.values():
            embed.add_field(
                name=machine["name"],
                value=f"{machine['description']}\n{machine['cost']} credits per spin\n`{ctx.prefix}slots play {machine['name'].lower()}` to play",
                inline=False,
            )
        await ctx.send(embed=embed)

    @slots.command(name="play", usage="<machine>")
    async def slots_play(self, ctx, choice):
        """
        Play a slot machine

        See all the available games in `[p]slots`
        """

        try:
            machine = self.slot_machines[choice.lower()]
        except KeyError:
            return await ctx.send(
                f"Unknown machine, please refer to `{ctx.prefix}slots` for the available games"
            )

        embed = discord.Embed()
        embed.title = "Slot Machine - " + machine["name"]
        embed.description = "Lets spin those reels\n\n*click click click*"
        embed.color = discord.Color.blurple()
        msg = await ctx.send(embed=embed)

        await asyncio.sleep(2)
        slots = await self._play_game(machine)
        embed.add_field(
            name="Outcome",
            value=(
                f"⏹️ {slots[0][0]}{slots[1][0]}{slots[2][0]}\n"
                f"▶️ {slots[0][1]}{slots[1][1]}{slots[2][1]}\n"
                f"⏹️ {slots[0][2]}{slots[1][2]}{slots[2][2]}\n"
            ),
        )
        embed.description = (
            "Winner!!!"
            if (slots[0][1] == slots[1][1] and slots[1][1] == slots[2][1])
            else "Loser!!!"
        )
        embed.color = discord.Color.green()
        await msg.edit(embed=embed)

    async def red_get_data_for_user(self, *, user_id: int):
        # this cog does not store any user data
        return {}

    async def red_delete_data_for_user(self, *, requester, user_id: int) -> None:
        # this cog does not store any user data
        pass

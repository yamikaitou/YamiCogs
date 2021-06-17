import asyncio
import logging
import random
import re
import unicodedata
from collections import deque

import discord
import yaml
from dislash import *  # pylint:disable=unused-wildcard-import
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

        self.config.register_global(
            **{"machines": ["local/fruits.yaml"]}
        )  # , "local/sports.yaml"]})
        self.config.register_user(**{"playing": False})

        self.slot_machines = {}
        self.bot.loop.create_task(self._load_machines())

    async def _load_machines(self):
        await self.bot.wait_until_red_ready()

        machines = await self.config.machines()
        for machine_str in machines:
            location, filename = machine_str.split("/")
            if location == "local":
                machine = yaml.safe_load(open(data_manager.bundled_data_path(self) / filename))
                errors = await self._validate_machine(machine)
                if errors == []:
                    self.slot_machines[machine["name"].lower()] = machine
                else:
                    log.info(f"Failed to parse slot machine {filename}")
                    log.debug(errors)
            else:
                machine = yaml.safe_load(open(data_manager.bundled_data_path(self) / filename))
                errors = await self._validate_machine(machine)
                if errors == []:
                    self.slot_machines[machine["name"].lower()] = machine
                else:
                    log.info(f"Failed to parse slot machine {filename}")
                    log.debug(errors)

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

    async def _load_machine(self, source, filename):

        if source == "local":
            machine = yaml.safe_load(open(data_manager.bundled_data_path(self) / filename))
        else:
            machine = yaml.safe_load(open(data_manager.cog_data_path(self) / filename))
        errors = await self._validate_machine(machine)
        if errors == []:
            self.slot_machines[machine["name"].lower()] = machine
        else:
            log.info(f"Failed to parse slot machine {filename}")
            log.debug(errors)

        return errors

    async def _play_game(self, game):
        reel = deque()
        for slot in game["icons"].values():
            reel.append([slot["name"], slot["emoji"]])

        reels = []
        for k in range(3):  # pylint:disable=unused-variable
            reel.rotate(random.randint(-999, 999))
            reels.append(deque(reel, maxlen=3))

        return reels

    @commands.bot_has_permissions(embed_links=True)
    @commands.command(name="slots")
    async def slots(self, ctx, bid: int = 0):
        """
        Play some slot games

        Not providing a bid will cause you to bid at the machines default amount
        """
        embed = discord.Embed()
        embed.title = "Slot Machine Alley"
        embed.description = (
            "Welcome to Slot Machine Alley.\n\nEnjoy your stay and watch your credits."
        )

        buttons = []
        for machine in self.slot_machines.values():
            if bid != 0:
                machine["cost"] = bid
            embed.add_field(
                name=machine["name"],
                value=f"{machine['description']}\n{machine['cost']} credits per spin\n",
                inline=False,
            )
            buttons.append(
                Button(
                    style=ButtonStyle.blurple,
                    label=machine["name"],
                    custom_id=machine["name"].lower(),
                )
            )
        msg = await ctx.send(embed=embed, components=auto_rows(*buttons, max_in_row=5))

        def check(inter):
            return inter.author == ctx.author

        inter = await msg.wait_for_button_click(check=check)

        try:
            machine = self.slot_machines[inter.clicked_button.custom_id]
            if bid != 0:
                machine["cost"] = bid
        except KeyError:
            await inter.reply(
                f"That machine somehow doesn't exist", type=ResponseType.UpdateMessage
            )
            await msg.edit(components=None, embed=None)
        else:
            await inter.reply(type=ResponseType.DeferredUpdateMessage)
            await self._slots_play(ctx, machine, msg)

    async def _slots_play(self, ctx, machine, msg):

        embed = discord.Embed()
        embed.title = "Slot Machine - " + machine["name"]
        embed.description = "Lets spin those reels"
        embed.color = discord.Color.blurple()
        winnings = 0

        def button_check(inter):
            if inter.author != ctx.author:
                self.bot.loop.create_task(
                    inter.reply(
                        f"Sorry, this is not your game to play, try launching your own with `{ctx.prefix}slots`",
                        ephemeral=True,
                    )
                )
                return False

            if inter.clicked_button.custom_id == "dead":
                self.bot.loop.create_task(
                    inter.reply(
                        f"Sorry, but clicking on the slot icons doesn't do anything",
                        ephemeral=True,
                    )
                )
                return False

            if inter.clicked_button.custom_id == "coins":
                self.bot.loop.create_task(
                    inter.reply(
                        f"This is the amount of credits you have gained/lost during this session",
                        ephemeral=True,
                    )
                )
                return False

            return True

        while True:
            slots = await self._play_game(machine)

            if len(embed.fields) == 0:
                outcome_field = embed.insert_field_at
            else:
                outcome_field = embed.set_field_at

            outcome = await self._check_outcome(machine, slots)
            if outcome is False:
                winnings -= machine["cost"]
                outcome_field(0, name="Outcome", value="No matches, try again!")
            else:
                winnings += outcome[1]
                outcome_field(
                    0, name="Outcome", value=f"Winner!! {outcome[0]}\n+ {outcome[1]} credits"
                )

            buttons = [
                ActionRow(
                    Button(
                        style=ButtonStyle.gray,
                        disabled=False,
                        emoji="\N{BLACK SQUARE FOR STOP}\N{VARIATION SELECTOR-16}",
                        custom_id="dead",
                    ),
                    Button(
                        style=ButtonStyle.gray,
                        disabled=False,
                        emoji=slots[0][0][1],
                        custom_id="dead",
                    ),
                    Button(
                        style=ButtonStyle.gray,
                        disabled=False,
                        emoji=slots[1][0][1],
                        custom_id="dead",
                    ),
                    Button(
                        style=ButtonStyle.gray,
                        disabled=False,
                        emoji=slots[2][0][1],
                        custom_id="dead",
                    ),
                    Button(
                        style=ButtonStyle.green,
                        label="Spin",
                        custom_id="spin",
                    ),
                ),
                ActionRow(
                    Button(
                        style=ButtonStyle.gray,
                        disabled=False,
                        emoji="\N{BLACK RIGHT-POINTING TRIANGLE}\N{VARIATION SELECTOR-16}",
                        custom_id="dead",
                    ),
                    Button(
                        style=ButtonStyle.gray,
                        disabled=False,
                        emoji=slots[0][1][1],
                        custom_id="dead",
                    ),
                    Button(
                        style=ButtonStyle.gray,
                        disabled=False,
                        emoji=slots[1][1][1],
                        custom_id="dead",
                    ),
                    Button(
                        style=ButtonStyle.gray,
                        disabled=False,
                        emoji=slots[2][1][1],
                        custom_id="dead",
                    ),
                    Button(
                        style=ButtonStyle.red,
                        label="Exit",
                        custom_id="cancel",
                    ),
                ),
                ActionRow(
                    Button(
                        style=ButtonStyle.gray,
                        disabled=False,
                        emoji="\N{BLACK SQUARE FOR STOP}\N{VARIATION SELECTOR-16}",
                        custom_id="dead",
                    ),
                    Button(
                        style=ButtonStyle.gray,
                        disabled=False,
                        emoji=slots[0][2][1],
                        custom_id="dead",
                    ),
                    Button(
                        style=ButtonStyle.gray,
                        disabled=False,
                        emoji=slots[1][2][1],
                        custom_id="dead",
                    ),
                    Button(
                        style=ButtonStyle.gray,
                        disabled=False,
                        emoji=slots[2][2][1],
                        custom_id="dead",
                    ),
                    Button(
                        style=ButtonStyle.blurple,
                        disabled=False,
                        emoji="\U0001fa99",
                        label=winnings,
                        custom_id="coins",
                    ),
                ),
            ]

            await msg.edit(embed=embed, components=buttons)

            try:
                inter = await msg.wait_for_button_click(check=button_check, timeout=60)
            except asyncio.TimeoutError:
                await msg.edit(
                    content="Okay then, see ya later!\nYou have {} {} credits this session".format(
                        ("lost" if winnings < 0 else "won"), abs(winnings)
                    ),
                    components=None,
                    embed=None,
                )
                return

            if inter.clicked_button.custom_id == "cancel":
                await inter.reply(
                    "Okay then, see ya later!\nYou have {} {} credits this session".format(
                        ("lost" if winnings < 0 else "won"), abs(winnings)
                    ),
                    type=ResponseType.UpdateMessage,
                )
                await msg.edit(components=None, embed=None)
                return

            await inter.reply(type=ResponseType.DeferredUpdateMessage)

    async def _check_outcome(self, machine, reels):
        table = machine["prizes"]

        for k in sorted(table.keys(), reverse=True):
            try:
                pattern = table[k]["pattern"]

                if (
                    reels[0][1][0] == pattern[0]
                    and reels[1][1][0] == pattern[1]
                    and reels[2][1][0] == pattern[2]
                ):
                    return (table[k]["name"], machine["cost"] * table[k]["prize"])
            except KeyError:
                if table[k]["name"] == "Match 3":
                    if reels[0][1][0] == reels[1][1][0] == reels[2][1][0]:
                        return (table[k]["name"], machine["cost"] * table[k]["prize"])
                if table[k]["name"] == "Match 2":
                    if (
                        reels[0][1][0] == reels[1][1][0]
                        or reels[0][1][0] == reels[2][1][0]
                        or reels[1][1][0] == reels[2][1][0]
                    ):
                        return (table[k]["name"], machine["cost"] * table[k]["prize"])

        return False

    async def red_get_data_for_user(self, *, user_id: int):
        # this cog does not store any user data
        return {}

    async def red_delete_data_for_user(self, *, requester, user_id: int) -> None:
        # this cog does not store any user data
        pass

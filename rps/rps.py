import logging
import random
from typing import Literal

import discord
from dislash import *  # pylint:disable=unused-wildcard-import
from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.config import Config

log = logging.getLogger("red.yamicogs.rps")

RequestType = Literal["discord_deleted_user", "owner", "user", "user_strict"]

ICONS_RPS = {
    "rock": "\U0001faa8",
    "paper": "\N{NEWSPAPER}",
    "scissors": "\N{BLACK SCISSORS}\N{VARIATION SELECTOR-16}",
}
ICONS_RPSLS = {
    "rock": "\U0001faa8",
    "paper": "\N{NEWSPAPER}",
    "scissors": "\N{BLACK SCISSORS}\N{VARIATION SELECTOR-16}",
    "lizard": "\N{LIZARD}",
    "spock": "\N{RAISED HAND WITH PART BETWEEN MIDDLE AND RING FINGERS}",
}


class RPS(commands.Cog):
    """
    Rock, Paper, Scissors (Lizard, Spock)

    More detailed docs: <https://cogs.yamikaitou.dev/rps.html>
    """

    def __init__(self, bot: Red) -> None:
        self.bot = bot
        self.config = Config.get_conf(
            self,
            identifier=582650109,
            force_registration=True,
        )

    @commands.command(name="rpsrules", aliases=["rpslsrules"])
    async def _rps_rules(self, ctx):
        """Rules of Rock, Paper, Scissors (Lizard, Spock)"""

        embed = discord.Embed()
        embed.title = "Rock, Paper, Scissors (Lizard, Spock)"
        embed.color = await ctx.embed_color()
        embed.description = (
            f"A game of skill (chance).\n"
            f"Simply select your choice and see if you can defeat he computer\n\n"
            f"2 versions are includes, the rules are below\n"
        )
        embed.add_field(
            name="Rock, Paper, Scissors",
            inline=False,
            value=(
                f"Rock {ICONS_RPS['rock']} beats Scissors {ICONS_RPS['scissors']}\n"
                f"Scissors {ICONS_RPS['scissors']} beats Paper {ICONS_RPS['paper']}\n"
                f"Paper {ICONS_RPS['paper']} beats Rock {ICONS_RPS['rock']}\n\n"
                f"Play with `{ctx.prefix}rps`\n"
            ),
        )
        embed.add_field(
            name="Rock, Paper, Scissors, Lizard, Spock",
            inline=False,
            value=(
                f"Rock {ICONS_RPSLS['rock']} beats Scissors {ICONS_RPSLS['scissors']} and Lizard {ICONS_RPSLS['lizard']}\n"
                f"Paper {ICONS_RPSLS['paper']} beats Rock {ICONS_RPSLS['rock']} and Spock {ICONS_RPSLS['spock']}\n"
                f"Scissors {ICONS_RPSLS['scissors']} beats Paper {ICONS_RPSLS['paper']} and Lizard {ICONS_RPSLS['lizard']}\n"
                f"Lizard {ICONS_RPSLS['lizard']} beats Paper {ICONS_RPSLS['paper']} and Spock {ICONS_RPSLS['spock']}\n"
                f"Spock {ICONS_RPSLS['spock']} beats Rock {ICONS_RPSLS['rock']} and Scissors {ICONS_RPSLS['scissors']}\n\n"
                f"Play with `{ctx.prefix}rpsls`\n"
            ),
        )

        await ctx.send(embed=embed)

    @commands.command(name="rps")
    async def _rps(self, ctx):
        """Play a game of Rock, Paper, Scissors"""
        row_of_buttons = [
            ActionRow(
                Button(
                    style=ButtonStyle.blurple,
                    label="Rock",
                    emoji=discord.PartialEmoji(name="\U0001faa8"),
                    custom_id="rock",
                ),
                Button(
                    style=ButtonStyle.blurple,
                    label="Paper",
                    emoji=discord.PartialEmoji(name="\N{NEWSPAPER}"),
                    custom_id="paper",
                ),
                Button(
                    style=ButtonStyle.blurple,
                    label="Scissors",
                    emoji=discord.PartialEmoji(name="\N{BLACK SCISSORS}\N{VARIATION SELECTOR-16}"),
                    custom_id="scissors",
                ),
            ),
            ActionRow(
                Button(
                    style=ButtonStyle.red,
                    label="Cancel",
                    custom_id="cancel",
                ),
                Button(
                    style=ButtonStyle.gray,
                    label="Rules",
                    emoji=discord.PartialEmoji(name="\N{MEMO}"),
                    custom_id="rules",
                ),
            ),
        ]
        msg = await ctx.reply(
            "Let's play!",
            components=row_of_buttons,
            mention_author=False,
        )
        computer = random.choice(["rock", "paper", "scissors"])

        on_click = msg.create_click_listener(timeout=60)
        dead = False

        def is_not_author(inter):
            # Note that this check must take only 1 arg
            return inter.author != ctx.author

        @on_click.matching_condition(is_not_author, cancel_others=True)
        async def on_wrong_user(inter):
            # Reply with a hidden message
            await inter.reply(
                f"Sorry, this is not your game to play, try launching your own with `{ctx.prefix}rps`",
                ephemeral=True,
            )

        @on_click.matching_id("rock", cancel_others=True)
        async def on_rock(inter):
            await inter.reply(type=ResponseType.DeferredUpdateMessage)
            if computer == "rock":
                await msg.edit(
                    content=f"Well, we must be mind-readers!\n\nYou {ICONS_RPS['rock']} - {ICONS_RPS[computer]} Me",
                    components=None,
                )
            elif computer == "paper":
                await msg.edit(
                    content=f"Look at that, I win!\n\nYou {ICONS_RPS['rock']} - {ICONS_RPS[computer]} Me",
                    components=None,
                )
            else:
                await msg.edit(
                    content=f"Congrats, you win!\n\nYou {ICONS_RPS['rock']} - {ICONS_RPS[computer]} Me",
                    components=None,
                )
            global dead
            dead = True

        @on_click.matching_id("paper", cancel_others=True)
        async def on_paper(inter):
            await inter.reply(type=ResponseType.DeferredUpdateMessage)
            if computer == "rock":
                await msg.edit(
                    content=f"Congrats, you win!\n\nYou {ICONS_RPS['paper']} - {ICONS_RPS[computer]} Me",
                    components=None,
                )
            elif computer == "paper":
                await msg.edit(
                    content=f"Well, we must be mind-readers!\n\nYou {ICONS_RPS['paper']} - {ICONS_RPS[computer]} Me",
                    components=None,
                )
            else:
                await msg.edit(
                    content=f"Look at that, I win!\n\nYou {ICONS_RPS['paper']} - {ICONS_RPS[computer]} Me",
                    components=None,
                )
            global dead
            dead = True

        @on_click.matching_id("scissors", cancel_others=True)
        async def on_scissors(inter):
            await inter.reply(type=ResponseType.DeferredUpdateMessage)
            if computer == "rock":
                await msg.edit(
                    content=f"Look at that, I win!\n\nYou {ICONS_RPS['scissors']} - {ICONS_RPS[computer]} Me",
                    components=None,
                )
            elif computer == "paper":
                await msg.edit(
                    content=f"Congrats, you win!\n\nYou {ICONS_RPS['scissors']} - {ICONS_RPS[computer]} Me",
                    components=None,
                )
            else:
                await msg.edit(
                    content=f"Well, we must be mind-readers!\n\nYou {ICONS_RPS['scissors']} - {ICONS_RPS[computer]} Me",
                    components=None,
                )
            global dead
            dead = True

        @on_click.matching_id("rules", cancel_others=False, reset_timeout=True)
        async def on_rules(inter):
            embed = discord.Embed()
            embed.title = "Rock, Paper, Scissors"
            embed.color = await ctx.embed_color()
            embed.description = (
                f"A game of skill (chance).\n"
                f"Simply select your choice and see if you can defeat he computer\n\n\n"
                f"Rock {ICONS_RPS['rock']} beats Scissors {ICONS_RPS['scissors']}\n"
                f"Paper {ICONS_RPS['paper']} beats Rock {ICONS_RPS['rock']}\n"
                f"Scissors {ICONS_RPS['scissors']} beats Paper {ICONS_RPS['paper']}\n"
            )
            await inter.reply(embed=embed, ephemeral=True)

        @on_click.matching_id("cancel", cancel_others=False)
        async def on_cancel(inter):
            await inter.reply(type=ResponseType.DeferredUpdateMessage)
            await msg.edit(content="Very well, maybe later", components=None)

        @on_click.timeout
        async def on_timeout():
            global dead
            if not dead:
                await msg.edit(content="Okay then, maybe later", components=None)

    @commands.command(name="rpsls")
    async def _rpsls(self, ctx):
        """Play a game of Rock, Paper, Scissors, Lizard, Spock"""
        row_of_buttons = [
            ActionRow(
                Button(
                    style=ButtonStyle.blurple,
                    label="Rock",
                    emoji=discord.PartialEmoji(name="\U0001faa8"),
                    custom_id="rock",
                ),
                Button(
                    style=ButtonStyle.blurple,
                    label="Paper",
                    emoji=discord.PartialEmoji(name="\N{NEWSPAPER}"),
                    custom_id="paper",
                ),
                Button(
                    style=ButtonStyle.blurple,
                    label="Scissors",
                    emoji=discord.PartialEmoji(name="\N{BLACK SCISSORS}\N{VARIATION SELECTOR-16}"),
                    custom_id="scissors",
                ),
                Button(
                    style=ButtonStyle.blurple,
                    label="Lizard",
                    emoji=discord.PartialEmoji(name="\N{LIZARD}"),
                    custom_id="lizard",
                ),
                Button(
                    style=ButtonStyle.blurple,
                    label="Spock",
                    emoji=discord.PartialEmoji(
                        name="\N{RAISED HAND WITH PART BETWEEN MIDDLE AND RING FINGERS}"
                    ),
                    custom_id="spock",
                ),
            ),
            ActionRow(
                Button(
                    style=ButtonStyle.red,
                    label="Cancel",
                    custom_id="cancel",
                ),
                Button(
                    style=ButtonStyle.gray,
                    label="Rules",
                    emoji=discord.PartialEmoji(name="\N{MEMO}"),
                    custom_id="rules",
                ),
            ),
        ]
        msg = await ctx.reply(
            "Let's play!",
            components=row_of_buttons,
            mention_author=False,
        )
        computer = random.choice(["rock", "paper", "scissors", "lizard", "spock"])

        on_click = msg.create_click_listener(timeout=60)
        dead = False

        def is_not_author(inter):
            # Note that this check must take only 1 arg
            return inter.author != ctx.author

        @on_click.matching_condition(is_not_author, cancel_others=True)
        async def on_wrong_user(inter):
            # Reply with a hidden message
            await inter.reply(
                f"Sorry, this is not your game to play, try launching your own with `{ctx.prefix}rpsls`",
                ephemeral=True,
            )

        @on_click.matching_id("rock", cancel_others=True)
        async def on_rock(inter):
            await inter.reply(type=ResponseType.DeferredUpdateMessage)
            if computer == "rock":
                await msg.edit(
                    content=f"Well, we must be mind-readers!\n\nYou {ICONS_RPSLS['rock']} - {ICONS_RPSLS[computer]} Me",
                    components=None,
                )
            elif computer == "paper":
                await msg.edit(
                    content=f"Look at that, I win!\n\nYou {ICONS_RPSLS['rock']} - {ICONS_RPSLS[computer]} Me",
                    components=None,
                )
            elif computer == "scissors":
                await msg.edit(
                    content=f"Congrats, you win!\n\nYou {ICONS_RPSLS['rock']} - {ICONS_RPSLS[computer]} Me",
                    components=None,
                )
            elif computer == "lizard":
                await msg.edit(
                    content=f"Congrats, you win!\n\nYou {ICONS_RPSLS['rock']} - {ICONS_RPSLS[computer]} Me",
                    components=None,
                )
            else:  # computer == 'spock'
                await msg.edit(
                    content=f"Look at that, I win!\n\nYou {ICONS_RPSLS['rock']} - {ICONS_RPSLS[computer]} Me",
                    components=None,
                )
            global dead
            dead = True

        @on_click.matching_id("paper", cancel_others=True)
        async def on_paper(inter):
            await inter.reply(type=ResponseType.DeferredUpdateMessage)
            if computer == "rock":
                await msg.edit(
                    content=f"Congrats, you win!\n\nYou {ICONS_RPSLS['paper']} - {ICONS_RPSLS[computer]} Me",
                    components=None,
                )
            elif computer == "paper":
                await msg.edit(
                    content=f"Well, we must be mind-readers!\n\nYou {ICONS_RPSLS['paper']} - {ICONS_RPSLS[computer]} Me",
                    components=None,
                )
            elif computer == "scissors":
                await msg.edit(
                    content=f"Look at that, I win!\n\nYou {ICONS_RPSLS['paper']} - {ICONS_RPSLS[computer]} Me",
                    components=None,
                )
            elif computer == "lizard":
                await msg.edit(
                    content=f"Look at that, I win!\n\nYou {ICONS_RPSLS['paper']} - {ICONS_RPSLS[computer]} Me",
                    components=None,
                )
            else:  # computer == 'spock'
                await msg.edit(
                    content=f"Congrats, you win!\n\nYou {ICONS_RPSLS['paper']} - {ICONS_RPSLS[computer]} Me",
                    components=None,
                )
            global dead
            dead = True

        @on_click.matching_id("scissors", cancel_others=True)
        async def on_scissors(inter):
            await inter.reply(type=ResponseType.DeferredUpdateMessage)
            if computer == "rock":
                await msg.edit(
                    content=f"Look at that, I win!\n\nYou {ICONS_RPSLS['scissors']} - {ICONS_RPSLS[computer]} Me",
                    components=None,
                )
            elif computer == "paper":
                await msg.edit(
                    content=f"Congrats, you win!\n\nYou {ICONS_RPSLS['scissors']} - {ICONS_RPSLS[computer]} Me",
                    components=None,
                )
            elif computer == "scissors":
                await msg.edit(
                    content=f"Well, we must be mind-readers!\n\nYou {ICONS_RPSLS['scissors']} - {ICONS_RPSLS[computer]} Me",
                    components=None,
                )
            elif computer == "lizard":
                await msg.edit(
                    content=f"Congrats, you win!\n\nYou {ICONS_RPSLS['scissors']} - {ICONS_RPSLS[computer]} Me",
                    components=None,
                )
            else:  # computer == 'spock'
                await msg.edit(
                    content=f"Look at that, I win!\n\nYou {ICONS_RPSLS['scissors']} - {ICONS_RPSLS[computer]} Me",
                    components=None,
                )
            global dead
            dead = True

        @on_click.matching_id("lizard", cancel_others=True)
        async def on_lizard(inter):
            await inter.reply(type=ResponseType.DeferredUpdateMessage)
            if computer == "rock":
                await msg.edit(
                    content=f"Look at that, I win!\n\nYou {ICONS_RPSLS['lizard']} - {ICONS_RPSLS[computer]} Me",
                    components=None,
                )
            elif computer == "paper":
                await msg.edit(
                    content=f"Congrats, you win!\n\nYou {ICONS_RPSLS['lizard']} - {ICONS_RPSLS[computer]} Me",
                    components=None,
                )
            elif computer == "scissors":
                await msg.edit(
                    content=f"Look at that, I win!\n\nYou {ICONS_RPSLS['lizard']} - {ICONS_RPSLS[computer]} Me",
                    components=None,
                )
            elif computer == "lizard":
                await msg.edit(
                    content=f"Well, we must be mind-readers!\n\nYou {ICONS_RPSLS['lizard']} - {ICONS_RPSLS[computer]} Me",
                    components=None,
                )
            else:  # computer == 'spock'
                await msg.edit(
                    content=f"Congrats, you win!\n\nYou {ICONS_RPSLS['lizard']} - {ICONS_RPSLS[computer]} Me",
                    components=None,
                )
            global dead
            dead = True

        @on_click.matching_id("spock", cancel_others=True)
        async def on_spock(inter):
            await inter.reply(type=ResponseType.DeferredUpdateMessage)
            if computer == "rock":
                await msg.edit(
                    content=f"Congrats, you win!\n\nYou {ICONS_RPSLS['spock']} - {ICONS_RPSLS[computer]} Me",
                    components=None,
                )
            elif computer == "paper":
                await msg.edit(
                    content=f"Look at that, I win!\n\nYou {ICONS_RPSLS['spock']} - {ICONS_RPSLS[computer]} Me",
                    components=None,
                )
            elif computer == "scissors":
                await msg.edit(
                    content=f"Congrats, you win!\n\nYou {ICONS_RPSLS['spock']} - {ICONS_RPSLS[computer]} Me",
                    components=None,
                )
            elif computer == "lizard":
                await msg.edit(
                    content=f"Look at that, I win!\n\nYou {ICONS_RPSLS['spock']} - {ICONS_RPSLS[computer]} Me",
                    components=None,
                )
            else:  # computer == 'spock'
                await msg.edit(
                    content=f"Well, we must be mind-readers!\n\nYou {ICONS_RPSLS['spock']} - {ICONS_RPSLS[computer]} Me",
                    components=None,
                )
            global dead
            dead = True

        @on_click.matching_id("rules", cancel_others=False, reset_timeout=True)
        async def on_rules(inter):
            embed = discord.Embed()
            embed.title = "Rock, Paper, Scissors"
            embed.color = await ctx.embed_color()
            embed.description = (
                f"A game of skill (chance).\n"
                f"Simply select your choice and see if you can defeat he computer\n\n\n"
                f"Rock {ICONS_RPSLS['rock']} beats Scissors {ICONS_RPSLS['scissors']} and Lizard {ICONS_RPSLS['lizard']}\n"
                f"Paper {ICONS_RPSLS['paper']} beats Rock {ICONS_RPSLS['rock']} and Spock {ICONS_RPSLS['spock']}\n"
                f"Scissors {ICONS_RPSLS['scissors']} beats Paper {ICONS_RPSLS['paper']} and Lizard {ICONS_RPSLS['lizard']}\n"
                f"Lizard {ICONS_RPSLS['lizard']} beats Paper {ICONS_RPSLS['paper']} and Spock {ICONS_RPSLS['spock']}\n"
                f"Spock {ICONS_RPSLS['spock']} beats Rock {ICONS_RPSLS['rock']} and Scissors {ICONS_RPSLS['scissors']}\n"
            )
            await inter.reply(embed=embed, ephemeral=True)

        @on_click.matching_id("cancel", cancel_others=False)
        async def on_cancel(inter):
            await inter.reply(type=ResponseType.DeferredUpdateMessage)
            await msg.edit(content="Very well, maybe later", components=None)

        @on_click.timeout
        async def on_timeout():
            global dead
            if not dead:
                await msg.edit(content="Okay then, maybe later", components=None)

    async def red_delete_data_for_user(self, *, requester: RequestType, user_id: int) -> None:
        # this cog does not store any user data
        pass

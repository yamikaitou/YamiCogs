import asyncio
import logging
import random
from datetime import datetime
from typing import Literal

import discord
from discord.ext import tasks
from redbot.core import Config, bank, commands
from redbot.core.bot import Red
from redbot.core.utils.chat_formatting import box
from tabulate import tabulate

log = logging.getLogger("red.yamicogs.russianroulette")


class RussianRoulette(commands.Cog):
    """
    Russian Roulette
    """

    __version__ = "0.1"

    def format_help_for_context(self, ctx):
        """Thanks Sinbad."""
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\nCog Version: {self.__version__}"

    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(
            self, identifier=582650109, force_registration=True
        )

        default_guild = {"mode": True, "chamber": 6, "cost": 100, "channel": 0}
        default_channel = {"pot": 0, "players": [], "active": 0, "time": 0}

        self.config.register_guild(**default_guild)
        self.config.register_channel(**default_channel)

    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    async def russian(self, ctx):
        """ Create or Join a game of Russian Roulette """

        c = await self.config.guild(ctx.guild).all()

        if c["channel"] == 0:
            await ctx.send(
                "Cannot proceed, game has not been configured yet for the server (no output channel)"
            )

        return await self.add_player(ctx, c)

    async def add_player(self, ctx, settings):

        setting = self.config.channel_from_id(settings["channel"])
        c = await setting.all()
        if c["active"] == 2:
            return await ctx.send(
                "You cannot join a game that is currently in progress, please wait until it is finished"
            )

        if not await bank.can_spend(ctx.author, settings["cost"]):
            return await ctx.send(
                "Sorry, you do not have enough {credits} to play (you need {cost})".format(
                    credits=await bank.get_currency_name(ctx.guild),
                    cost=settings["cost"],
                )
            )

        async with setting.players() as p:
            p.append(ctx.author.id)
        await setting.pot.set(await setting.pot() + settings["cost"])
        if len(await setting.players()) > 2:
            await setting.time.set(datetime.now())
            await setting.active.set(1)

    @tasks.loop(seconds=30.0)
    async def game_tick(self):

        async with self.config.all_channels() as channels:
            pass

    @commands.command(name="dev")
    @commands.is_owner()
    async def yami_dev(self, ctx, action, extra=None):

        if action == "add":
            extra = int(extra)
            if 2 <= extra <= (await self.config.guild(ctx.guild).chamber()):
                users = random.sample(
                    ctx.guild.get_role(346744009458450433).members, extra
                )
                await self.config.channel(ctx.channel).players.clear()
                async with self.config.channel(ctx.channel).players() as p:
                    for m in users:
                        p.append(m.id)
                        log.debug(f"Added {m}")
                await self.config.channel(ctx.channel).pot.set(
                    (await self.config.guild(ctx.guild).cost()) * extra
                )
                await ctx.send(f"Cleared the pool and added {extra} players")
        elif action == "list":
            users = await self.config.channel(ctx.channel).players()
            names = ""
            for u in users:
                log.debug(u)
                names += (
                    await self.bot.get_or_fetch_member(ctx.guild, u)
                ).display_name + "\n"

            await ctx.send(
                f"Pot: {await self.config.channel(ctx.channel).pot()}\n```{names}```"
            )
        elif action == "play":
            await self.config.channel(ctx.channel).active.set(True)
            users = await self.config.channel(ctx.channel).players()
            names = [
                [
                    u,
                    (
                        await self.bot.get_or_fetch_member(ctx.guild, u)
                    ).display_name,
                ]
                for u in users
            ]

            mode = await self.config.guild(ctx.guild).mode()
            size = await self.config.guild(ctx.guild).chamber()
            r = 1

            msg = await ctx.send("Starting game, please hold")

            state = True
            while state:
                embed = discord.Embed()
                embed.title = "Russian Roulette - Round {}".format(r)
                embed.description = (
                    "{} loads the revolver and spins the chamber\n\n".format(
                        ctx.guild.me.display_name
                    )
                )
                gun = [0] * size
                gun[random.randrange(len(gun))] = 1

                chamber = 0
                dead = False
                for n in names:
                    if gun[chamber]:
                        embed.description += (
                            "{} - *bang* \N{COLLISION SYMBOL} \n".format(n[1])
                        )
                        if not mode:  # 1 Loser
                            state = False
                        names.remove(n)
                        async with self.config.channel(ctx.channel).players() as p:
                            p.remove(n[0])
                        dead = True

                        break
                    else:
                        embed.description += "{} - *click*\n".format(n[1])
                    chamber += 1

                log.debug(
                    f"{chamber} >= {len(gun)-1} = {chamber>=len(gun)-1} | {state}"
                )
                if chamber >= len(gun) - 1 and not dead:
                    log.debug("additional shots")
                    for n in names:
                        if gun[chamber]:
                            embed.description += (
                                "{} - *bang* \N{COLLISION SYMBOL} \n".format(n[1])
                            )
                            if not mode:  # 1 Loser
                                state = False
                            names.remove(n)
                            async with self.config.channel(ctx.channel).players() as p:
                                p.remove(n[0])

                            break
                        else:
                            embed.description += "{} - *click*\n".format(n[1])
                        chamber += 1

                log.debug(names)
                await ctx.send(embed=embed)

                if mode:
                    r += 1
                    if len(names) == 1:
                        state = False
                    await asyncio.sleep(1)

            users = await self.config.channel(ctx.channel).players()
            names = ""
            for u in users:
                names += (
                    await self.bot.get_or_fetch_member(ctx.guild, u)
                ).display_name + "\n"

            await ctx.send(f"Survivors\n```{names}```")

    @russian.command(name="reset", hidden=True)
    @commands.admin_or_permissions(manage_guild=True)
    async def russian_reset(self, ctx):
        """ Stop a game. Do not use unless instructed, no refunds """

        chan = await self.config.guild(ctx.guild).channel()
        await self.config.channel_from_id(chan).clear()
        await ctx.tick()

    @commands.group()
    @commands.guild_only()
    @commands.admin_or_permissions(manage_guild=True)
    async def setrussian(self, ctx):
        """Configure Russian Roulette"""

    @setrussian.command(name="show")
    async def set_show(self, ctx):
        """Show the configured settings"""

        c = await self.config.guild(ctx.guild).all()

        settings = [
            ["Mode", ("1 Winner" if c["mode"] else "1 Loser")],
            ["Chambers", c["chamber"]],
            ["Cost", c["cost"]],
            [
                "Channel",
                "Not Set"
                if c["channel"] == 0
                else ctx.guild.get_channel(c["channel"]).name,
            ],
        ]

        await ctx.maybe_send_embed(box(tabulate(settings)))

    @setrussian.command(name="mode")
    async def set_mode(self, ctx, mode: str):
        """
        Set the mode for Russian Roulette

        `win` - Game keeps going until there is 1 player left
        `lose` - Game stops after 1 player dies
        """

        if mode == "win":
            await self.config.guild(ctx.guild).mode.set(True)
            await ctx.tick()
        elif mode == "lose":
            await self.config.guild(ctx.guild).mode.set(False)
            await ctx.tick()
        else:
            await ctx.send("Unknown mode, please provide either `win` or `lose`")

    @setrussian.command(name="chamber")
    async def set_chamber(self, ctx, size: int):
        """
        Set the number of chambers the revolver has
        Min is 3 and Max is 12
        """

        if not 3 <= size <= 12:
            return await ctx.send(
                "Invalid chamber size. Please select a size that is no lower than 3 and no higher than 12"
            )

        await self.config.guild(ctx.guild).chamber.set(size)
        await ctx.tick()

    @setrussian.command(name="cost")
    async def set_cost(self, ctx, cost: int):
        """
        Set the cost for playing.
        """

        if cost < 1:
            return await ctx.send("You cannot set the cost lower than 1")
        if cost > bank.get_max_balance(ctx.guild):
            return await ctx.send("You cannot set the cost higher than the Bank's max")

        await self.config.guild(ctx.guild).cost.set(cost)
        await ctx.tick()

    @setrussian.command(name="channel")
    async def set_channel(self, ctx, channel: discord.TextChannel):
        """
        Set the channel for the game output
        """

        try:
            await channel.trigger_typing()
        except discord.Forbidden:
            return await ctx.send("I do not have access to that channel")

        await self.config.guild(ctx.guild).channel.set(channel.id)
        await ctx.tick()

    @game_tick.before_loop
    async def before_game_tick(self):
        await self.bot.wait_until_red_ready()

    async def red_delete_data_for_user(
        self,
        *,
        requester: Literal["discord_deleted_user", "owner", "user", "user_strict"],
        user_id: int,
    ):

        pass

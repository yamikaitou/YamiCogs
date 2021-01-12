import logging
import math
from typing import Literal

from discord.ext import tasks
from redbot.core import Config, bank, commands
from redbot.core.bot import Red
from tabulate import tabulate

from . import checks as lc

log = logging.getLogger("red.yamicogs.trickle")


class Trickle(commands.Cog):
    """
    Trickle credits into your Economy
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

        default_config = {"credits": 0, "messages": 0}

        self.config.register_global(**default_config)
        self.config.register_guild(**default_config)

        self.bot.loop.create_task(self.initialize())
        self.msg = {}
        self.trickle.start()

    async def initialize(self):
        await self.bot.wait_until_red_ready()

        if await bank.is_global():
            self.cache = await self.config.all()
        else:
            self.cache = await self.config.all_guilds()
        self.bank = await bank.is_global()

    def cog_unload(self):
        self.trickle.cancel()

    @commands.Cog.listener()
    async def on_message_without_command(self, message):

        if message.author.bot:
            return
        if message.guild == None:
            return

        if await bank.is_global():
            try:
                self.msg[message.author.id].append(message.id)
            except KeyError:
                self.msg[message.author.id] = [message.id]
        else:
            print(self.msg)
            try:
                self.msg[message.guild.id]
                try:
                    self.msg[message.guild.id][message.author.id].append(
                        message.id
                    )
                except KeyError:
                    self.msg[message.guild.id][message.author.id] = [message.id]
            except KeyError:
                self.msg[message.guild.id] = {message.author.id: [message.id]}
            
            print(self.msg)

    @tasks.loop(minutes=1)
    async def trickle(self):
        if self.bank is not await bank.is_global():
            if await bank.is_global():
                self.cache = await self.config.all()
            else:
                self.cache = await self.config.all_guilds()
            self.bank = await bank.is_global()

        if await bank.is_global():
            log.info(f"Global || Starting task")
            msgs = self.msg
            for user, msg in msgs.items():
                if len(msg) >= self.cache["messages"]:
                    num = math.floor(len(msg) / self.cache["messages"])
                    del (self.msg[user])[0 : (num * self.cache["messages"])]
                    val = await bank.deposit_credits(
                        (await self.bot.get_or_fetch_user(user)),
                        num * self.cache["credits"],
                    )
                    log.info(
                        f"Global || {await self.bot.get_or_fetch_user(user)} || {val} || {num}"
                    )
        else:
            log.info(f"Local || Starting task")
            msgs = self.msg
            for guild, users in msgs.items():
                for user, msg in users.items():
                    if len(msg) >= self.cache[guild]["messages"]:
                        num = math.floor(len(msg) / self.cache[guild]["messages"])
                        del (self.msg[guild][user])[
                            0 : (num * self.cache[guild]["messages"])
                        ]
                        val = await bank.deposit_credits(
                            (
                                await self.bot.get_or_fetch_member(
                                    self.bot.get_guild(guild), user
                                )
                            ),
                            num * self.cache[guild]["credits"],
                        )
                        log.info(
                            f"Local || {self.bot.get_guild(guild).name} || {await self.bot.get_or_fetch_member(self.bot.get_guild(guild), user)} || {val} || {num}"
                        )

    @trickle.before_loop
    async def before_trickle(self):
        await self.bot.wait_until_red_ready()

    @commands.is_owner()
    @commands.command()
    async def trickles(self, ctx):

        dev = {}
        if await bank.is_global():
            msgs = self.msg
            for user, msg in msgs.items():
                num = math.floor(len(msg) / self.cache["messages"])
                del self.msg[user][:num]
                dev[(await self.bot.get_or_fetch_user(user)).display_name] = (
                    num * self.cache["credits"]
                )
            await ctx.send(dev)
        else:
            for user, msg in self.msg[ctx.guild.id].items():
                dev[
                    (await self.bot.get_or_fetch_member(ctx.guild, user)).display_name
                ] = len(msg)
            await ctx.send(dev)

    @commands.admin_or_permissions(manage_guild=True)
    @commands.group()
    async def trickleset(self, ctx):
        """ Configure various settings """

    @trickleset.command(name="credits")
    async def ts_credits(self, ctx, number: int):
        """
        Set the number of credits to grant

        Set the number to 0 to disable
        """

        if await bank.is_global():
            if 0 <= number <= (await bank.get_max_balance()):
                await self.config.credits.set(number)
                self.cache["credits"] = number
                await ctx.tick()
            else:
                await ctx.send(
                    f"You must specify a value that is not less than 0 and not more than {(await bank.get_max_balance())}"
                )
        else:
            if 0 <= number <= (await bank.get_max_balance(ctx.guild)):
                await self.config.guild(ctx.guild).credits.set(number)
                self.cache[ctx.guild.id] = await self.config.guild(ctx.guild).all()
                await ctx.tick()
            else:
                await ctx.send(
                    f"You must specify a value that is not less than 0 and not more than {(await bank.get_max_balance())}"
                )

    @trickleset.command(name="messages")
    async def ts_messages(self, ctx, number: int):
        """
        Set the number of messages required to gain credits

        Set the number to 0 to disable
        Max value is 100
        """

        if await bank.is_global():
            if 0 <= number <= 100:
                await self.config.messages.set(number)
                self.cache["messages"] = number
                await ctx.tick()
            else:
                await ctx.send(
                    f"You must specify a value that is not less than 0 and not more than 100"
                )
        else:
            if 0 <= number <= 100:
                await self.config.guild(ctx.guild).messages.set(number)
                self.cache[ctx.guild.id] = await self.config.guild(ctx.guild).all()
                await ctx.tick()
            else:
                await ctx.send(
                    f"You must specify a value that is not less than 0 and not more than 100"
                )

    async def red_delete_data_for_user(
        self,
        *,
        requester: Literal["discord_deleted_user", "owner", "user", "user_strict"],
        user_id: int,
    ):
        pass

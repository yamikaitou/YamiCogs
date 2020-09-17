import discord
from discord.ext import tasks
from redbot.core import commands, Config, checks, bank
from redbot.core.bot import Red
from redbot.core.utils.chat_formatting import box, humanize_timedelta
from tabulate import tabulate
import logging
from datetime import datetime, timedelta
from typing import Literal
from . import checks as lc


log = logging.getLogger("red.yamicogs.payday")

class PayDay(commands.Cog):
    """
    Customizable PayDay system
    """

    __version__ = "0.1"

    def format_help_for_context(self, ctx):
        """Thanks Sinbad."""
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\nCog Version: {self.__version__}"

    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=582650109, force_registration=True)

        default_config = {
            "hour": 0,
            "day": 0,
            "week": 0,
            "month": 0,
            "quarter": 0,
            "year": 0
        }
        default_user = {
            "hour": "2016-01-02T04:25:00-04:00",
            "day": "2016-01-02T04:25:00-04:00",
            "week": "2016-01-02T04:25:00-04:00",
            "month": "2016-01-02T04:25:00-04:00",
            "quarter": "2016-01-02T04:25:00-04:00",
            "year": "2016-01-02T04:25:00-04:00"
        }

        self.config.register_global(**default_config)
        self.config.register_guild(**default_config)
        self.config.register_member(**default_user)
        self.config.register_user(**default_user)

    @lc.guild_only_check()
    @commands.group(invoke_without_command=True)
    async def freecredits(self, ctx):
        """Get some free more currency."""
        pass
    
    @lc.hourly()
    @freecredits.command(name="hourly")
    async def freecredits_hourly(self, ctx):
        """Get some free currency every hour"""

        if await bank.is_global():
            free = await self.config.hour()
            if free > 0:
                last = datetime.fromisoformat(await self.config.member(ctx.author).hour())
                now = datetime.now().astimezone().replace(microsecond=0)
                
                if (now - last).seconds >= 3600:
                    await bank.deposit_credits(ctx.author, free)
                    await self.config.user(ctx.author).hour.set(now.isoformat())
                    await ctx.send("You have been given {} {}".format(free, (await bank.get_currency_name())))
                else:
                    await ctx.send("Sorry, you still have {} until your next hourly bonus".format(humanize_timedelta(timedelta=(timedelta(hours=1)-(now-last)))))
        else:
            free = await self.config.guild(ctx.guild).hour()
            if free > 0:
                last = datetime.fromisoformat(await self.config.member(ctx.author).hour())
                now = datetime.now().astimezone().replace(microsecond=0)
                
                if (now - last).seconds >= 3600:
                    await bank.deposit_credits(ctx.author, free)
                    await self.config.member(ctx.author).hour.set(now.isoformat())
                    await ctx.send("You have been given {} {}".format(free, (await bank.get_currency_name(ctx.guild))))
                else:
                    await ctx.send("Sorry, you still have {} until your next hourly bonus".format(humanize_timedelta(timedelta=(timedelta(hours=1)-(now-last)))))
    
    @lc.daily()
    @freecredits.command(name="daily")
    async def freecredits_daily(self, ctx):
        """Get some free currency every day"""

        if await bank.is_global():
            free = await self.config.day()
            if free > 0:
                last = datetime.fromisoformat(await self.config.member(ctx.author).day())
                now = datetime.now().astimezone().replace(microsecond=0)
                
                if (now - last).days >= 1:
                    await bank.deposit_credits(ctx.author, free)
                    await self.config.user(ctx.author).day.set(now.isoformat())
                    await ctx.send("You have been given {} {}".format(free, (await bank.get_currency_name())))
                else:
                    await ctx.send("Sorry, you still have {} until your next daily bonus".format(humanize_timedelta(timedelta=(timedelta(days=1)-(now-last)))))
        else:
            free = await self.config.guild(ctx.guild).day()
            if free > 0:
                last = datetime.fromisoformat(await self.config.member(ctx.author).day())
                now = datetime.now().astimezone().replace(microsecond=0)
                
                if (now - last).days >= 1:
                    await bank.deposit_credits(ctx.author, free)
                    await self.config.member(ctx.author).day.set(now.isoformat())
                    await ctx.send("You have been given {} {}".format(free, (await bank.get_currency_name(ctx.guild))))
                else:
                    await ctx.send("Sorry, you still have {} until your next daily bonus".format(humanize_timedelta(timedelta=(timedelta(days=1)-(now-last)))))
    
    @lc.weekly()
    @freecredits.command(name="weekly")
    async def freecredits_weekly(self, ctx):
        """Get some free currency every week (7 days)"""

        if await bank.is_global():
            free = await self.config.week()
            if free > 0:
                last = datetime.fromisoformat(await self.config.member(ctx.author).week())
                now = datetime.now().astimezone().replace(microsecond=0)
                
                if (now - last).days >= 7:
                    await bank.deposit_credits(ctx.author, free)
                    await self.config.user(ctx.author).week.set(now.isoformat())
                    await ctx.send("You have been given {} {}".format(free, (await bank.get_currency_name())))
                else:
                    await ctx.send("Sorry, you still have {} until your next weekly bonus".format(humanize_timedelta(timedelta=(timedelta(days=7)-(now-last)))))
        else:
            free = await self.config.guild(ctx.guild).week()
            if free > 0:
                last = datetime.fromisoformat(await self.config.member(ctx.author).week())
                now = datetime.now().astimezone().replace(microsecond=0)
                
                if (now - last).days >= 7:
                    await bank.deposit_credits(ctx.author, free)
                    await self.config.member(ctx.author).week.set(now.isoformat())
                    await ctx.send("You have been given {} {}".format(free, (await bank.get_currency_name(ctx.guild))))
                else:
                    await ctx.send("Sorry, you still have {} until your next weekly bonus".format(humanize_timedelta(timedelta=(timedelta(days=7)-(now-last)))))
    
    @lc.monthly()
    @freecredits.command(name="monthly")
    async def freecredits_monthly(self, ctx):
        """Get some free currency every month (30 days)"""

        if await bank.is_global():
            free = await self.config.month()
            if free > 0:
                last = datetime.fromisoformat(await self.config.member(ctx.author).month())
                now = datetime.now().astimezone().replace(microsecond=0)
                
                if (now - last).days >= 30:
                    await bank.deposit_credits(ctx.author, free)
                    await self.config.user(ctx.author).month.set(now.isoformat())
                    await ctx.send("You have been given {} {}".format(free, (await bank.get_currency_name())))
                else:
                    await ctx.send("Sorry, you still have {} until your next monthly bonus".format(humanize_timedelta(timedelta=(timedelta(days=30)-(now-last)))))
        else:
            free = await self.config.guild(ctx.guild).month()
            if free > 0:
                last = datetime.fromisoformat(await self.config.member(ctx.author).month())
                now = datetime.now().astimezone().replace(microsecond=0)
                
                if (now - last).days >= 30:
                    await bank.deposit_credits(ctx.author, free)
                    await self.config.member(ctx.author).month.set(now.isoformat())
                    await ctx.send("You have been given {} {}".format(free, (await bank.get_currency_name(ctx.guild))))
                else:
                    await ctx.send("Sorry, you still have {} until your next monthly bonus".format(humanize_timedelta(timedelta=(timedelta(days=30)-(now-last)))))
    
    @lc.quarterly()
    @freecredits.command(name="quarterly")
    async def freecredits_quarterly(self, ctx):
        """Get some free currency every quarter (122 days)"""

        if await bank.is_global():
            free = await self.config.quarter()
            if free > 0:
                last = datetime.fromisoformat(await self.config.member(ctx.author).quarter())
                now = datetime.now().astimezone().replace(microsecond=0)
                
                if (now - last).days >= 122:
                    await bank.deposit_credits(ctx.author, free)
                    await self.config.user(ctx.author).quarter.set(now.isoformat())
                    await ctx.send("You have been given {} {}".format(free, (await bank.get_currency_name())))
                else:
                    await ctx.send("Sorry, you still have {} until your next quarterly bonus".format(humanize_timedelta(timedelta=(timedelta(days=122)-(now-last)))))
        else:
            free = await self.config.guild(ctx.guild).quarter()
            if free > 0:
                last = datetime.fromisoformat(await self.config.member(ctx.author).quarter())
                now = datetime.now().astimezone().replace(microsecond=0)
                
                if (now - last).days >= 122:
                    await bank.deposit_credits(ctx.author, free)
                    await self.config.member(ctx.author).quarter.set(now.isoformat())
                    await ctx.send("You have been given {} {}".format(free, (await bank.get_currency_name(ctx.guild))))
                else:
                    await ctx.send("Sorry, you still have {} until your next quarterly bonus".format(humanize_timedelta(timedelta=(timedelta(days=122)-(now-last)))))
    
    @lc.yearly()
    @freecredits.command(name="yearly")
    async def freecredits_yearly(self, ctx):
        """Get some free currency every year (365 days)"""

        if await bank.is_global():
            free = await self.config.year()
            if free > 0:
                last = datetime.fromisoformat(await self.config.member(ctx.author).year())
                now = datetime.now().astimezone().replace(microsecond=0)
                
                if (now - last).days >= 365:
                    await bank.deposit_credits(ctx.author, free)
                    await self.config.user(ctx.author).year.set(now.isoformat())
                    await ctx.send("You have been given {} {}".format(free, (await bank.get_currency_name())))
                else:
                    await ctx.send("Sorry, you still have {} until your next yearly bonus".format(humanize_timedelta(timedelta=(timedelta(days=365)-(now-last)))))
        else:
            free = await self.config.guild(ctx.guild).year()
            if free > 0:
                last = datetime.fromisoformat(await self.config.member(ctx.author).year())
                now = datetime.now().astimezone().replace(microsecond=0)
                
                if (now - last).days >= 365:
                    await bank.deposit_credits(ctx.author, free)
                    await self.config.member(ctx.author).year.set(now.isoformat())
                    await ctx.send("You have been given {} {}".format(free, (await bank.get_currency_name(ctx.guild))))
                else:
                    await ctx.send("Sorry, you still have {} until your next yearly bonus".format(humanize_timedelta(timedelta=(timedelta(days=365)-(now-last)))))
    
    @lc.is_owner_if_bank_global()
    @checks.guildowner_or_permissions(administrator=True)
    @commands.group()
    async def pdconfig(self, ctx):
        """Configure the `freecredits` options"""
        pass

    @lc.is_owner_if_bank_global()
    @checks.guildowner_or_permissions(administrator=True)
    @pdconfig.command(name="settings")
    async def pdconfig_info(self, ctx):
        """Print the `freecredits` options"""
        
        if await bank.is_global():
            conf = await self.config.all()
            await ctx.send(box(tabulate(conf.items())))
        else:
            conf = await self.config.guild(ctx.guild).all()
            await ctx.send(box(tabulate(conf.items())))

    @lc.is_owner_if_bank_global()
    @checks.guildowner_or_permissions(administrator=True)
    @pdconfig.command(name="hourly")
    async def pdconfig_hourly(self, ctx):
        """Configure the `hourly` options"""
        pass

    
    @commands.group()
    async def test(self, ctx):
        await ctx.send("Hi")

    @test.command()
    async def ing(self, ctx):
        await ctx.send(ctx.command)
    
    async def red_delete_data_for_user(
        self,
        *,
        requester: Literal["discord_deleted_user", "owner", "user", "user_strict"],
        user_id: int,
    ):
        if requester == "discord_deleted_user":
            # user is deleted, just comply

            data = await self.config.all_members()
            async for guild_id, members in AsyncIter(data.items(), steps=100):
                if user_id in members:
                    await self.config.member_from_ids(guild_id, user_id).clear()
            
            data = await self.config.all_users()
            async for users in AsyncIter(data.items(), steps=100):
                if user_id in users:
                    await self.config.user_from_id(user_id).clear()
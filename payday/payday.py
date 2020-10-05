import discord
from discord.ext import tasks
from redbot.core import commands, Config, checks, bank
from redbot.core.commands import BadArgument
from redbot.core.bot import Red
from redbot.core.utils.chat_formatting import box, humanize_timedelta, inline
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

    settings = {'day':1,'week':7,'month':30,'quarter':122,'year':365}
    friendly = {'hour':"Hourly",'day':"Daily",'week':"Weekly",'month':"Monthly",'quarter':"Quarterly",'year':"Yearly"}

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
    @commands.group()
    async def freecredits(self, ctx):
        """Get some free more currency."""
        pass

    @lc.all()
    @freecredits.command(name="times")
    async def freecredits_times(self, ctx):
        """Display remaining time for all options"""

        if await bank.is_global():
            amounts = await self.config.all()
            times = await self.config.user(ctx.author).all()
            now = datetime.now().astimezone().replace(microsecond=0)
            strings = ""

            if amounts['hour']:
                td = (now-datetime.fromisoformat(times['hour']))
                strings += self.friendly['hour'] + ": " + (humanize_timedelta(timedelta=(timedelta(hours=1)-td)) if td.seconds < 3600 else "Available Now!") + "\n"
            
            for k,v in self.settings.items():
                if amounts[k]:
                    td = (now-(datetime.fromisoformat(times[k])))
                    strings += self.friendly[k] + ": " + (humanize_timedelta(timedelta=(timedelta(days=v)-td)) if td.days < v else "Available Now!") + "\n"
            
            await ctx.send(strings)
        else:
            amounts = await self.config.guild(ctx.guild).all()
            times = await self.config.member(ctx.author).all()
            now = datetime.now().astimezone().replace(microsecond=0)
            strings = ""

            if amounts['hour']:
                td = (now-(datetime.fromisoformat(times['hour'])))
                strings += self.friendly['hour'] + ": " + (humanize_timedelta(timedelta=(timedelta(hours=1)-td)) if td.seconds < 3600 else "Available Now!") + "\n"
            
            for k,v in self.settings.items():
                if amounts[k]:
                    td = (now-(datetime.fromisoformat(times[k])))
                    strings += self.friendly[k] + ": " + (humanize_timedelta(timedelta=(timedelta(days=v)-td)) if td.days < v else "Available Now!") + "\n"
            
            await ctx.send(strings)


    
    @lc.all()
    @freecredits.command(name="all")
    async def freecredits_all(self, ctx):
        """Claim all available freecredits"""
        
        amount = 0
        if await bank.is_global():
            amounts = await self.config.all()
            times = await self.config.user(ctx.author).all()
            now = datetime.now().astimezone().replace(microsecond=0)

            if amounts['hour'] and (now-(datetime.fromisoformat(times['hour']))).seconds >= 3600:
                amount += await self.config.hour()
                await self.config.hour.set(now.isoformat())

            for k,v in self.settings.items():
                if amounts[k] and (now-(datetime.fromisoformat(times[k]))).days >= v:
                    amount += amounts[k]
                    await self.config.user(ctx.author).set_raw(k, value=now.isoformat())
            
            if amount > 0:
                await bank.deposit_credits(ctx.author, amount)
                await ctx.send("You have claimed all available credits from the `freecredits` program! +{} {}".format(amount, (await bank.get_currency_name())))
        else:
            amounts = await self.config.guild(ctx.guild).all()
            times = await self.config.member(ctx.author).all()
            now = datetime.now().astimezone().replace(microsecond=0)

            if amounts['hour'] and (now-(datetime.fromisoformat(times['hour']))).seconds >= 3600:
                amount += await self.config.guild(ctx.guild).hour()
                await self.config.hour.set(now.isoformat())

            for k,v in self.settings.items():
                if amounts[k] and (now-(datetime.fromisoformat(times[k]))).days >= v:
                    amount += amounts[k]
                    await self.config.member(ctx.author).set_raw(k, value=now.isoformat())
            
            if amount > 0:
                await bank.deposit_credits(ctx.author, amount)
                await ctx.send("You have claimed all available credits from the `freecredits` program! +{} {}".format(amount, (await bank.get_currency_name(ctx.guild))))
    
    @lc.hourly()
    @freecredits.command(name="hourly")
    async def freecredits_hourly(self, ctx):
        """Get some free currency every hour"""

        if await bank.is_global():
            free = await self.config.hour()
            if free > 0:
                last = datetime.fromisoformat(await self.config.user(ctx.author).hour())
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
                last = datetime.fromisoformat(await self.config.user(ctx.author).day())
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
                last = datetime.fromisoformat(await self.config.user(ctx.author).week())
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
                last = datetime.fromisoformat(await self.config.user(ctx.author).month())
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
                last = datetime.fromisoformat(await self.config.user(ctx.author).quarter())
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
                last = datetime.fromisoformat(await self.config.user(ctx.author).year())
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
    @pdconfig.command(name="hourly", aliases=["hour"])
    async def pdconfig_hourly(self, ctx, value: int):
        """Configure the `hourly` options"""

        if value < 0:
            await ctx.send("You must provide a non-negative value or 0")
        if await bank.is_global():
            await self.config.hour.set(value)
            await ctx.tick()
        else:
            await self.config.guild(ctx.guild).hour.set(value)
            await ctx.tick()

    @lc.is_owner_if_bank_global()
    @checks.guildowner_or_permissions(administrator=True)
    @pdconfig.command(name="daily", aliases=["day"])
    async def pdconfig_daily(self, ctx, value: int):
        """Configure the `daily` options"""

        if value < 0:
            await ctx.send("You must provide a non-negative value or 0")
        if await bank.is_global():
            await self.config.day.set(value)
            await ctx.tick()
        else:
            await self.config.guild(ctx.guild).day.set(value)
            await ctx.tick()

    @lc.is_owner_if_bank_global()
    @checks.guildowner_or_permissions(administrator=True)
    @pdconfig.command(name="weekly", aliases=["week"])
    async def pdconfig_weekly(self, ctx, value: int):
        """Configure the `weekly` options"""

        if value < 0:
            await ctx.send("You must provide a non-negative value or 0")
        if await bank.is_global():
            await self.config.week.set(value)
            await ctx.tick()
        else:
            await self.config.guild(ctx.guild).week.set(value)
            await ctx.tick()

    @lc.is_owner_if_bank_global()
    @checks.guildowner_or_permissions(administrator=True)
    @pdconfig.command(name="monthly", aliases=["month"])
    async def pdconfig_monthly(self, ctx, value: int):
        """Configure the `monthly` options"""

        if value < 0:
            await ctx.send("You must provide a non-negative value or 0")
        if await bank.is_global():
            await self.config.month.set(value)
            await ctx.tick()
        else:
            await self.config.guild(ctx.guild).month.set(value)
            await ctx.tick()

    @lc.is_owner_if_bank_global()
    @checks.guildowner_or_permissions(administrator=True)
    @pdconfig.command(name="quarterly", aliases=["quarter"])
    async def pdconfig_quarterly(self, ctx, value: int):
        """Configure the `quarterly` options"""

        if value < 0:
            await ctx.send("You must provide a non-negative value or 0")
        if await bank.is_global():
            await self.config.quarter.set(value)
            await ctx.tick()
        else:
            await self.config.guild(ctx.guild).quarter.set(value)
            await ctx.tick()

    @lc.is_owner_if_bank_global()
    @checks.guildowner_or_permissions(administrator=True)
    @pdconfig.command(name="yearly", aliases=["year"])
    async def pdconfig_yearly(self, ctx, value: int):
        """Configure the `yearly` options"""

        if value < 0:
            await ctx.send("You must provide a non-negative value or 0")
        if await bank.is_global():
            await self.config.year.set(value)
            await ctx.tick()
        else:
            await self.config.guild(ctx.guild).year.set(value)
            await ctx.tick()

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

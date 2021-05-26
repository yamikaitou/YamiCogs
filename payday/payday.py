import logging
from datetime import datetime, timedelta
from typing import Literal, Union

import discord
from redbot.core import Config, bank, checks, commands
from redbot.core.bot import Red
from redbot.core.utils import AsyncIter
from redbot.core.utils.chat_formatting import box, humanize_timedelta
from tabulate import tabulate

from . import checks as lc

log = logging.getLogger("red.yamicogs.payday")


class PayDay(commands.Cog):
    """
    Customizable PayDay system
    """

    settings = {"day": 1, "week": 7, "month": 30, "quarter": 122, "year": 365}
    friendly = {
        "hour": "Hourly",
        "day": "Daily",
        "week": "Weekly",
        "month": "Monthly",
        "quarter": "Quarterly",
        "year": "Yearly",
    }

    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=582650109, force_registration=True)

        default_config = {
            "hour": 0,
            "day": 0,
            "week": 0,
            "month": 0,
            "quarter": 0,
            "year": 0,
            "streaks": {
                "hour": 0,
                "day": 0,
                "week": 0,
                "month": 0,
                "quarter": 0,
                "year": 0,
                "percent": False,
            },
        }
        default_user = {
            "hour": "2016-01-02T04:25:00-04:00",
            "day": "2016-01-02T04:25:00-04:00",
            "week": "2016-01-02T04:25:00-04:00",
            "month": "2016-01-02T04:25:00-04:00",
            "quarter": "2016-01-02T04:25:00-04:00",
            "year": "2016-01-02T04:25:00-04:00",
        }

        self.config.register_global(**default_config)
        self.config.register_guild(**default_config)
        self.config.register_member(**default_user)
        self.config.register_user(**default_user)

    @lc.guild_only_check()
    @commands.group()
    async def freecredits(self, ctx):
        """More options to get free credits"""

    @lc.all()
    @freecredits.command(name="times")
    async def freecredits_times(self, ctx):
        """Display remaining time for all options"""

        if await bank.is_global():
            amounts = await self.config.all()
            times = await self.config.user(ctx.author).all()
        else:
            amounts = await self.config.guild(ctx.guild).all()
            times = await self.config.member(ctx.author).all()

        now = datetime.now().astimezone().replace(microsecond=0)
        strings = ""

        if amounts["hour"]:
            td = now - datetime.fromisoformat(times["hour"])
            strings += (
                self.friendly["hour"]
                + ": "
                + (
                    humanize_timedelta(timedelta=(timedelta(hours=1) - td))
                    if td.seconds < 3600
                    else "Available Now!"
                )
                + "\n"
            )

        for k, v in self.settings.items():
            if amounts[k]:
                td = now - (datetime.fromisoformat(times[k]))
                strings += (
                    self.friendly[k]
                    + ": "
                    + (
                        humanize_timedelta(timedelta=(timedelta(days=v) - td))
                        if td.days < v
                        else "Available Now!"
                    )
                    + "\n"
                )
        if strings == "":
            await ctx.send("No freecredit options have been configured yet")
        else:
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

            if amounts["hour"] and (now - (datetime.fromisoformat(times["hour"]))).seconds >= 3600:
                amount += await self.config.hour()
                await self.config.user(ctx.author).hour.set(now.isoformat())

            for k, v in self.settings.items():
                if amounts[k] and (now - (datetime.fromisoformat(times[k]))).days >= v:
                    amount += amounts[k]
                    await self.config.user(ctx.author).set_raw(k, value=now.isoformat())

            bankname = await bank.get_currency_name()
            if amount > 0:
                await bank.deposit_credits(ctx.author, amount)
                await ctx.send(
                    "You have claimed all available {} from the `freecredits` program! +{} {}".format(
                        bankname, amount, bankname
                    )
                )
            else:
                await ctx.send("You have no available {} for claiming.".format(bankname))
        else:
            amounts = await self.config.guild(ctx.guild).all()
            times = await self.config.member(ctx.author).all()
            now = datetime.now().astimezone().replace(microsecond=0)

            if amounts["hour"] and (now - (datetime.fromisoformat(times["hour"]))).seconds >= 3600:
                amount += await self.config.guild(ctx.guild).hour()
                await self.config.member(ctx.author).hour.set(now.isoformat())

            for k, v in self.settings.items():
                if amounts[k] and (now - (datetime.fromisoformat(times[k]))).days >= v:
                    amount += int(amounts[k])
                    await self.config.member(ctx.author).set_raw(k, value=now.isoformat())
            bankname = await bank.get_currency_name(ctx.guild)
            if amount > 0:
                await bank.deposit_credits(ctx.author, amount)
                await ctx.send(
                    "You have claimed all available {} from the `freecredits` program! +{} {}".format(
                        bankname, amount, bankname
                    )
                )
            else:
                await ctx.send("You have no available {} for claiming.".format(bankname))

    @lc.hourly()
    @freecredits.command(name="hourly")
    async def freecredits_hourly(self, ctx):
        """Get some free currency every hour"""

        if await bank.is_global():
            free = await self.config.hour()
            streak = await self.config.streaks.hour()
            perc = await self.config.streaks.percent()
            config = self.config.user(ctx.author)
        else:
            free = await self.config.guild(ctx.guild).hour()
            streak = await self.config.guild(ctx.guild).streaks.hour()
            perc = await self.config.guild(ctx.guild).streaks.percent()
            config = self.config.member(ctx.author)

        if free > 0:
            last = datetime.fromisoformat(await config.hour())
            now = datetime.now().astimezone().replace(microsecond=0)

            if streak > 0 and (timedelta(hours=2) > (now - last) >= timedelta(hours=1)):
                if perc:
                    streak = free * streak
                await bank.deposit_credits(ctx.author, free + streak)
                await config.hour.set(now.isoformat())
                await ctx.send(
                    "You have been given {} {} plus {} for maintaining a streak".format(
                        free, (await bank.get_currency_name()), streak
                    )
                )
            elif (now - last) >= timedelta(hours=1):
                await bank.deposit_credits(ctx.author, free)
                await config.hour.set(now.isoformat())
                await ctx.send(
                    "You have been given {} {}".format(free, (await bank.get_currency_name()))
                )
            else:
                await ctx.send(
                    "Sorry, you still have {} until your next hourly bonus".format(
                        humanize_timedelta(timedelta=(timedelta(hours=1) - (now - last)))
                    )
                )

    @lc.daily()
    @freecredits.command(name="daily")
    async def freecredits_daily(self, ctx):
        """Get some free currency every day"""

        if await bank.is_global():
            free = await self.config.day()
            streak = await self.config.streaks.day()
            perc = await self.config.streaks.percent()
            config = self.config.user(ctx.author)
        else:
            free = await self.config.guild(ctx.guild).day()
            streak = await self.config.guild(ctx.guild).streaks.day()
            perc = await self.config.guild(ctx.guild).streaks.percent()
            config = self.config.member(ctx.author)

        if free > 0:
            last = datetime.fromisoformat(await config.day())
            now = datetime.now().astimezone().replace(microsecond=0)

            if streak > 0 and (timedelta(days=2) > (now - last) >= timedelta(days=1)):
                if perc:
                    streak = free * streak
                await bank.deposit_credits(ctx.author, free + streak)
                await config.day.set(now.isoformat())
                await ctx.send(
                    "You have been given {} {} plus {} for maintaining a streak".format(
                        free, (await bank.get_currency_name()), streak
                    )
                )
            elif (now - last) >= timedelta(days=1):
                await bank.deposit_credits(ctx.author, free)
                await config.day.set(now.isoformat())
                await ctx.send(
                    "You have been given {} {}".format(free, (await bank.get_currency_name()))
                )
            else:
                await ctx.send(
                    "Sorry, you still have {} until your next daily bonus".format(
                        humanize_timedelta(timedelta=(timedelta(days=1) - (now - last)))
                    )
                )

    @lc.weekly()
    @freecredits.command(name="weekly")
    async def freecredits_weekly(self, ctx):
        """Get some free currency every week (7 days)"""

        if await bank.is_global():
            free = await self.config.week()
            streak = await self.config.streaks.week()
            perc = await self.config.streaks.percent()
            config = self.config.user(ctx.author)
        else:
            free = await self.config.guild(ctx.guild).week()
            streak = await self.config.guild(ctx.guild).streaks.week()
            perc = await self.config.guild(ctx.guild).streaks.percent()
            config = self.config.member(ctx.author)

        if free > 0:
            last = datetime.fromisoformat(await config.week())
            now = datetime.now().astimezone().replace(microsecond=0)

            if streak > 0 and (timedelta(days=14) > (now - last) >= timedelta(days=7)):
                if perc:
                    streak = free * streak
                await bank.deposit_credits(ctx.author, free + streak)
                await config.week.set(now.isoformat())
                await ctx.send(
                    "You have been given {} {} plus {} for maintaining a streak".format(
                        free, (await bank.get_currency_name()), streak
                    )
                )
            elif (now - last) >= timedelta(days=7):
                await bank.deposit_credits(ctx.author, free)
                await config.week.set(now.isoformat())
                await ctx.send(
                    "You have been given {} {}".format(free, (await bank.get_currency_name()))
                )
            else:
                await ctx.send(
                    "Sorry, you still have {} until your next weekly bonus".format(
                        humanize_timedelta(timedelta=(timedelta(days=7) - (now - last)))
                    )
                )

    @lc.monthly()
    @freecredits.command(name="monthly")
    async def freecredits_monthly(self, ctx):
        """Get some free currency every month (30 days)"""

        if await bank.is_global():
            free = await self.config.month()
            streak = await self.config.streaks.month()
            perc = await self.config.streaks.percent()
            config = self.config.user(ctx.author)
        else:
            free = await self.config.guild(ctx.guild).month()
            streak = await self.config.guild(ctx.guild).streaks.month()
            perc = await self.config.guild(ctx.guild).streaks.percent()
            config = self.config.member(ctx.author)

        if free > 0:
            last = datetime.fromisoformat(await config.month())
            now = datetime.now().astimezone().replace(microsecond=0)

            if streak > 0 and (timedelta(days=60) > (now - last) >= timedelta(days=30)):
                if perc:
                    streak = free * streak
                await bank.deposit_credits(ctx.author, free + streak)
                await config.month.set(now.isoformat())
                await ctx.send(
                    "You have been given {} {} plus {} for maintaining a streak".format(
                        free, (await bank.get_currency_name()), streak
                    )
                )
            elif (now - last) >= timedelta(days=30):
                await bank.deposit_credits(ctx.author, free)
                await config.month.set(now.isoformat())
                await ctx.send(
                    "You have been given {} {}".format(free, (await bank.get_currency_name()))
                )
            else:
                await ctx.send(
                    "Sorry, you still have {} until your next monthly bonus".format(
                        humanize_timedelta(timedelta=(timedelta(days=30) - (now - last)))
                    )
                )

    @lc.quarterly()
    @freecredits.command(name="quarterly")
    async def freecredits_quarterly(self, ctx):
        """Get some free currency every quarter (122 days)"""

        if await bank.is_global():
            free = await self.config.quarter()
            streak = await self.config.streaks.quarter()
            perc = await self.config.streaks.percent()
            config = self.config.user(ctx.author)
        else:
            free = await self.config.guild(ctx.guild).quarter()
            streak = await self.config.guild(ctx.guild).streaks.quarter()
            perc = await self.config.guild(ctx.guild).streaks.percent()
            config = self.config.member(ctx.author)

        if free > 0:
            last = datetime.fromisoformat(await config.quarter())
            now = datetime.now().astimezone().replace(microsecond=0)

            if streak > 0 and (timedelta(days=244) > (now - last) >= timedelta(days=122)):
                if perc:
                    streak = free * streak
                await bank.deposit_credits(ctx.author, free + streak)
                await config.quarter.set(now.isoformat())
                await ctx.send(
                    "You have been given {} {} plus {} for maintaining a streak".format(
                        free, (await bank.get_currency_name()), streak
                    )
                )
            elif (now - last) >= timedelta(days=122):
                await bank.deposit_credits(ctx.author, free)
                await config.quarter.set(now.isoformat())
                await ctx.send(
                    "You have been given {} {}".format(free, (await bank.get_currency_name()))
                )
            else:
                await ctx.send(
                    "Sorry, you still have {} until your next quarterly bonus".format(
                        humanize_timedelta(timedelta=(timedelta(days=122) - (now - last)))
                    )
                )

    @lc.yearly()
    @freecredits.command(name="yearly")
    async def freecredits_yearly(self, ctx):
        """Get some free currency every year (365 days)"""

        if await bank.is_global():
            free = await self.config.year()
            streak = await self.config.streaks.year()
            perc = await self.config.streaks.percent()
            config = self.config.user(ctx.author)
        else:
            free = await self.config.guild(ctx.guild).year()
            streak = await self.config.guild(ctx.guild).streaks.year()
            perc = await self.config.guild(ctx.guild).streaks.percent()
            config = self.config.member(ctx.author)

        if free > 0:
            last = datetime.fromisoformat(await config.year())
            now = datetime.now().astimezone().replace(microsecond=0)

            if streak > 0 and (timedelta(days=730) > (now - last) >= timedelta(days=365)):
                if perc:
                    streak = free * streak
                await bank.deposit_credits(ctx.author, free + streak)
                await config.year.set(now.isoformat())
                await ctx.send(
                    "You have been given {} {} plus {} for maintaining a streak".format(
                        free, (await bank.get_currency_name()), streak
                    )
                )
            elif (now - last) >= timedelta(days=365):
                await bank.deposit_credits(ctx.author, free)
                await config.year.set(now.isoformat())
                await ctx.send(
                    "You have been given {} {}".format(free, (await bank.get_currency_name()))
                )
            else:
                await ctx.send(
                    "Sorry, you still have {} until your next yearly bonus".format(
                        humanize_timedelta(timedelta=(timedelta(days=365) - (now - last)))
                    )
                )

    @lc.is_owner_if_bank_global()
    @checks.guildowner_or_permissions(administrator=True)
    @commands.group()
    async def pdconfig(self, ctx):
        """
        Configure the `freecredits` options

        More detailed docs: <https://cogs.yamikaitou.dev/payday.html#pdconfig>
        """

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
        """
        Configure the `hourly` options

        Setting this to 0 will disable the command
        """

        if value < 0:
            return await ctx.send("You must provide a non-negative value or 0")
        try:
            if await bank.is_global():
                await self.config.hour.set(value)
            else:
                await self.config.guild(ctx.guild).hour.set(value)
        except Exception as e:
            raise e
        else:
            if not await ctx.tick():
                await ctx.send("Setting saved")

    @lc.is_owner_if_bank_global()
    @checks.guildowner_or_permissions(administrator=True)
    @pdconfig.command(name="daily", aliases=["day"])
    async def pdconfig_daily(self, ctx, value: int):
        """
        Configure the `daily` options

        Setting this to 0 will disable the command"""

        if value < 0:
            return await ctx.send("You must provide a non-negative value or 0")
        try:
            if await bank.is_global():
                await self.config.day.set(value)
            else:
                await self.config.guild(ctx.guild).day.set(value)
        except Exception as e:
            raise e
        else:
            if not await ctx.tick():
                await ctx.send("Setting saved")

    @lc.is_owner_if_bank_global()
    @checks.guildowner_or_permissions(administrator=True)
    @pdconfig.command(name="weekly", aliases=["week"])
    async def pdconfig_weekly(self, ctx, value: int):
        """
        Configure the `weekly` options

        Setting this to 0 will disable the command
        """

        if value < 0:
            return await ctx.send("You must provide a non-negative value or 0")
        try:
            if await bank.is_global():
                await self.config.week.set(value)
            else:
                await self.config.guild(ctx.guild).week.set(value)
        except Exception as e:
            raise e
        else:
            if not await ctx.tick():
                await ctx.send("Setting saved")

    @lc.is_owner_if_bank_global()
    @checks.guildowner_or_permissions(administrator=True)
    @pdconfig.command(name="monthly", aliases=["month"])
    async def pdconfig_monthly(self, ctx, value: int):
        """
        Configure the `monthly` options

        Setting this to 0 will disable the command
        """

        if value < 0:
            return await ctx.send("You must provide a non-negative value or 0")
        try:
            if await bank.is_global():
                await self.config.month.set(value)
            else:
                await self.config.guild(ctx.guild).month.set(value)
        except Exception as e:
            raise e
        else:
            if not await ctx.tick():
                await ctx.send("Setting saved")

    @lc.is_owner_if_bank_global()
    @checks.guildowner_or_permissions(administrator=True)
    @pdconfig.command(name="quarterly", aliases=["quarter"])
    async def pdconfig_quarterly(self, ctx, value: int):
        """
        Configure the `quarterly` options

        Setting this to 0 will disable the command
        """

        if value < 0:
            return await ctx.send("You must provide a non-negative value or 0")
        try:
            if await bank.is_global():
                await self.config.quarter.set(value)
            else:
                await self.config.guild(ctx.guild).quarter.set(value)
        except Exception as e:
            raise e
        else:
            if not await ctx.tick():
                await ctx.send("Setting saved")

    @lc.is_owner_if_bank_global()
    @checks.guildowner_or_permissions(administrator=True)
    @pdconfig.command(name="yearly", aliases=["year"])
    async def pdconfig_yearly(self, ctx, value: int):
        """
        Configure the `yearly` options

        Setting this to 0 will disable the command
        """

        if value < 0:
            return await ctx.send("You must provide a non-negative value or 0")
        try:
            if await bank.is_global():
                await self.config.year.set(value)
            else:
                await self.config.guild(ctx.guild).year.set(value)
        except Exception as e:
            raise e
        else:
            if not await ctx.tick():
                await ctx.send("Setting saved")

    @lc.is_owner_if_bank_global()
    @checks.guildowner_or_permissions(administrator=True)
    @pdconfig.group(name="streaks")
    async def pdconfig_streaks(self, ctx):
        """Configure the `streaks` options"""

    @lc.is_owner_if_bank_global()
    @checks.guildowner_or_permissions(administrator=True)
    @pdconfig_streaks.command(name="hourly", aliases=["hour"])
    async def pdconfig_streaks_hourly(self, ctx, value: int):
        """
        Configure the `hourly` streaks value

        Setting this to 0 will disable the streak bonus
        """

        if value < 0:
            return await ctx.send("You must provide a non-negative value or 0")
        try:
            if await bank.is_global():
                await self.config.streaks.hour.set(value)
            else:
                await self.config.guild(ctx.guild).streaks.hour.set(value)
        except Exception as e:
            raise e
        else:
            if not await ctx.tick():
                await ctx.send("Setting saved")

    @lc.is_owner_if_bank_global()
    @checks.guildowner_or_permissions(administrator=True)
    @pdconfig_streaks.command(name="daily", aliases=["day"])
    async def pdconfig_streaks_daily(self, ctx, value: int):
        """
        Configure the `daily` streaks value

        Setting this to 0 will disable the streak bonus
        """

        if value < 0:
            return await ctx.send("You must provide a non-negative value or 0")
        try:
            if await bank.is_global():
                await self.config.streaks.day.set(value)
            else:
                await self.config.guild(ctx.guild).streaks.day.set(value)
        except Exception as e:
            raise e
        else:
            if not await ctx.tick():
                await ctx.send("Setting saved")

    @lc.is_owner_if_bank_global()
    @checks.guildowner_or_permissions(administrator=True)
    @pdconfig_streaks.command(name="weekly", aliases=["week"])
    async def pdconfig_streaks_weekly(self, ctx, value: int):
        """
        Configure the `weekly` streaks value

        Setting this to 0 will disable the streak bonus
        """

        if value < 0:
            return await ctx.send("You must provide a non-negative value or 0")
        try:
            if await bank.is_global():
                await self.config.streaks.week.set(value)
            else:
                await self.config.guild(ctx.guild).streaks.week.set(value)
        except Exception as e:
            raise e
        else:
            if not await ctx.tick():
                await ctx.send("Setting saved")

    @lc.is_owner_if_bank_global()
    @checks.guildowner_or_permissions(administrator=True)
    @pdconfig_streaks.command(name="monthly", aliases=["month"])
    async def pdconfig_streaks_monthly(self, ctx, value: int):
        """
        Configure the `monthly` streaks value

        Setting this to 0 will disable the streak bonus
        """

        if value < 0:
            return await ctx.send("You must provide a non-negative value or 0")
        try:
            if await bank.is_global():
                await self.config.streaks.month.set(value)
            else:
                await self.config.guild(ctx.guild).streaks.month.set(value)
        except Exception as e:
            raise e
        else:
            if not await ctx.tick():
                await ctx.send("Setting saved")

    @lc.is_owner_if_bank_global()
    @checks.guildowner_or_permissions(administrator=True)
    @pdconfig_streaks.command(name="quarterly", aliases=["quarter"])
    async def pdconfig_streaks_quarterly(self, ctx, value: int):
        """
        Configure the `quarterly` streaks value

        Setting this to 0 will disable the streak bonus
        """

        if value < 0:
            return await ctx.send("You must provide a non-negative value or 0")
        try:
            if await bank.is_global():
                await self.config.streaks.quarter.set(value)
            else:
                await self.config.guild(ctx.guild).streaks.quarter.set(value)
        except Exception as e:
            raise e
        else:
            if not await ctx.tick():
                await ctx.send("Setting saved")

    @lc.is_owner_if_bank_global()
    @checks.guildowner_or_permissions(administrator=True)
    @pdconfig_streaks.command(name="yearly", aliases=["year"])
    async def pdconfig_streaks_yearly(self, ctx, value: int):
        """
        Configure the `yearly` streaks value

        Setting this to 0 will disable the streak bonus
        """

        if value < 0:
            return await ctx.send("You must provide a non-negative value or 0")
        try:
            if await bank.is_global():
                await self.config.streaks.year.set(value)
            else:
                await self.config.guild(ctx.guild).streaks.year.set(value)
        except Exception as e:
            raise e
        else:
            if not await ctx.tick():
                await ctx.send("Setting saved")

    @lc.is_owner_if_bank_global()
    @checks.guildowner_or_permissions(administrator=True)
    @pdconfig_streaks.command(name="percent", aliases=["percentage"])
    async def pdconfig_streaks_percentage(self, ctx, state: bool):
        """
        Configure streaks to be a percentage or flat amount

        <state> should be any of these combinations, `on/off`, `yes/no`, `1/0`, `true/false`
        """

        try:
            if await bank.is_global():
                await self.config.streaks.percent.set(state)
            else:
                await self.config.guild(ctx.guild).streaks.percent.set(state)
        except Exception as e:
            raise e
        else:
            if not await ctx.tick():
                await ctx.send("Setting saved")

    @lc.is_owner_if_bank_global()
    @checks.guildowner_or_permissions(administrator=True)
    @pdconfig.command(name="debug", hidden=True)
    async def pdconfig_debug(self, ctx, person: Union[discord.Member, discord.User]):
        """Pull some config data for a specific user/member, useful for Support questions"""

        if await bank.is_global():
            amounts = await self.config.all()
            times = await self.config.user(person).all()

            await ctx.send(
                "```"
                "Global Settings\n"
                f"{tabulate(amounts.items())}\n\n"
                f"User Settings for {person.id}\n"
                f"{tabulate(times.items())}"
                "```"
            )
        else:
            amounts = await self.config.guild(ctx.guild).all()
            times = await self.config.member(person).all()

            await ctx.send(
                "```"
                "Guild Settings\n"
                f"{tabulate(amounts.items())}\n\n"
                f"Member Settings for {person.id}\n"
                f"{tabulate(times.items())}"
                "```"
            )

    @lc.is_owner_if_bank_global()
    @checks.guildowner_or_permissions(administrator=True)
    @pdconfig.command(name="reset", hidden=True)
    async def pdconfig_reset(
        self, ctx, person: Union[discord.Member, discord.User], *, options: str
    ):
        """
        Forcibly reset the time for a user. WARNING, this will allow the user to claim the credits right away

        For <options>, you can provide any combination of the following (seperate by a space to include multiple)
        hour
        day
        week
        month
        quarter
        year
        """

        try:
            if await bank.is_global():
                for opt in options.split():
                    await self.config.user(person).set_raw(opt, value="2016-01-02T04:25:00-04:00")
            else:
                for opt in options.split():
                    await self.config.member(person).set_raw(
                        opt, value="2016-01-02T04:25:00-04:00"
                    )
        except Exception as e:
            raise e
        else:
            await ctx.send(f"The provided times for {person.display_name} have been reset")

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

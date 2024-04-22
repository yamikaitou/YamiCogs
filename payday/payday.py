import logging
import math
from datetime import datetime, timedelta
from typing import Literal, Union

import discord
from redbot.core import Config, bank, checks, commands
from redbot.core.bot import Red
from redbot.core.i18n import Translator, cog_i18n
from redbot.core.utils import AsyncIter
from redbot.core.utils.chat_formatting import box, humanize_timedelta
from tabulate import tabulate

log = logging.getLogger("red.yamicogs.payday")

_ = Translator("Talk", __file__)


def cmd_check(option):
    async def pred(ctx: commands.Context):
        if await bank.is_global():
            if await ctx.bot.get_cog("PayDay").config.get_raw(option) > 0:
                return True
        elif not await bank.is_global() and ctx.guild is not None:
            if await ctx.bot.get_cog("PayDay").config.guild(ctx.guild).get_raw(option) > 0:
                return True
        else:
            return False

    return commands.check(pred)


def cmd_all():
    async def pred(ctx: commands.Context):
        if await bank.is_global():
            return True
        elif not await bank.is_global() and ctx.guild is not None:
            return True
        else:
            return False

    return commands.check(pred)


# taken from Red-Discordbot economy.py
def guild_only_check():
    async def pred(ctx: commands.Context):
        if await bank.is_global():
            return True
        elif not await bank.is_global() and ctx.guild is not None:
            return True
        else:
            return False

    return commands.check(pred)


# taken from Red-Discordbot bank.py
def is_owner_if_bank_global():
    """
    Command decorator. If the bank is global, it checks if the author is
    bot owner, otherwise it only checks
    if command was used in guild - it DOES NOT check any permissions.
    When used on the command, this should be combined
    with permissions check like `guildowner_or_permissions()`.
    """

    async def pred(ctx: commands.Context):
        author = ctx.author
        if not await bank.is_global():
            if not ctx.guild:
                return False
            return True
        else:
            return await ctx.bot.is_owner(author)

    return commands.check(pred)


@cog_i18n(_)
class PayDay(commands.Cog):
    """
    Customizable PayDay system

    More detailed docs: <https://cogs.yamikaitou.dev/payday.html>
    """

    settings = {"day": 1, "week": 7, "month": 30, "quarter": 91, "year": 365}
    friendly = {
        "hour": "Hourly",
        "day": "Daily",
        "week": "Weekly",
        "month": "Monthly",
        "quarter": "Quarterly",
        "year": "Yearly",
    }
    times = {
        "hour": 1,
        "day": 24,
        "week": 168,
        "month": 720,
        "quarter": 2184,
        "year": 8760,
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

    @guild_only_check()
    @commands.group()
    async def freecredits(self, ctx):
        """More options to get free credits"""

    @cmd_all()
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
                    else _("Available Now!")
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
                        else _("Available Now!")
                    )
                    + "\n"
                )
        if strings == "":
            await ctx.send(_("No freecredit options have been configured yet"))
        else:
            await ctx.send(strings)

    @cmd_all()
    @freecredits.command(name="all")
    async def freecredits_all(self, ctx):
        """Claim all available freecredits"""

        total_amount = 0
        total_streak = 0

        for k in self.friendly:
            free, streak, remain = await self.grant_award(ctx, k, False)
            if remain != -1:
                continue
            elif streak != -1:
                total_amount += free
                total_streak += streak
            elif free != -1:
                total_amount += free

        bankname = await bank.get_currency_name(ctx.guild)
        if total_streak > 0:
            await bank.deposit_credits(ctx.author, total_amount + total_streak)
            await ctx.send(
                _(
                    "You have claimed all available {bankname} from the `freecredits` program! +{total_amount} {bankname}\nPlus an additional {total_streak} for maintaining your streaks"
                ).format(bankname=bankname, total_amount=total_amount, total_streak=total_streak)
            )
        elif total_amount > 0:
            await bank.deposit_credits(ctx.author, total_amount)
            await ctx.send(
                _(
                    "You have claimed all available {bankname} from the `freecredits` program! +{total_amount} {bankname}"
                ).format(bankname=bankname, total_amount=total_amount)
            )
        else:
            await ctx.send(
                _("You have no available {bankname} for claiming.").format(bankname=bankname)
            )

    @cmd_check("hour")
    @freecredits.command(name="hourly")
    async def freecredits_hourly(self, ctx):
        """Get some free currency every hour"""

        free, streak, remain = await self.grant_award(ctx, "hour")

        if remain != -1:
            await ctx.send(
                _("Sorry, you still have {remain} until your next hourly bonus").format(
                    remain=remain
                )
            )
        elif streak != -1:
            await ctx.send(
                _(
                    "You have been given {free_credits} {bankname} plus {streak_bonus} for maintaining a streak"
                ).format(
                    free_credits=free,
                    bankname=(await bank.get_currency_name(ctx.guild)),
                    streak_bonus=streak,
                )
            )
        elif free != -1:
            await ctx.send(
                _("You have been given {free_credits} {bankname}").format(
                    free_credits=free, bankname=(await bank.get_currency_name(ctx.guild))
                )
            )
        else:
            log.debug("grant_award returned no results")

    @cmd_check("day")
    @freecredits.command(name="daily")
    async def freecredits_daily(self, ctx):
        """Get some free currency every day"""

        free, streak, remain = await self.grant_award(ctx, "day")

        if remain != -1:
            await ctx.send(
                _("Sorry, you still have {remain} until your next dailya bonus").format(
                    remain=remain
                )
            )
        elif streak != -1:
            await ctx.send(
                _(
                    "You have been given {free_credits} {bankname} plus {streak_bonus} for maintaining a streak"
                ).format(
                    free_credits=free,
                    bankname=(await bank.get_currency_name(ctx.guild)),
                    streak_bonus=streak,
                )
            )
        elif free != -1:
            await ctx.send(
                _("You have been given {free_credits} {bankname}").format(
                    free_credits=free, bankname=(await bank.get_currency_name(ctx.guild))
                )
            )
        else:
            log.debug("grant_award returned no results")

    @cmd_check("week")
    @freecredits.command(name="weekly")
    async def freecredits_weekly(self, ctx):
        """Get some free currency every week (7 days)"""

        free, streak, remain = await self.grant_award(ctx, "week")

        if remain != -1:
            await ctx.send(
                _("Sorry, you still have {remain} until your next weekly bonus").format(
                    remain=remain
                )
            )
        elif streak != -1:
            await ctx.send(
                _(
                    "You have been given {free_credits} {bankname} plus {streak_bonus} for maintaining a streak"
                ).format(
                    free_credits=free,
                    bankname=(await bank.get_currency_name(ctx.guild)),
                    streak_bonus=streak,
                )
            )
        elif free != -1:
            await ctx.send(
                _("You have been given {free_credits} {bankname}").format(
                    free_credits=free, bankname=(await bank.get_currency_name(ctx.guild))
                )
            )
        else:
            log.debug("grant_award returned no results")

    @cmd_check("month")
    @freecredits.command(name="monthly")
    async def freecredits_monthly(self, ctx):
        """Get some free currency every month (30 days)"""

        free, streak, remain = await self.grant_award(ctx, "month")

        if remain != -1:
            await ctx.send(
                _("Sorry, you still have {remain} until your next monthly bonus").format(
                    remain=remain
                )
            )
        elif streak != -1:
            await ctx.send(
                _(
                    "You have been given {free_credits} {bankname} plus {streak_bonus} for maintaining a streak"
                ).format(
                    free_credits=free,
                    bankname=(await bank.get_currency_name(ctx.guild)),
                    streak_bonus=streak,
                )
            )
        elif free != -1:
            await ctx.send(
                _("You have been given {free_credits} {bankname}").format(
                    free_credits=free, bankname=(await bank.get_currency_name(ctx.guild))
                )
            )
        else:
            log.debug("grant_award returned no results")

    @cmd_check("quarter")
    @freecredits.command(name="quarterly")
    async def freecredits_quarterly(self, ctx):
        """Get some free currency every quarter (122 days)"""

        free, streak, remain = await self.grant_award(ctx, "quarter")

        if remain != -1:
            await ctx.send(
                _("Sorry, you still have {remain} until your next quarterly bonus").format(
                    remain=remain
                )
            )
        elif streak != -1:
            await ctx.send(
                _(
                    "You have been given {free_credits} {bankname} plus {streak_bonus} for maintaining a streak"
                ).format(
                    free_credits=free,
                    bankname=(await bank.get_currency_name(ctx.guild)),
                    streak_bonus=streak,
                )
            )
        elif free != -1:
            await ctx.send(
                _("You have been given {free_credits} {bankname}").format(
                    free_credits=free, bankname=(await bank.get_currency_name(ctx.guild))
                )
            )
        else:
            log.debug("grant_award returned no results")

    @cmd_check("year")
    @freecredits.command(name="yearly")
    async def freecredits_yearly(self, ctx):
        """Get some free currency every year (365 days)"""

        free, streak, remain = await self.grant_award(ctx, "year")

        if remain != -1:
            await ctx.send(
                _("Sorry, you still have {remain} until your next yearly bonus").format(
                    remain=remain
                )
            )
        elif streak != -1:
            await ctx.send(
                _(
                    "You have been given {free_credits} {bankname} plus {streak_bonus} for maintaining a streak"
                ).format(
                    free_credits=free,
                    bankname=(await bank.get_currency_name(ctx.guild)),
                    streak_bonus=streak,
                )
            )
        elif free != -1:
            await ctx.send(
                _("You have been given {free_credits} {bankname}").format(
                    free_credits=free, bankname=(await bank.get_currency_name(ctx.guild))
                )
            )
        else:
            log.debug("grant_award returned no results")

    async def grant_award(self, ctx, option, deposit=True):
        if await bank.is_global():
            free = await self.config.get_raw(option)
            streak = await self.config.streaks.get_raw(option)
            perc = await self.config.streaks.percent()
            config = self.config.user(ctx.author)
        else:
            free = await self.config.guild(ctx.guild).get_raw(option)
            streak = await self.config.guild(ctx.guild).streaks.get_raw(option)
            perc = await self.config.guild(ctx.guild).streaks.percent()
            config = self.config.member(ctx.author)

        if free > 0:
            last = datetime.fromisoformat(await config.get_raw(option))
            now = datetime.now().astimezone().replace(microsecond=0)

            if streak > 0 and (
                timedelta(hours=(self.times[option] * 2))
                > (now - last)
                >= timedelta(hours=self.times[option])
            ):
                if perc:
                    streak = free * math.floor(streak / 100)
                if deposit:
                    await bank.deposit_credits(ctx.author, free + streak)
                await config.set_raw(option, value=now.isoformat())
                return (free, streak, -1)
            elif (now - last) >= timedelta(hours=self.times[option]):
                if deposit:
                    await bank.deposit_credits(ctx.author, free)
                await config.set_raw(option, value=now.isoformat())
                return (free, -1, -1)
            else:
                return (
                    0,
                    0,
                    humanize_timedelta(
                        timedelta=(timedelta(hours=self.times[option]) - (now - last))
                    ),
                )

        return (-1, -1, -1)

    @is_owner_if_bank_global()
    @checks.guildowner_or_permissions(administrator=True)
    @commands.group()
    async def pdconfig(self, ctx):
        """
        Configure the `freecredits` options

        More detailed docs: <https://cogs.yamikaitou.dev/payday.html#pdconfig>
        """

    @is_owner_if_bank_global()
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

    @is_owner_if_bank_global()
    @checks.guildowner_or_permissions(administrator=True)
    @pdconfig.command(name="hourly", aliases=["hour"])
    async def pdconfig_hourly(self, ctx, value: int):
        """
        Configure the `hourly` options

        Setting this to 0 will disable the command
        """

        if value < 0:
            return await ctx.send(_("You must provide a non-negative value or 0"))
        try:
            if await bank.is_global():
                await self.config.hour.set(value)
            else:
                await self.config.guild(ctx.guild).hour.set(value)
        except Exception as e:
            raise e
        else:
            if not await ctx.tick():
                await ctx.send(_("Setting saved"))

    @is_owner_if_bank_global()
    @checks.guildowner_or_permissions(administrator=True)
    @pdconfig.command(name="daily", aliases=["day"])
    async def pdconfig_daily(self, ctx, value: int):
        """
        Configure the `daily` options

        Setting this to 0 will disable the command"""

        if value < 0:
            return await ctx.send(_("You must provide a non-negative value or 0"))
        try:
            if await bank.is_global():
                await self.config.day.set(value)
            else:
                await self.config.guild(ctx.guild).day.set(value)
        except Exception as e:
            raise e
        else:
            if not await ctx.tick():
                await ctx.send(_("Setting saved"))

    @is_owner_if_bank_global()
    @checks.guildowner_or_permissions(administrator=True)
    @pdconfig.command(name="weekly", aliases=["week"])
    async def pdconfig_weekly(self, ctx, value: int):
        """
        Configure the `weekly` options

        Setting this to 0 will disable the command
        """

        if value < 0:
            return await ctx.send(_("You must provide a non-negative value or 0"))
        try:
            if await bank.is_global():
                await self.config.week.set(value)
            else:
                await self.config.guild(ctx.guild).week.set(value)
        except Exception as e:
            raise e
        else:
            if not await ctx.tick():
                await ctx.send(_("Setting saved"))

    @is_owner_if_bank_global()
    @checks.guildowner_or_permissions(administrator=True)
    @pdconfig.command(name="monthly", aliases=["month"])
    async def pdconfig_monthly(self, ctx, value: int):
        """
        Configure the `monthly` options

        Setting this to 0 will disable the command
        """

        if value < 0:
            return await ctx.send(_("You must provide a non-negative value or 0"))
        try:
            if await bank.is_global():
                await self.config.month.set(value)
            else:
                await self.config.guild(ctx.guild).month.set(value)
        except Exception as e:
            raise e
        else:
            if not await ctx.tick():
                await ctx.send(_("Setting saved"))

    @is_owner_if_bank_global()
    @checks.guildowner_or_permissions(administrator=True)
    @pdconfig.command(name="quarterly", aliases=["quarter"])
    async def pdconfig_quarterly(self, ctx, value: int):
        """
        Configure the `quarterly` options

        Setting this to 0 will disable the command
        """

        if value < 0:
            return await ctx.send(_("You must provide a non-negative value or 0"))
        try:
            if await bank.is_global():
                await self.config.quarter.set(value)
            else:
                await self.config.guild(ctx.guild).quarter.set(value)
        except Exception as e:
            raise e
        else:
            if not await ctx.tick():
                await ctx.send(_("Setting saved"))

    @is_owner_if_bank_global()
    @checks.guildowner_or_permissions(administrator=True)
    @pdconfig.command(name="yearly", aliases=["year"])
    async def pdconfig_yearly(self, ctx, value: int):
        """
        Configure the `yearly` options

        Setting this to 0 will disable the command
        """

        if value < 0:
            return await ctx.send(_("You must provide a non-negative value or 0"))
        try:
            if await bank.is_global():
                await self.config.year.set(value)
            else:
                await self.config.guild(ctx.guild).year.set(value)
        except Exception as e:
            raise e
        else:
            if not await ctx.tick():
                await ctx.send(_("Setting saved"))

    @is_owner_if_bank_global()
    @checks.guildowner_or_permissions(administrator=True)
    @pdconfig.group(name="streaks")
    async def pdconfig_streaks(self, ctx):
        """Configure the `streaks` options"""

    @is_owner_if_bank_global()
    @checks.guildowner_or_permissions(administrator=True)
    @pdconfig_streaks.command(name="hourly", aliases=["hour"])
    async def pdconfig_streaks_hourly(self, ctx, value: int):
        """
        Configure the `hourly` streaks value

        Setting this to 0 will disable the streak bonus
        """

        if value < 0:
            return await ctx.send(_("You must provide a non-negative value or 0"))
        try:
            if await bank.is_global():
                await self.config.streaks.hour.set(value)
            else:
                await self.config.guild(ctx.guild).streaks.hour.set(value)
        except Exception as e:
            raise e
        else:
            if not await ctx.tick():
                await ctx.send(_("Setting saved"))

    @is_owner_if_bank_global()
    @checks.guildowner_or_permissions(administrator=True)
    @pdconfig_streaks.command(name="daily", aliases=["day"])
    async def pdconfig_streaks_daily(self, ctx, value: int):
        """
        Configure the `daily` streaks value

        Setting this to 0 will disable the streak bonus
        """

        if value < 0:
            return await ctx.send(_("You must provide a non-negative value or 0"))
        try:
            if await bank.is_global():
                await self.config.streaks.day.set(value)
            else:
                await self.config.guild(ctx.guild).streaks.day.set(value)
        except Exception as e:
            raise e
        else:
            if not await ctx.tick():
                await ctx.send(_("Setting saved"))

    @is_owner_if_bank_global()
    @checks.guildowner_or_permissions(administrator=True)
    @pdconfig_streaks.command(name="weekly", aliases=["week"])
    async def pdconfig_streaks_weekly(self, ctx, value: int):
        """
        Configure the `weekly` streaks value

        Setting this to 0 will disable the streak bonus
        """

        if value < 0:
            return await ctx.send(_("You must provide a non-negative value or 0"))
        try:
            if await bank.is_global():
                await self.config.streaks.week.set(value)
            else:
                await self.config.guild(ctx.guild).streaks.week.set(value)
        except Exception as e:
            raise e
        else:
            if not await ctx.tick():
                await ctx.send(_("Setting saved"))

    @is_owner_if_bank_global()
    @checks.guildowner_or_permissions(administrator=True)
    @pdconfig_streaks.command(name="monthly", aliases=["month"])
    async def pdconfig_streaks_monthly(self, ctx, value: int):
        """
        Configure the `monthly` streaks value

        Setting this to 0 will disable the streak bonus
        """

        if value < 0:
            return await ctx.send(_("You must provide a non-negative value or 0"))
        try:
            if await bank.is_global():
                await self.config.streaks.month.set(value)
            else:
                await self.config.guild(ctx.guild).streaks.month.set(value)
        except Exception as e:
            raise e
        else:
            if not await ctx.tick():
                await ctx.send(_("Setting saved"))

    @is_owner_if_bank_global()
    @checks.guildowner_or_permissions(administrator=True)
    @pdconfig_streaks.command(name="quarterly", aliases=["quarter"])
    async def pdconfig_streaks_quarterly(self, ctx, value: int):
        """
        Configure the `quarterly` streaks value

        Setting this to 0 will disable the streak bonus
        """

        if value < 0:
            return await ctx.send(_("You must provide a non-negative value or 0"))
        try:
            if await bank.is_global():
                await self.config.streaks.quarter.set(value)
            else:
                await self.config.guild(ctx.guild).streaks.quarter.set(value)
        except Exception as e:
            raise e
        else:
            if not await ctx.tick():
                await ctx.send(_("Setting saved"))

    @is_owner_if_bank_global()
    @checks.guildowner_or_permissions(administrator=True)
    @pdconfig_streaks.command(name="yearly", aliases=["year"])
    async def pdconfig_streaks_yearly(self, ctx, value: int):
        """
        Configure the `yearly` streaks value

        Setting this to 0 will disable the streak bonus
        """

        if value < 0:
            return await ctx.send(_("You must provide a non-negative value or 0"))
        try:
            if await bank.is_global():
                await self.config.streaks.year.set(value)
            else:
                await self.config.guild(ctx.guild).streaks.year.set(value)
        except Exception as e:
            raise e
        else:
            if not await ctx.tick():
                await ctx.send(_("Setting saved"))

    @is_owner_if_bank_global()
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
                await ctx.send(_("Setting saved"))

    @is_owner_if_bank_global()
    @checks.guildowner_or_permissions(administrator=True)
    @pdconfig.command(name="debug", hidden=True)
    async def pdconfig_debug(self, ctx, person: Union[discord.Member, discord.User]):
        """Pull some config data for a specific user/member, useful for Support questions"""

        if await bank.is_global():
            amounts = await self.config.all()
            times = await self.config.user(person).all()

            await ctx.send(
                "```{global_label}\n{global_items}\n\n{user_label}\n{user_items}```".format(
                    global_label=_("Global Settings"),
                    global_items=tabulate(amounts.items()),
                    user_label=_("User Settings for {person}").format(person=person.id),
                    user_items=tabulate(times.items()),
                )
            )
        else:
            amounts = await self.config.guild(ctx.guild).all()
            times = await self.config.member(person).all()

            await ctx.send(
                "```{global_label}\n{global_items}\n\n{user_label}\n{user_items}```".format(
                    global_label=_("Global Settings"),
                    global_items=tabulate(amounts.items()),
                    user_label=_("Member Settings for {person}").format(person=person.id),
                    user_items=tabulate(times.items()),
                )
            )

    @is_owner_if_bank_global()
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
            await ctx.send(
                _("The provided times for {person} have been reset").format(
                    person=person.display_name
                )
            )

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

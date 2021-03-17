from redbot.core import bank, commands


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
            return bool(ctx.guild)
        else:
            return await ctx.bot.is_owner(author)

    return commands.check(pred)


def all():
    async def pred(ctx: commands.Context):
        if await bank.is_global():
            return True
        elif not await bank.is_global() and ctx.guild is not None:
            return True
        else:
            return False

    return commands.check(pred)


def hourly():
    async def pred(ctx: commands.Context):
        if await bank.is_global():
            if await ctx.bot.get_cog("PayDay").config.hour() > 0:
                return True
        elif not await bank.is_global() and ctx.guild is not None:
            if await ctx.bot.get_cog("PayDay").config.guild(ctx.guild).hour() > 0:
                return True
        else:
            return False

    return commands.check(pred)


def daily():
    async def pred(ctx: commands.Context):
        if await bank.is_global():
            if await ctx.bot.get_cog("PayDay").config.day() > 0:
                return True
        elif not await bank.is_global() and ctx.guild is not None:
            if await ctx.bot.get_cog("PayDay").config.guild(ctx.guild).day() > 0:
                return True
        else:
            return False

    return commands.check(pred)


def weekly():
    async def pred(ctx: commands.Context):
        if await bank.is_global():
            if await ctx.bot.get_cog("PayDay").config.week() > 0:
                return True
        elif not await bank.is_global() and ctx.guild is not None:
            if await ctx.bot.get_cog("PayDay").config.guild(ctx.guild).week() > 0:
                return True
        else:
            return False

    return commands.check(pred)


def monthly():
    async def pred(ctx: commands.Context):
        if await bank.is_global():
            if await ctx.bot.get_cog("PayDay").config.month() > 0:
                return True
        elif not await bank.is_global() and ctx.guild is not None:
            if await ctx.bot.get_cog("PayDay").config.guild(ctx.guild).month() > 0:
                return True
        else:
            return False

    return commands.check(pred)


def quarterly():
    async def pred(ctx: commands.Context):
        if await bank.is_global():
            if await ctx.bot.get_cog("PayDay").config.quarter() > 0:
                return True
        elif not await bank.is_global() and ctx.guild is not None:
            if await ctx.bot.get_cog("PayDay").config.guild(ctx.guild).quarter() > 0:
                return True
        else:
            return False

    return commands.check(pred)


def yearly():
    async def pred(ctx: commands.Context):
        if await bank.is_global():
            if await ctx.bot.get_cog("PayDay").config.year() > 0:
                return True
        elif not await bank.is_global() and ctx.guild is not None:
            if await ctx.bot.get_cog("PayDay").config.guild(ctx.guild).year() > 0:
                return True
        else:
            return False

    return commands.check(pred)

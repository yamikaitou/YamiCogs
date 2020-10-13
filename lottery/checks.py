from redbot.core import commands


def lucky3_enabled():
    async def pred(ctx: commands.Context):
        return await ctx.bot.get_cog("Lottery").config.guild(ctx.guild).lucky3.enable()

    return commands.check(pred)
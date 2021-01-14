import random

import discord
from redbot.core import Config, checks, commands


class Kill(commands.Cog):
    """
    Kill people in interesting ways
    """

    __version__ = "2.3"

    def format_help_for_context(self, ctx):
        """Thanks Sinbad."""
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\nCog Version: {self.__version__}"

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(
            self, identifier=582650109, force_registration=True
        )
        self.config.register_guild(
            **{
                "msg": ["{killer} slays {victim}"],
                "selfkill": "Per the Laws of Robotics, I cannot assist you in killing yourself",
                "botkill": "Wow, how original. I laugh at your feeble attempt to kill me",
            }
        )

    @commands.group()
    @checks.admin_or_permissions(manage_guild=True)
    async def killset(self, ctx):
        """
        Configure the kill messages

        More detailed docs: <https://cogs.yamikaitou.dev/kill.html#killset>
        """

    @killset.command(name="add")
    async def _add(self, ctx, *, msg):
        """
        Add a new kill message.

        {killer} and {victim} will be replaced with a users mention
        {killer2} and {victim2} will be replaced with a users name in italics
        """

        async with self.config.guild(ctx.guild).msg() as kill:
            kill.append(msg)

        if not await ctx.tick():
            await ctx.send("Message added")

    @killset.command(name="delete")
    async def _delete(self, ctx, num: int):
        """
        Removes a kill message. Use `[p]killset list` to for the numbers
        """

        if num < 0:
            return await ctx.send("Negative numbers are not supported")
        async with self.config.guild(ctx.guild).msg() as kill:
            if num >= len(kill):
                return await ctx.send(
                    "Sorry, but you don't have a kill message with that number. "
                    "Please use `[p]killset list` to get the number of the message you wish to delete"
                )

            kill.pop(num)

        if not await ctx.tick():
            await ctx.send("Message removed")

    @killset.command(name="list")
    @checks.bot_has_permissions(embed_links=True)
    async def _list(self, ctx):
        """
        List all the kill messages
        """

        embed = discord.Embed(
            colour=discord.Colour(0x636BD6),
            description="{killer} and {victim} will be replaced with a users mention\n"
            "{killer2} and {victim2} will be replaced with a users name in italics",
        )
        botkill = await self.config.guild(ctx.guild).botkill()
        embed.add_field(name="Bot Kill", value=botkill)
        selfkill = await self.config.guild(ctx.guild).selfkill()
        embed.add_field(name="Self Kill", value=selfkill)
        killmsgs = await self.config.guild(ctx.guild).msg()
        k = 0
        killmsg = ""
        for msg in killmsgs:
            killmsg += "`" + str(k) + ") " + msg + "`\n"
            k += 1
        if k == 0:
            embed.add_field(
                name="Kill Messages", value="There are no messages configured"
            )
        else:
            embed.add_field(name="Kill Messages", value=killmsg)

        await ctx.send(embed=embed)

    @killset.command(name="bot")
    async def _bot(self, ctx, *, msg):
        """
        Sets the message for killing the bot

        {killer} and {victim} will be replaced with a users mention
        {killer2} and {victim2} will be replaced with a users name in italics
        """

        await self.config.guild(ctx.guild).botkill.set(msg)

        if not await ctx.tick():
            await ctx.send("Message saved")

    @killset.command(name="self")
    async def _self(self, ctx, *, msg):
        """
        Sets the message for killing yourself

        {killer} and {victim} will be replaced with a users mention
        {killer2} and {victim2} will be replaced with a users name in italics
        """

        await self.config.guild(ctx.guild).selfkill.set(msg)

        if not await ctx.tick():
            await ctx.send("Message saved")

    @commands.command()
    async def kill(self, ctx, *, user: discord.Member):
        """
        Kill a user in a random way
        """

        if user is ctx.author:
            msg = await self.config.guild(ctx.guild).selfkill()
        elif user is ctx.me:
            msg = await self.config.guild(ctx.guild).botkill()
        else:
            kills = await self.config.guild(ctx.guild).msg()
            if len(kills) == 0:
                return await ctx.send(
                    "Your life has been spared this time as I do not have any kill methods configured"
                )
            msg = kills[random.randint(0, len(kills) - 1)]

        await ctx.send(
            msg.replace("{killer}", ctx.author.mention)
            .replace("{killer2}", "*" + ctx.author.display_name + "*")
            .replace("{victim}", ctx.me.mention)
            .replace("{victim2}", "*" + user.display_name + "*")
        )

    async def red_get_data_for_user(self, *, user_id: int):
        # this cog does not store any data
        return {}

    async def red_delete_data_for_user(self, *, requester, user_id: int) -> None:
        # this cog does not store any data
        pass

import discord
import random
from redbot.core import commands, Config, checks


class Kill(commands.Cog):
    """
    Kill people in interesting ways
    """

    __version__ = "2.1"

    def format_help_for_context(self, ctx):
        """Thanks Sinbad."""
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\nCog Version: {self.__version__}"

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=582650109, force_registration=True)
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

        pass

    @killset.command(name="add")
    async def _add(self, ctx, *, msg):
        """
            Add a new kill message.
            {killer} and {victim} will be replaced with a users mention
            {killer2} and {victim2} will be replaced with a users name in italics
        """

        async with self.config.guild(ctx.guild).msg() as kill:
            kill.append(msg)

        await ctx.message.add_reaction("\U00002705")

    @killset.command(name="delete")
    async def _delete(self, ctx, num: int):
        """
            Removes a kill message. Use `[p]killset list` to for the numbers
        """

        async with self.config.guild(ctx.guild).msg() as kill:
            if num > len(kill):
                await ctx.send(
                    "Sorry, but you don't have a kill message with that number."
                    "Please use `[p]killset list` to get the number of the message you wish to delete"
                )

            kill.pop(num)

        await ctx.message.add_reaction("\U00002705")

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

        await ctx.message.add_reaction("\U00002705")

    @killset.command(name="self")
    async def _self(self, ctx, *, msg):
        """
            Sets the message for killing yourself
            {killer} and {victim} will be replaced with a users mention
            {killer2} and {victim2} will be replaced with a users name in italics
        """

        await self.config.guild(ctx.guild).selfkill.set(msg)

        await ctx.message.add_reaction("\U00002705")

    @commands.command()
    async def kill(self, ctx, *, user: discord.Member):
        """
            Kill a user in a random way
        """

        if user is ctx.author:
            msg = await self.config.guild(ctx.guild).selfkill()
        elif user is ctx.guild.me:
            msg = await self.config.guild(ctx.guild).botkill()
        else:
            kills = await self.config.guild(ctx.guild).msg()
            msg = kills[random.randint(0, len(kills) - 1)]

        await ctx.send(
            msg.format(
                killer=ctx.author.mention,
                victim=user.mention,
                killer2="*" + ctx.author.name + "*",
                victim2="*" + user.name + "*",
            )
        )
    
    async def red_get_data_for_user(self, *, user_id: int):
        # this cog does not store any data
        return {}

    async def red_delete_data_for_user(self, *, requester, user_id: int) -> None:
        # this cog does not store any data
        pass
import logging
import random

import discord
from redbot.core import Config, checks, commands
from redbot.core.i18n import Translator, cog_i18n
from redbot.core.utils.views import SimpleMenu

log = logging.getLogger("red.yamicogs.kill")
_ = Translator("Kill", __file__)


@cog_i18n(_)
class Kill(commands.Cog):
    """
    Kill people in interesting ways

    More detailed docs: <https://cogs.yamikaitou.dev/kill.html>
    """

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
            await ctx.send(_("Message added"))

    @killset.command(name="delete")
    async def _delete(self, ctx, num: int):
        """
        Removes a kill message. Use `[p]killset list` to for the numbers
        """

        if num < 0:
            return await ctx.send(_("Negative numbers are not supported"))
        async with self.config.guild(ctx.guild).msg() as kill:
            if num >= len(kill):
                return await ctx.send(
                    _(
                        "Sorry, but you don't have a kill message with that number. "
                        "Please use `[p]killset list` to get the number of the message you wish to delete"
                    )
                )

            kill.pop(num)

        if not await ctx.tick():
            await ctx.send(_("Message removed"))

    @killset.command(name="list")
    @checks.bot_has_permissions(embed_links=True)
    async def _list(self, ctx):
        """
        List all the kill messages
        """
        
        killmsgs = await self.config.guild(ctx.guild).msg()
        if not killmsgs:
            return await ctx.send(_("There are no messages configured"))

        # Pagination settings
        messages_per_page = 5  # Number of messages per embed
        total_pages = (len(killmsgs) + messages_per_page - 1) // messages_per_page  # Calculate total pages
        pages = []

        for page in range(total_pages):
            embed = discord.Embed(
                colour=discord.Colour(0x636BD6),
                title=_("Kill Messages - Page {}/{}".format(page + 1, total_pages)),
                description=_(
                    "{killer} and {victim} will be replaced with a users mention\n"
                    "{killer2} and {victim2} will be replaced with a users name in italics"
                ),
            )
            start_index = page * messages_per_page
            end_index = start_index + messages_per_page
            for k in range(start_index, min(end_index, len(killmsgs))):
                embed.add_field(name=f"{k})", value=killmsgs[k], inline=False)

            pages.append(embed)
        
        await SimpleMenu(pages).start(ctx)

    @killset.command(name="bot")
    async def _bot(self, ctx, *, msg):
        """
        Sets the message for killing the bot

        {killer} and {victim} will be replaced with a users mention
        {killer2} and {victim2} will be replaced with a users name in italics
        """

        await self.config.guild(ctx.guild).botkill.set(msg)

        if not await ctx.tick():
            await ctx.send(_("Message saved"))

    @killset.command(name="self")
    async def _self(self, ctx, *, msg):
        """
        Sets the message for killing yourself

        {killer} and {victim} will be replaced with a users mention
        {killer2} and {victim2} will be replaced with a users name in italics
        """

        await self.config.guild(ctx.guild).selfkill.set(msg)

        if not await ctx.tick():
            await ctx.send(_("Message saved"))

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
                    _(
                        "Your life has been spared this time as I do not have any kill methods configured"
                    )
                )
            msg = kills[random.randint(0, len(kills) - 1)]

        await ctx.send(
            msg.replace("{killer}", ctx.author.mention)
            .replace("{killer2}", "*" + ctx.author.display_name + "*")
            .replace("{victim}", user.mention)
            .replace("{victim2}", "*" + user.display_name + "*")
        )

    @commands.command()
    async def suicide(self, ctx):
        """
        Commit suicide
        """

        msg = await self.config.guild(ctx.guild).selfkill()
        await ctx.send(
            msg.replace("{killer}", ctx.author.mention).replace(
                "{killer2}", "*" + ctx.author.display_name + "*"
            )
        )

    async def red_get_data_for_user(self, *, user_id: int):
        # this cog does not store any data
        return {}

    async def red_delete_data_for_user(self, *, requester, user_id: int) -> None:
        # this cog does not store any data
        pass

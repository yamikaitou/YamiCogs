import logging
from typing import Literal, Optional

import discord
from redbot.core import app_commands, commands
from redbot.core.bot import Red
from redbot.core.config import Config

log = logging.getLogger("red.yamicogs.talk")

RequestType = Literal["discord_deleted_user", "owner", "user", "user_strict"]


class Talk(commands.Cog):
    """
    Talk as the bot
    """

    def __init__(self, bot: Red) -> None:
        self.bot = bot
        self.config = Config.get_conf(
            self,
            identifier=582650109,
            force_registration=True,
        )
        self.config.register_guild(**{"everyone": False})

    @commands.command(name="talk")
    @commands.mod_or_permissions(manage_messages=True)
    async def talk_prefix(self, ctx, *, message):
        """Send a message as the bot"""

        await ctx.send(content=message, allowed_mentions=discord.AllowedMentions().none())

    @commands.command(name="talkm")
    @commands.mod_or_permissions(manage_messages=True)
    async def talk_mention(self, ctx, *, message):
        """Send a message as the bot, with mentions enabled"""

        if await self.config.guild(ctx.guild).everyone():
            mention = discord.AllowedMentions(users=True, roles=True, everyone=True)
        else:
            mention = discord.AllowedMentions(users=True, roles=True, everyone=False)

        await ctx.send(content=message, allowed_mentions=mention)

    @commands.command(name="talkd")
    @commands.mod_or_permissions(manage_messages=True)
    async def talk_delete(self, ctx, *, message):
        """Send a message as the bot, but delete the command message"""

        await ctx.message.delete()
        await ctx.send(content=message, allowed_mentions=discord.AllowedMentions().none())

    @commands.command(name="talkmd")
    @commands.mod_or_permissions(manage_messages=True)
    async def talk_mention_delete(self, ctx, *, message):
        """Send a message as the bot, with mentions enabled and delete the command message"""

        if await self.config.guild(ctx.guild).everyone():
            mention = discord.AllowedMentions(users=True, roles=True, everyone=True)
        else:
            mention = discord.AllowedMentions(users=True, roles=True, everyone=False)

        await ctx.message.delete()
        await ctx.send(content=message, allowed_mentions=mention)

    @app_commands.command(name="talk")
    @app_commands.guild_only()
    @app_commands.default_permissions(manage_messages=True)
    @app_commands.describe(
        message="The message to send",
        hide="Show the command usage (default False)",
        mentions="Allow the usage of User/Role mentions (default False)",
    )
    async def talk_slash(
        self,
        interaction: discord.Interaction,
        message: str,
        hide: Optional[bool] = False,
        mentions: Optional[bool] = False,
    ):
        """Send a message as the bot"""

        if mentions:
            if await self.config.guild(interaction.guild).everyone():
                mention = discord.AllowedMentions(users=True, roles=True, everyone=True)
            else:
                mention = discord.AllowedMentions(users=True, roles=True, everyone=False)
        else:
            mention = discord.AllowedMentions(users=False, roles=False, everyone=False)

        if hide:
            await interaction.channel.send(message, allowed_mentions=mention)
        else:
            await interaction.response.send_message(message, allowed_mentions=mention)

    @commands.group(name="talkset")
    @commands.admin_or_permissions(manage_server=True)
    async def t_set(self, ctx):
        """Configure settings"""

    @t_set.command(name="everyone")
    async def ts_everyone(self, ctx, value: bool = None):
        """Set the ability to mass mention using `everyone` or `here`"""

        if value is None:
            await ctx.send(f"Current setting: {await self.config.guild(ctx.guild).everyone()}")
        else:
            await self.config.guild(ctx.guild).everyone.set(value)
            await ctx.send(f"Setting changed to {value}")

    async def red_delete_data_for_user(self, *, requester: RequestType, user_id: int) -> None:
        # this cog does not store any user data
        pass

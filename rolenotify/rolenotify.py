import logging
from typing import Union

import discord
from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.config import Config

log = logging.getLogger("red.yamicogs.rolenotify")


class RoleNotify(commands.Cog):
    """
    Notify a user when they have a Role added or removed from them

    More detailed docs: <https://cogs.yamikaitou.dev/rolenotify.html>
    """

    def __init__(self, bot: Red) -> None:
        self.bot = bot
        self.config = Config.get_conf(
            self,
            identifier=582650109,
            force_registration=True,
        )

        self.config.register_role(
            **{
                "method": "DM",
                "add": False,
                "remove": False,
                "add_msg": "You were granted the Role *{role_name}*",
                "rem_msg": "You lost the Role *{role_name}*",
                "channel": 0,
            }
        )
        self.config.register_guild(
            **{
                "channel": 0,
            }
        )

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.roles != after.roles and not await self.bot.cog_disabled_in_guild(
            self, before.guild
        ):
            removal = set(before.roles) - set(after.roles)
            addition = set(after.roles) - set(before.roles)
            for role in addition:
                crole = await self.config.role(role).all()
                if crole["add"]:
                    if crole["method"] == "DM":
                        dest = after
                    elif crole["method"] == "Channel":
                        if crole["channel"] != 0:
                            dest = after.guild.get_channel(crole["channel"])
                        else:
                            dest = after.guild.get_channel(
                                await self.config.guild(after.guild).channel()
                            )
                    else:
                        dest = None

                    await self._sanatize_send(
                        dest,
                        after,
                        role,
                        crole["add_msg"],
                    )
            for role in removal:
                crole = await self.config.role(role).all()
                if crole["remove"]:
                    if crole["method"] == "DM":
                        dest = after
                    elif crole["method"] == "Channel":
                        if crole["channel"] != 0:
                            dest = after.guild.get_channel(crole["channel"])
                        else:
                            dest = after.guild.get_channel(
                                await self.config.guild(after.guild).channel()
                            )
                    else:
                        dest = None

                    await self._sanatize_send(
                        dest,
                        after,
                        role,
                        crole["rem_msg"],
                    )

    async def _sanatize_send(self, dest, user, role, msg):
        """
        {role_name}
        {role_mention}
        {user_name}
        {user_mention}
        """

        await dest.send(
            msg.replace("{role_name}", role.name)
            .replace("{role_mention}", role.mention)
            .replace("{user_name}", user.display_name)
            .replace("{user_mention}", user.mention)
        )

    @commands.guild_only()
    @commands.admin_or_permissions(manage_roles=True)
    @commands.group()
    async def rolenotify(self, ctx):
        """Configure RoleNotify"""

    @rolenotify.command(name="channel")
    async def rolenotify_channel(self, ctx, channel: Union[discord.TextChannel, int] = None):
        """
        Set the channel to output Role Notifications to

        Pass 0 to clear the channel
        Pass nothing to see the configured channel
        """

        if channel is None:
            chan = await self.config.guild(ctx.guild).channel()
            await ctx.send(f"Currently set to {self.bot.get_channel(chan).mention}")
        elif channel == 0:
            await self.config.guild(ctx.guild).channel.set(0)
            if not await ctx.tick():
                await ctx.send("Channel has been cleared")
        else:
            await self.config.guild(ctx.guild).channel.set(channel.id)
            await ctx.send("Channel has been set")

    @rolenotify.group(name="role")
    async def rolenotify_role(self, ctx):
        """Configure settings for a Role"""

    @rolenotify_role.command(name="info")
    async def rolenotify_role_info(self, ctx, role: discord.Role):
        """Display the configured settings for a Role"""

        settings = await self.config.role(role).all()
        await ctx.send(
            """Settings for *{role}*\n----------\n**Method**: {method}\n{channel}**Addition**: {add}\n**Message**: {add_msg}\n**Removal**: {rem}\n**Message**: {rem_msg}""".format(
                role=role.name,
                method=settings["method"],
                channel=""
                if settings["channel"] == 0
                else f"**Channel**: {self.bot.get_channel(settings['channel']).mention}\n",
                add=settings["add"],
                add_msg=settings["add_msg"],
                rem=settings["remove"],
                rem_msg=settings["rem_msg"],
            )
        )

    @rolenotify_role.command(name="method")
    async def rolenotify_role_method(self, ctx, role: discord.Role, method: str):
        """
        Set the notification method

        Valid options are `dm` and `channel`
        """

        if method.lower() == "dm":
            await self.config.role(role).method.set("DM")
        elif method.lower() == "channel":
            await self.config.role(role).method.set("Channel")
        else:
            return await ctx.send("Invalid option, please use either `dm` or `channel`")

        if not await ctx.tick():
            await ctx.send("Notification method has been set")

    @rolenotify_role.command(name="channel")
    async def rolenotify_role_channel(self, ctx, role: discord.Role, channel: discord.TextChannel):
        """
        Set the channel to output Role Notifications to

        Pass 0 to clear the channel and use the server defined channel
        """

        if channel == 0:
            await self.config.role(role).channel.set(0)
            if not await ctx.tick():
                await ctx.send("Channel has been cleared")
        else:
            await self.config.role(role).channel.set(channel.id)
            await ctx.send("Channel has been set")

    @rolenotify_role.command(name="message")
    async def rolenotify_role_msg(self, ctx, role: discord.Role, option: str, *, message: str):
        """
        Set the notification message

        <option> can be either `add` or `remove`

        Formatting options available for <message> are
        {role_name} = Role Name
        {role_mention} = Role Mention (will not ping)
        {user_name} = User's Display Name
        {user_mention} = User Mention

        """

        if option.lower() == "add":
            await self.config.role(role).add_msg.set(message)
        elif option.lower() == "remove":
            await self.config.role(role).rem_msg.set(message)
        else:
            return await ctx.send("Invalid option, please use either `add` or `remove`")

        if not await ctx.tick():
            await ctx.send("Notification Message has been set")

    @rolenotify_role.command(name="add")
    async def rolenotify_role_add(self, ctx, role: discord.Role, state: bool):
        """
        Set if the notification should be sent on Role Add

        <state> should be any of these combinations, `on/off`, `yes/no`, `1/0`, `true/false`
        """

        await self.config.role(role).add.set(state)

        if not await ctx.tick():
            await ctx.send("Add Notificaiton has been set")

    @rolenotify_role.command(name="remove")
    async def rolenotify_role_remove(self, ctx, role: discord.Role, state: bool):
        """
        Set if the notification should be sent on Role Remove

        <state> should be any of these combinations, `on/off`, `yes/no`, `1/0`, `true/false`
        """

        await self.config.role(role).remove.set(state)

        if not await ctx.tick():
            await ctx.send("Remove Notificaiton has been set")

    async def red_get_data_for_user(self, *, user_id: int):
        # this cog does not store any user data
        return {}

    async def red_delete_data_for_user(self, *, requester, user_id: int) -> None:
        # this cog does not store any user data
        pass

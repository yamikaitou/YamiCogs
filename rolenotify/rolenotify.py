from typing import Union

import discord
from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.config import Config


class RoleNotify(commands.Cog):
    """
    Notify a user when they have a Role added or removed from them
    """

    def __init__(self, bot: Red) -> None:
        self.bot = bot
        self.config = Config.get_conf(
            self,
            identifier=582650109,
            force_registration=True,
        )

        self.config.register_role(**{"method": "DM", "add": False, "remove": False})
        self.config.register_guild(**{"channel": 0})

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.roles != after.roles and not await self.bot.cog_disabled_in_guild(
            self, before.guild
        ):
            removal = set(before.roles) - set(after.roles)
            addition = set(after.roles) - set(before.roles)
            for role in addition:
                if await self.config.role(role).add():
                    method = await self.config.role(role).method()
                    if method == "DM":
                        await after.send(
                            "You were granted the Role *{role_name}*".format(
                                role_name=role.name
                            )
                        )
                    elif method == "Channel":
                        await after.guild.get_channel(
                            await self.config.guild(after.guild).channel()
                        ).send(
                            "{member_name} has been granted the Role {role_name}".format(
                                member_name=after.display_name, role_name=role.name
                            )
                        )
            for role in removal:
                if await self.config.role(role).remove():
                    method = await self.config.role(role).method()
                    if method == "DM":
                        await after.send(
                            "You lost the Role *{role_name}*".format(
                                role_name=role.name
                            )
                        )
                    elif method == "Channel":
                        await after.guild.get_channel(
                            await self.config.guild(after.guild).channel()
                        ).send(
                            "{member_name} has lost the Role {role_name}".format(
                                member_name=after.display_name, role_name=role.name
                            )
                        )

    @commands.guild_only()
    @commands.admin_or_permissions(manage_roles=True)
    @commands.group()
    async def rolenotify(self, ctx):
        """Configure RoleNotify"""

    @rolenotify.command(name="channel")
    async def rolenotify_channel(self, ctx, channel: Union[discord.TextChannel, int]):
        """
        Set the channel to output Role Notifications to

        Pass 0 to clear the channel
        """

        if channel == 0:
            await self.config.guild(ctx.guild).channel.set(0)
            await ctx.send("Channel has been cleared")
        else:
            await self.config.guild(ctx.guild).channel.set(channel.id)
            await ctx.send("Channel has been set")

    @rolenotify.group(name="role")
    async def rolenotify_role(self, ctx):
        """Configure settings for a Role"""
        pass

    @rolenotify_role.command(name="info")
    async def rolenotify_role_info(self, ctx, role: discord.Role):
        """Display the configured settings for a Role"""

        settings = await self.config.role(role).all()
        await ctx.send(
            """Settings for *{role}*\n----------\n**Method**: {method}\n**Addition**: {add}\n**Removal**: {rem}""".format(
                role=role.name,
                method=settings["method"],
                add=settings["add"],
                rem=settings["remove"],
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

        await ctx.send("Notification method has been set")

    @rolenotify_role.command(name="add")
    async def rolenotify_role_add(self, ctx, role: discord.Role, state: bool):
        """Set if the notification should be sent on Role Add"""

        await self.config.role(role).add.set(state)
        await ctx.send("Add Notificaiton has been set")

    @rolenotify_role.command(name="remove")
    async def rolenotify_role_remove(self, ctx, role: discord.Role, state: bool):
        """Set if the notification should be sent on Role Remove"""

        await self.config.role(role).remove.set(state)
        await ctx.send("Remove Notificaiton has been set")

    async def red_get_data_for_user(self, *, user_id: int):
        # this cog does not store any user data
        return {}

    async def red_delete_data_for_user(self, *, requester, user_id: int) -> None:
        # this cog does not store any user data
        pass

import discord
from discord.ext import tasks
from redbot.core import Config, checks, commands
from redbot.core.bot import Red
from redbot.core.utils.chat_formatting import box

from tabulate import tabulate

# from menus import gslist


class GameServers(commands.Cog):
    """
    Game Servers
    """

    __version__ = "0.0.0"

    def format_help_for_context(self, ctx):
        """Thanks Sinbad."""
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\nCog Version: {self.__version__}"

    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(
            self, identifier=582650109, force_registration=True
        )

        self.config.register_guild(**{"servers": [], "statuschannel": 0})

    async def red_get_data_for_user(self, *, user_id: int):
        # this cog does not store any data
        return {}

    async def red_delete_data_for_user(self, *, requester, user_id: int) -> None:
        # this cog does not store any data
        pass

    @tasks.loop(minutes=1.0)
    async def poll_servers(self):
        pass

    @poll_servers.before_loop
    async def before_poll_servers(self):
        await self.bot.wait_until_ready()

    @commands.group()
    @commands.guild_only()
    @checks.admin_or_permissions(manage_channels=True)
    async def gameserver(self, ctx: commands.GuildContext):
        """I'll put something here later"""

    @gameserver.command(name="new")
    async def gs_new(
        self, ctx: commands.GuildContext, name: str, ip: str, port: int = 27015
    ):
        """
        Add a new game server.

        <name> = The friendly name to show for the server
        <ip> = Can be the IP or DNS for the server
        <port> = The port for the server. Default is 27015
        """

        server = {
            "name": name,
            "ip": ip,
            "port": port,
            "password": "",
            "down": False,
            "count": 0,
            "enable": False,
            "announce": False,
        }
        async with self.config.guild(ctx.guild).servers() as servers:
            servers.append(server)
            id = servers.index(server)

        await ctx.send(
            "Server has been added, configure the other options with `{}gameserver config {}`".format(
                ctx.clean_prefix, id
            )
        )

    @gameserver.command(name="config")
    async def gs_config(
        self, ctx: commands.GuildContext, serverid: int, key: str, *, value: str
    ):
        """
        Configure the additional settings for game servers

        <serverid> = The ID of the server, check `[p]gameserver list` if you forgot it
        <key> = The config key you want to change (see list below)
        <value> = The value you want to set

        Valid Key Options
        `name` = Change the friendly display name
        `ip` = Change the IP or DNS
        `port` = Change the Port
        `password` = Define the password you have set on your server
        `enable` = Toggle the Status Post (valid options are `yes` and `no`)
        `announce` = Toggle the Down Announcer Post (valid options are `yes` and `no`)
        """

        if key == "name":
            async with self.config.guild(guild).servers() as servers:
                servers[serverid]["name"] = value
            await ctx.tick()
        elif key == "ip":
            async with self.config.guild(guild).servers() as servers:
                servers[serverid]["ip"] = value
            await ctx.tick()
        elif key == "port":
            async with self.config.guild(guild).servers() as servers:
                servers[serverid]["port"] = value
            await ctx.tick()
        elif key == "password":
            async with self.config.guild(guild).servers() as servers:
                servers[serverid]["password"] = value
            await ctx.tick()
        elif key == "enable":
            async with self.config.guild(guild).servers() as servers:
                if value == "yes":
                    servers[serverid]["enable"] = True
                    await ctx.tick()
                elif value == "no":
                    servers[serverid]["enable"] = False
                    await ctx.tick()
        elif key == "announce":
            async with self.config.guild(guild).servers() as servers:
                if value == "yes":
                    servers[serverid]["announce"] = True
                    await ctx.tick()
                elif value == "no":
                    servers[serverid]["announce"] = False
                    await ctx.tick()
        else:
            await ctx.send("Unknown Key")

    @gameserver.command(name="list")
    async def gs_list(self, ctx: commands.GuildContext, serverid: int = None):
        """
        List the settings for each Game Server

        [serverid] = If provided, only that server will be returned. All will be provided in a menu if omitted
        """

        if serverid != None:
            servers = await self.config.guild(ctx.guild).servers()
            try:
                server = []
                for k, v in servers[serverid].items():
                    if k in ["ip", "port", "password"]:
                        server.append([k, v])
                    elif k in ["enable", "announce"]:
                        server.append([k, ("Yes" if v else "No")])
            except KeyError:
                await ctx.send("Unknown Server ID")
            else:
                embed = discord.Embed()
                embed.title = servers[serverid]["name"]
                embed.set_footer(text="Server ID {}".format(serverid))
                embed.description = box(tabulate(server), "properties")
                await ctx.send(embed=embed)
        else:
            await ctx.send("I don't work yet")

import discord
from redbot.core import Config, checks, commands


class MinecraftCasino(commands.Cog):
    """
    Play Casino games with random Minecraft stuff
    """

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=192153481165930496, force_registration=True)

        default_guild = {
            "conversion": 100,
            "poker": {"cost": 45, "min": 4, "stats": 10},
        }

        self.config.register_guild(**default_guild)

    @commands.group()
    @checks.guildowner_or_permissions(manage_guild=True)
    async def mccasino(self, ctx):
        """Configure the Casino"""

    @mccasino.command(name="info")
    async def mcc_info(self, ctx):
        """View configured settings"""

        settings = await self.config.guild(ctx.guild).all()

        embed = discord.Embed(title="Minecraft Casino Settings", color=await ctx.embed_color())
        embed.add_field(
            name="General",
            value=f"Cost per Diamond: {settings['conversion']}",
            inline=False,
        )
        embed.add_field(
            name="Poker",
            value=f"Diamonds to Play: {settings['poker']['cost']}\nMinimun Players: {settings['poker']['min']}\nNumber of Statistics: {settings['poker']['stats']}",
            inline=False,
        )

        await ctx.send(embed=embed)

    @commands.group()
    async def mcpoker(self, ctx):
        """Participate in a betting game using randomly generated Minecraft Statistics"""

    @mcpoker.command(name="start")
    async def mcp_start(self, ctx):
        """Start a game"""

    @mcpoker.command(name="join")
    async def mcp_join(self, ctx):
        """Join a game"""

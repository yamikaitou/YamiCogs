import random

import discord
from redbot.core import Config, bank, commands
from redbot.core.utils.chat_formatting import humanize_number
from redbot.core.utils.menus import DEFAULT_CONTROLS, menu

from . import checks as lc


log = logging.getLogger("red.yamicogs.lottery")


class Lottery(commands.Cog):
    """
    Lottery Games
    """

    lucky3 = ["🃏", "🔬", "💰", "🚀", "🏆", "🍰", "🌹", "🦀", "👑"]

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(
            self, identifier=582650109, force_registration=True
        )
        self.config.register_guild(
            **{
                "match1": {"enable": False, "cost": 100, "max": 30, "prize": 0},
                "match5": {"enable": False, "cost": 100, "max": 60, "prize": 0},
                "lucky3": {
                    "enable": False,
                    "cost": 100,
                    "icons": 3,
                    "prize": 1000,
                },
            }
        )

    @commands.group()
    async def lottery(self, ctx):
        """Lottery Game"""

    @lottery.command(name="games")
    async def l_games(self, ctx):
        """View game explanations"""

        settings = await self.config.guild(ctx.guild).all()
        currency = await bank.get_currency_name(ctx.guild)

        pages = []

        if settings["match1"]["enable"]:
            match1 = discord.Embed(
                title="Lottery Games - Match1", color=await ctx.embed_color()
            )
            match1.description = (
                "Play a daily drawing where if you match the Winning Number, you win!"
            )
            match1.add_field(
                name="Rules",
                inline=False,
                value="Get a number between 1 and {}.\n"
                "If your number matches the Winning Number, you win.\n"
                "Number is drawn daily. Winnings are split between all winners.\n"
                "If there is no winner, the prize pool rolls to the next drawing.".format(
                    settings["match1"]["max"]
                ),
            )
            match1.add_field(
                name="Settings",
                value="Cost per Entry: {1} {0}\nNumber Range: 1 - {2}\nCurrent Prize Pool: {3} {0}".format(
                    currency,
                    humanize_number(settings["match1"]["cost"]),
                    settings["match1"]["max"],
                    humanize_number(settings["match1"]["prize"]),
                ),
            )
            pages.append(match1)

        if settings["match5"]["enable"]:
            match5 = discord.Embed(
                title="Lottery Games - Match5", color=await ctx.embed_color()
            )
            match5.description = (
                "Play a weekly drawing where if you match the Winning Numbers, you win!"
            )
            match5.add_field(name="Rules", value="To be detailed later", inline=False)
            match5.add_field(
                name="Settings",
                value="Cost per Entry: {1} {0}\nNumber Range: 1 - {2}\nCurrent Prize Pool: {3} {0}".format(
                    currency,
                    humanize_number(settings["match5"]["cost"]),
                    settings["match5"]["max"],
                    humanize_number(settings["match5"]["prize"]),
                ),
            )
            pages.append(match5)

        if settings["lucky3"]["enable"]:
            lucky3 = discord.Embed(
                title="Lottery Games - Lucky3", color=await ctx.embed_color()
            )
            lucky3.description = "Draw 3 Symbols and with a prize if they all match!\nTo play, use `{}lottery lucky3`".format(
                ctx.clean_prefix
            )
            lucky3.add_field(
                name="Rules",
                inline=False,
                value="You will get {} random emojis. If you match 3 of them, you win!".format(
                    settings["lucky3"]["icons"]
                ),
            )
            lucky3.add_field(
                name="Settings",
                value="Cost per Entry: {1} {0}\nPrize: {2} {0}\nEmojis: {3}".format(
                    currency,
                    humanize_number(settings["match1"]["cost"]),
                    humanize_number(settings["lucky3"]["prize"]),
                    settings["lucky3"]["icons"],
                ),
            )
            pages.append(lucky3)

        if pages != []:
            await menu(ctx, pages, DEFAULT_CONTROLS)
        else:
            await ctx.send("No games are enabled")

    @lc.lucky3_enabled()
    @lottery.command(name="lucky3")
    async def l_lucky3(self, ctx):
        """Play a game of Lucky 3"""
        if not await self.config.guild(ctx.guild).lucky3.enable():
            return

        cost = await self.config.guild(ctx.guild).lucky3.cost()
        currency = await bank.get_currency_name(ctx.guild)

        if not await bank.can_spend(ctx.author, cost):
            await ctx.send(
                "You do not have enough {} to play, you need at least {}".format(
                    currency, cost
                )
            )
            return

        icons = await self.config.guild(ctx.guild).lucky3.icons() - 1
        prize = await self.config.guild(ctx.guild).lucky3.prize()

        num1 = random.randrange(0, icons)
        num2 = random.randrange(0, icons)
        num3 = random.randrange(0, icons)

        await bank.withdraw_credits(ctx.author, cost)
        await ctx.send(f"{self.lucky3[num1]}{self.lucky3[num2]}{self.lucky3[num3]}")

        if num1 == num2 and num1 == num3:
            await ctx.send(
                "🥳 WINNER!!! 🎉 +{} {}".format(humanize_number(prize), currency)
            )
            await bank.deposit_credits(ctx.author, prize)
        else:
            await ctx.send("Not a winner 😢")

    @commands.group()
    async def lottoset(self, ctx):
        """Lottery Settings"""

    @lottoset.command(name="info")
    async def ls_info(self, ctx):
        """View configured settings"""

        settings = await self.config.guild(ctx.guild).all()

        embed = discord.Embed(title="Lottery Settings", color=await ctx.embed_color())
        embed.add_field(
            name="Match 1 (Not yet implemented)",
            inline=True,
            value="Enabled?: {0}\nCost: {1}\nMax #: {2}".format(
                settings["match1"]["enable"],
                humanize_number(settings["match1"]["cost"]),
                settings["match1"]["max"],
            ),
        )
        embed.add_field(
            name="Match 5 (Not yet implemented)",
            inline=True,
            value="Enabled?: {0}\nCost: {1}\nMax #: {2}".format(
                settings["match5"]["enable"],
                humanize_number(settings["match5"]["cost"]),
                settings["match5"]["max"],
            ),
        )
        embed.add_field(
            name="Lucky 3",
            inline=True,
            value="Enabled?: {0}\nCost: {1}\nIcons: {2}\nPrize: {3}".format(
                settings["lucky3"]["enable"],
                humanize_number(settings["lucky3"]["cost"]),
                settings["lucky3"]["icons"],
                humanize_number(settings["lucky3"]["prize"]),
            ),
        )

        await ctx.send(embed=embed)

    @lottoset.group(name="lucky3")
    async def ls_lucky3(self, ctx):
        """Configure settings for Lucky 3"""

    @ls_lucky3.command(name="enable")
    async def ls3_enable(self, ctx, state: str):
        """
        Enable or Disable the Lucky3 game.

        <state> should be any of these combinations, `on/off`, `yes/no`, `1/0`, `true/false`
        """

        if state in ["on", "yes", "1", "true"]:
            await self.config.guild(ctx.guild).lucky3.enable.set(True)
            await ctx.tick()
        elif state in ["off", "no", "0", "false"]:
            await self.config.guild(ctx.guild).lucky3.enable.set(False)
            await ctx.tick()
        else:
            await ctx.send_help()

    @ls_lucky3.command(name="icons")
    async def ls3_icons(self, ctx, icons: int):
        """
        Sets the number of Emojis to choose from

        Valid options are 2-9
        Approximate Win percentrages are
        ```
        Icons: 2 | 25.0%
        Icons: 3 | 11.1%
        Icons: 4 |  6.3%
        Icons: 5 |  4.0%
        Icons: 6 |  2.8%
        Icons: 7 |  2.1%
        Icons: 8 |  1.6%
        Icons: 9 |  1.2%```
        """

        if 2 <= icons <= 9:
            await self.config.guild(ctx.guild).lucky3.icons.set(icons)
            await ctx.tick()
        else:
            await ctx.send(
                "Sorry, but **2** is the lowest and **9** is the highest settings supported"
            )

    @ls_lucky3.command(name="cost")
    async def ls3_cost(self, ctx, cost: int):
        """Set the cost per game"""

        await self.config.guild(ctx.guild).lucky3.cost.set(cost)
        await ctx.tick()

    @ls_lucky3.command(name="prize")
    async def ls3_prize(self, ctx, prize: int):
        """Set the Prize amount"""

        await self.config.guild(ctx.guild).lucky3.prize.set(prize)
        await ctx.tick()

    async def red_get_data_for_user(self, *, user_id: int):
        # this cog does not store any data
        return {}

    async def red_delete_data_for_user(self, *, requester, user_id: int) -> None:
        # this cog does not store any data
        pass

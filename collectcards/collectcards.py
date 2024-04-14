import random
import unicodedata
from typing import Literal

import discord
from databases import Database
from discord import app_commands
from redbot.core import commands, data_manager
from redbot.core.bot import Red
from redbot.core.config import Config

from .drawpackview import DrawPackView
from .enums import Card, Rarity, Set

RequestType = Literal["discord_deleted_user", "owner", "user", "user_strict"]


class CollectCards(commands.Cog):
    """
    A 'card' (emoji) collecting game
    """

    def __init__(self, bot: Red) -> None:
        self.bot = bot
        self.config = Config.get_conf(
            self,
            identifier=582650109,
            force_registration=True,
        )
        self.config.register_global(**{"schema": 0})

        self.database = None
        self.sets = {}
        self.cards = {}
        self.rarity = {1: [], 2: [], 3: []}

        bot.add_dev_env_value("database", lambda ctx: self.database)

    async def cog_unload(self):
        self.bot.remove_dev_env_value("database")

    async def cog_load(self):
        self.database = Database(f"sqlite+aiosqlite:///{data_manager.cog_data_path(self)}/data.db")
        await self.database.connect()

        schema = await self.config.schema()

        if schema == 0:
            with open(
                data_manager.bundled_data_path(self) / "schema_0.sql", "rt", encoding="UTF-8"
            ) as f:
                queries = f.readlines()
            await self.database.execute(query="PRAGMA journal_mode = 'WAL';")
            async with self.database.transaction():
                for query in queries:
                    await self.database.execute(query=query)

            await self.config.schema.set(1)

        setquery = "SELECT * FROM sets"
        cardquery = "SELECT * FROM cards WHERE setkey = :set"
        setrows = await self.database.fetch_all(query=setquery)
        for setrow in setrows:
            tset = Set(key=setrow.key, name=setrow.name, cards=[])
            cardrows = await self.database.fetch_all(query=cardquery, values={"set": setrow[0]})
            for cardrow in cardrows:
                tcard = Card(
                    key=cardrow.key,
                    name=cardrow.name,
                    rarity=cardrow.rarity,
                    emoji=cardrow.emoji,
                    setkey=cardrow.setkey,
                )
                tset.cards.append(tcard)
                self.cards[tcard.key] = tcard
                self.rarity[tcard.rarity].append(tcard)
            self.sets[tset.key] = tset

    @commands.hybrid_group(name="cards", aliases=["collectcards"])
    @app_commands.guild_only()
    @commands.guild_only()
    async def _collectcards(self, ctx):
        """
        About the game
        """

    @_collectcards.command(name="search")
    async def _collectcards_search(self, ctx):
        """
        Open a pack of cards
        """

        embed = discord.Embed()
        embed.description = (
            "You search around the stockroom and find a bag, what do you want to do?"
        )
        url = f"https://cdn.yamikaitou.app/YamiCogs/CollectCards/pack{random.randrange(1,8)}.png"
        embed.set_image(url=url)
        view = DrawPackView(self)
        msg = await ctx.send(embed=embed, view=view, ephemeral=True)

        await view.wait()
        if view.value is None:
            view.stop()
            await msg.edit(
                content="You wasted enough time pondering and left the bag where you found it and walked away",
                embed=None,
                view=None,
            )

    @_collectcards.command(name="bag")
    async def _collectcards_bag(self, ctx):
        """
        See the cards in your bag
        """

        embed = discord.Embed(title="Your Bag")
        hands = await self.database.fetch_all(
            query="SELECT * FROM hands WHERE userid = :user AND guildid = :guild",
            values={"user": ctx.author.id, "guild": ctx.guild.id},
        )
        for hand in hands:
            cards = eval(hand.cards)

            display = ""
            for card in cards.items():
                display = f"{display}\n{self.cards[card[0]].emoji} = {card[1]}"

            embed.add_field(name=self.sets[hand.setkey].name, value=display)

        await ctx.send(embed=embed, ephemeral=True)

    @_collectcards.command(name="sync", with_app_command=False)
    @commands.is_owner()
    async def _collectcards_sync(self, ctx, global_sync: bool = False):
        """
        Sync commands
        """

        if global_sync:
            await self.bot.tree.sync()
            await ctx.tick()
        else:
            self.bot.tree.copy_global_to(guild=ctx.guild)
            await self.bot.tree.sync(guild=ctx.guild)
            await ctx.tick()

    async def red_delete_data_for_user(self, *, requester: RequestType, user_id: int) -> None:
        pass

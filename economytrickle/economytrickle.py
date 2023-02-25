import logging
import math
from typing import Union

import discord
from discord.ext import tasks
from redbot.core import Config, bank, commands
from redbot.core.bot import Red
from tabulate import tabulate  # pylint:disable=import-error

log = logging.getLogger("red.yamicogs.economytrickle")


# taken from Red-Discordbot bank.py
def is_owner_if_bank_global():
    """
    Command decorator. If the bank is global, it checks if the author is
    bot owner, otherwise it only checks
    if command was used in guild - it DOES NOT check any permissions.
    When used on the command, this should be combined
    with permissions check like `guildowner_or_permissions()`.
    """

    async def pred(ctx: commands.Context):
        author = ctx.author
        if not await bank.is_global():
            if not ctx.guild:
                return False
            return True
        else:
            return await ctx.bot.is_owner(author)

    return commands.check(pred)


class EconomyTrickle(commands.Cog):
    """
    Trickle credits into your Economy

    More detailed docs: <https://cogs.yamikaitou.dev/economytrickle.html>
    """

    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=582650109, force_registration=True)

        default_config = {"credits": 0, "messages": 0, "voice": 0, "blocklist": []}

        self.config.register_global(**default_config)
        self.config.register_guild(**default_config)

        self.message = {}
        self.voice = {}

    async def cog_load(self):
        self.bank = await bank.is_global()
        self.blocklist = await self.config.blocklist()

        self.trickle.start()  # pylint:disable=no-member

    async def cog_unload(self):
        self.trickle.cancel()  # pylint:disable=no-member

    @commands.Cog.listener()
    async def on_message_without_command(self, message):
        if message.author.bot:
            return
        if message.guild == None:
            return
        if await self.bot.cog_disabled_in_guild(self, message.guild):
            return
        if message.channel.id in self.blocklist:
            log.debug(
                f"Found message from {message.author.id} in a blocked channel {message.guild.id}-{message.channel.id}"
            )
            return

        if await bank.is_global():
            try:
                log.debug(f"Found message from {message.author.id}")
                self.message[message.author.id].append(message.id)
            except KeyError:
                self.message[message.author.id] = [message.id]
        else:
            try:
                log.debug(f"Found message from {message.author.id} in {message.guild.id}")
                self.message[message.guild.id]
                try:
                    self.message[message.guild.id][message.author.id].append(message.id)
                except KeyError:
                    self.message[message.guild.id][message.author.id] = [message.id]
            except KeyError:
                self.message[message.guild.id] = {message.author.id: [message.id]}

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.bot:
            return
        if await self.bot.cog_disabled_in_guild(self, member.guild):
            return

        if before.channel is None and after.channel is not None:
            if after.channel.id in self.blocklist:
                log.debug(
                    f"Found voice state join from {member.id} in a blocked channel {member.guild.id}-{after.channel.id}"
                )
                return

            if await bank.is_global():
                log.debug(f"Found voice join from {member.id}")
                self.voice[member.id] = 1
            else:
                try:
                    log.debug(f"Found voice join from {member.id} in {member.guild.id}")
                    self.voice[member.guild.id][member.id] = 1
                except KeyError:
                    self.voice[member.guild.id] = {member.id: 1}

        elif after.channel is None and before.channel is not None:
            if before.channel.id in self.blocklist:
                log.debug(
                    f"Found voice state leave from {member.id} in a blocked channel {member.guild.id}-{after.channel.id}"
                )
                return

            if await bank.is_global():
                log.debug(f"Found voice leave from {member.id}")
                self.voice[member.id] = 0
            else:
                try:
                    log.debug(f"Found voice leave from {member.id} in {member.guild.id}")
                    self.voice[member.guild.id][member.id] = 0
                except KeyError:
                    self.voice[member.guild.id] = {member.id: 0}

        elif before.channel is not after.channel:
            if after.channel.id in self.blocklist:
                log.debug(
                    f"Found voice state change from {member.id} in a blocked channel {member.guild.id}-{after.channel.id}"
                )
                if await bank.is_global():
                    self.voice[member.id] = 0
                else:
                    try:
                        self.voice[member.guild.id][member.id] = 0
                    except KeyError:
                        self.voice[member.guild.id] = {member.id: 0}
                return
            elif before.channel.id in self.blocklist:
                if await bank.is_global():
                    log.debug(f"Found voice change from {member.id}")
                    self.voice[member.id] = 1
                else:
                    try:
                        log.debug(f"Found voice change from {member.id} in {member.guild.id}")
                        self.voice[member.guild.id][member.id] = 1
                    except KeyError:
                        self.voice[member.guild.id] = {member.id: 1}

    @tasks.loop(minutes=1)
    async def trickle(self):
        if self.bank is not await bank.is_global():
            if await bank.is_global():
                self.cache = await self.config.all()
            else:
                self.cache = await self.config.all_guilds()
            self.bank = await bank.is_global()

        if await bank.is_global():
            msgs = self.message
            cache = await self.config.all()

            if cache["messages"] != 0 and cache["credits"] != 0:
                for user, msg in msgs.items():
                    if len(msg) >= cache["messages"]:
                        num = math.floor(len(msg) / cache["messages"])
                        log.debug(f"Processing {num} messages for {user}")
                        del (self.message[user])[0 : (num * cache["messages"])]
                        await bank.deposit_credits(
                            (await self.bot.get_or_fetch_user(user)),
                            num * cache["credits"],
                        )

            voice = self.voice
            if cache["voice"] != 0:
                for user, yes in voice.items():
                    if yes:
                        log.debug(f"Processing voice for {user}")
                        await bank.deposit_credits(
                            (await self.bot.get_or_fetch_user(user)),
                            cache["voice"],
                        )

        else:
            msgs = self.message
            for guild, users in msgs.items():
                if not await self.bot.cog_disabled_in_guild(self, self.bot.get_guild(guild)):
                    cache = await self.config.guild_from_id(guild).all()

                    if cache["messages"] != 0 and cache["credits"] != 0:
                        for user, msg in users.items():
                            if len(msg) >= cache["messages"]:
                                num = math.floor(len(msg) / cache["messages"])
                                log.debug(f"Processing {num} messages for {user} in {guild}")
                                del (self.message[guild][user])[0 : (num * cache["messages"])]
                                await bank.deposit_credits(
                                    (
                                        await self.bot.get_or_fetch_member(
                                            self.bot.get_guild(guild), user
                                        )
                                    ),
                                    num * cache["credits"],
                                )

            voice = self.voice
            for guild, users in voice.items():
                if not await self.bot.cog_disabled_in_guild(self, self.bot.get_guild(guild)):
                    cache = await self.config.guild_from_id(guild).all()
                    if cache["voice"] != 0:
                        for user, yes in users.items():
                            if yes:
                                log.debug(f"Processing voice for {user} in {guild}")
                                await bank.deposit_credits(
                                    (
                                        await self.bot.get_or_fetch_member(
                                            self.bot.get_guild(guild), user
                                        )
                                    ),
                                    cache["voice"],
                                )

    @trickle.before_loop
    async def before_trickle(self):
        await self.bot.wait_until_red_ready()

    @is_owner_if_bank_global()
    @commands.admin_or_permissions(manage_guild=True)
    @commands.group(aliases=["trickleset"])
    async def economytrickle(self, ctx):
        """Configure various settings"""

    @is_owner_if_bank_global()
    @commands.admin_or_permissions(manage_guild=True)
    @economytrickle.command(name="settings", aliases=["info", "showsettings"])
    async def ts_settings(self, ctx):
        """Show the current settings"""

        if await bank.is_global():
            cache = await self.config.all()
            await ctx.send(
                f"Message Credits: {cache['credits']}\nMessage Count: {cache['messages']}\nVoice Credits: {cache['voice']}"
            )
        else:
            if ctx.guild is not None:
                cache = await self.config.guild(ctx.guild).all()
                await ctx.send(
                    f"Message Credits: {cache['credits']}\nMessage Count: {cache['messages']}\nVoice Credits: {cache['voice']}"
                )
            else:
                await ctx.send(
                    "Your bank is set to per-server. Please try this command in a server instead"
                )

    @is_owner_if_bank_global()
    @commands.admin_or_permissions(manage_guild=True)
    @economytrickle.command(name="credits")
    async def ts_credits(self, ctx, number: int):
        """
        Set the number of credits to grant

        Set the number to 0 to disable
        Max value is 1000
        """

        if await bank.is_global():
            if 0 <= number <= 1000:
                await self.config.credits.set(number)
                if not await ctx.tick():
                    await ctx.send("Setting saved")
            else:
                await ctx.send(
                    f"You must specify a value that is not less than 0 and not more than 1000"
                )
        else:
            if ctx.guild is not None:
                if 0 <= number <= 1000:
                    await self.config.guild(ctx.guild).credits.set(number)
                    if not await ctx.tick():
                        await ctx.send("Setting saved")
                else:
                    await ctx.send(
                        f"You must specify a value that is not less than 0 and not more than 1000"
                    )
            else:
                await ctx.send(
                    "Your bank is set to per-server. Please try this command in a server instead"
                )

    @is_owner_if_bank_global()
    @commands.admin_or_permissions(manage_guild=True)
    @economytrickle.command(name="messages")
    async def ts_messages(self, ctx, number: int):
        """
        Set the number of messages required to gain credits

        Set the number to 0 to disable
        Max value is 100
        """

        if await bank.is_global():
            if 0 <= number <= 100:
                await self.config.messages.set(number)
                if not await ctx.tick():
                    await ctx.send("Setting saved")
            else:
                await ctx.send(
                    f"You must specify a value that is not less than 0 and not more than 100"
                )
        else:
            if ctx.guild is not None:
                if 0 <= number <= 100:
                    await self.config.guild(ctx.guild).messages.set(number)
                    if not await ctx.tick():
                        await ctx.send("Setting saved")
                else:
                    await ctx.send(
                        f"You must specify a value that is not less than 0 and not more than 100"
                    )
            else:
                await ctx.send(
                    "Your bank is set to per-server. Please try this command in a server instead"
                )

    @is_owner_if_bank_global()
    @commands.admin_or_permissions(manage_guild=True)
    @economytrickle.command(name="voice")
    async def ts_voice(self, ctx, number: int):
        """
        Set the number of credits to grant every minute

        Set the number to 0 to disable
        Max value is 1000
        """

        if await bank.is_global():
            if 0 <= number <= 1000:
                await self.config.voice.set(number)
                if not await ctx.tick():
                    await ctx.send("Setting saved")
            else:
                await ctx.send(
                    f"You must specify a value that is not less than 0 and not more than 1000"
                )
        else:
            if ctx.guild is not None:
                if 0 <= number <= 1000:
                    await self.config.guild(ctx.guild).voice.set(number)
                    if not await ctx.tick():
                        await ctx.send("Setting saved")
                else:
                    await ctx.send(
                        f"You must specify a value that is not less than 0 and not more than 1000"
                    )
            else:
                await ctx.send(
                    "Your bank is set to per-server. Please try this command in a server instead"
                )

    @commands.guild_only()
    @commands.admin_or_permissions(manage_guild=True)
    @economytrickle.command(name="blocklist", aliases=["blacklist"])
    async def ts_blocklist(
        self, ctx, channel: Union[discord.TextChannel, discord.VoiceChannel] = None
    ):
        """
        Add/Remove the current channel (or a specific channel) to the blocklist

        Not passing a channel will add/remove the channel you ran the command in to the blocklist
        """

        if channel is None:
            channel = ctx.channel

        try:
            self.blocklist.remove(channel.id)
            await ctx.send("Channel removed from the blocklist")
        except ValueError:
            self.blocklist.append(channel.id)
            await ctx.send("Channel added to the blocklist")
        finally:
            await self.config.blocklist.set(self.blocklist)

    @commands.guild_only()
    @commands.admin_or_permissions(manage_guild=True)
    @economytrickle.command(name="showblocks", aliases=["showblock"])
    async def ts_showblocks(self, ctx):
        """Provide a list of channels that are on the blocklist for this server"""

        blocks = ""
        for block in self.blocklist:
            chan = self.bot.get_channel(block)
            if chan.guild is ctx.guild:
                blocks += f"{chan.name}\n"

        if blocks == "":
            blocks = "No channels blocked"

        await ctx.send(f"The following channels are blocked from EconomyTrickle\n{blocks}")

    async def red_get_data_for_user(self, *, user_id: int):
        # this cog does not store any data
        return {}

    async def red_delete_data_for_user(self, *, requester, user_id: int) -> None:
        # this cog does not store any data
        pass

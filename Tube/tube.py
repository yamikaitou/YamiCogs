# -*- coding: utf-8 -*-
import datetime
import hashlib
import logging
import re
import time
from typing import Optional

import aiohttp
import discord
import feedparser
from discord.ext import tasks
from redbot.core import Config, bot, checks, commands
from redbot.core.data_manager import cog_data_path
from redbot.core.utils.chat_formatting import pagify
from redbot.logging import RotatingFileHandler

log = logging.getLogger("red.cbd-cogs.tube")
debugger = logging.getLogger("red.yamicogs.tube.debugger")

__all__ = ["UNIQUE_ID", "Tube"]

UNIQUE_ID = 0x547562756C6172

TIME_DEFAULT = "1970-01-01T00:00:00+00:00"
# Time tuple for use with time.mktime()
TIME_TUPLE = (*(int(x) for x in re.split(r"-|T|:|\+", TIME_DEFAULT)), 0)

# Word tokenizer
TOKENIZER = re.compile(r"([^\s]+)")


class Tube(commands.Cog):
    """A YouTube subscription cog

    Thanks to mikeshardmind(Sinbad) for the RSS cog as reference"""

    has_warned_about_invalid_channels = False

    def __init__(self, bot: bot.Red):
        self.bot = bot
        self.conf = Config.get_conf(self, identifier=UNIQUE_ID, force_registration=True)
        self.conf.register_guild(subscriptions=[], cache=[])
        self.conf.register_global(interval=300, cache_size=500, debugger=False)
        self.background_get_new_videos.start()

        # Thanks Laggron and AAA3A
        formatter = logging.Formatter(
            "[{asctime}] {message}", datefmt="%Y-%m-%d %H:%M:%S", style="{"
        )
        file_handler = RotatingFileHandler(
            stem="tube",
            directory=cog_data_path(self),
            maxBytes=10_000_000,
            backupCount=8,
            encoding="utf-8",
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        debugger.addHandler(file_handler)
        self.debug = False

    @commands.group()
    async def tube(self, ctx: commands.Context):
        """Post when new videos are added to a YouTube channel"""

    @checks.admin_or_permissions(manage_guild=True)
    @commands.guild_only()
    @tube.command()
    async def subscribe(
        self,
        ctx: commands.Context,
        channelYouTube,
        channelDiscord: Optional[discord.TextChannel] = None,
        publish: Optional[bool] = False,
    ):
        """Subscribe a Discord channel to a YouTube channel

        If no discord channel is specified, the current channel will be subscribed

        Adding channels by name is not supported at this time. The YouTube channel ID for this can be found in channel links on videos.

        For example, to subscribe to the channel Ctrl Shift Face, you would search YouTube for the name, then on one of the videos in the results copy the channel link. It should look like this:
        https://www.youtube.com/channel/UCKpH0CKltc73e4wh0_pgL3g

        Now take the last part of the link as the channel ID:
        `[p]tube subscribe UCKpH0CKltc73e4wh0_pgL3g`

        Setting the `publish` flag will cause new videos to be published to the specified channel. Using this on non-announcement channels may result in errors.
        """
        if not channelDiscord:
            channelDiscord = ctx.channel
        subs = await self.conf.guild(ctx.guild).subscriptions()
        newSub = {
            "id": channelYouTube,
            "channel": {"name": channelDiscord.name, "id": channelDiscord.id},
            "publish": publish,
        }
        newSub["uid"] = self.sub_uid(newSub)
        for sub in subs:
            if sub["uid"] == newSub["uid"]:
                await ctx.send("This subscription already exists!")
                return
        feed = feedparser.parse(await self.get_feed(newSub["id"]))
        last_video = {}
        for entry in feed["entries"]:
            if not last_video or datetime.datetime.fromisoformat(
                entry["published"]
            ) > datetime.datetime.fromisoformat(last_video["published"]):
                last_video = entry
        if last_video and last_video.get("published"):
            newSub["previous"] = last_video["published"]
        try:
            newSub["name"] = feed["feed"]["title"]
        except KeyError:
            await ctx.send(f"Error getting channel feed title. Make sure the ID is correct.")
            return
        subs.append(newSub)
        await self.conf.guild(ctx.guild).subscriptions.set(subs)
        await ctx.send(f"Subscription added: {newSub}")
        self.debug_info(f"Subscription added: {newSub}")

    @checks.admin_or_permissions(manage_guild=True)
    @commands.guild_only()
    @tube.command()
    async def unsubscribe(
        self,
        ctx: commands.Context,
        channelYouTube,
        channelDiscord: Optional[discord.TextChannel] = None,
    ):
        """Unsubscribe a Discord channel from a YouTube channel

        If no Discord channel is specified and the asAnnouncement flag not set to True, the subscription will be removed from all channels
        """
        subs = await self.conf.guild(ctx.guild).subscriptions()
        unsubbed = []
        if channelDiscord:
            newSub = {"id": channelYouTube, "channel": {"id": channelDiscord.id}}
            unsubTarget, unsubType = self.sub_uid(newSub), "uid"
        else:
            unsubTarget, unsubType = channelYouTube, "id"
        for i, sub in enumerate(subs):
            if sub[unsubType] == unsubTarget:
                unsubbed.append(subs.pop(i))
        if not len(unsubbed):
            await ctx.send("Subscription not found")
            return
        await self.conf.guild(ctx.guild).subscriptions.set(subs)
        await ctx.send(f"Subscription(s) removed: {unsubbed}")
        self.debug_info(f"Subscription(s) removed: {unsubbed}")

    @checks.admin_or_permissions(manage_guild=True)
    @commands.guild_only()
    @tube.command()
    async def customize(self, ctx: commands.Context, channelYouTube, customMessage: str = False):
        """Add a custom message to videos from a YouTube channel

        You can use any keys available in the RSS object in your custom message
        by surrounding the key in perecent signs, e.g.:
        [p]tube customize UCKpH0CKltc73e4wh0_pgL3g "It's ya boi %author% wish a fresh vid: %title%\\nWatch, like, subscribe, give monies, etc.

        You can also remove customization by not specifying any message.
        """
        subs = await self.conf.guild(ctx.guild).subscriptions()
        found = False
        for i, sub in enumerate(subs):
            if sub["id"] == channelYouTube:
                found = True
                subs[i]["custom"] = customMessage
        if not found:
            await ctx.send("Subscription not found")
            return
        await self.conf.guild(ctx.guild).subscriptions.set(subs)
        await ctx.send(f"Custom message {'added' if customMessage else 'removed'}")

    @checks.admin_or_permissions(manage_guild=True)
    @commands.guild_only()
    @tube.command()
    async def rolemention(
        self, ctx: commands.Context, channelYouTube, rolemention: Optional[discord.Role]
    ):
        """Adds a role mention in front of the message"""
        subs = await self.conf.guild(ctx.guild).subscriptions()
        found = False
        for i, sub in enumerate(subs):
            if sub["id"] == channelYouTube:
                found = True
                subs[i]["mention"] = rolemention.id if rolemention is not None else rolemention
        if not found:
            await ctx.send("Subscription not found")
            return
        await self.conf.guild(ctx.guild).subscriptions.set(subs)
        await ctx.send(f'Role mention {"added" if rolemention else "removed" }')

    @commands.guild_only()
    @tube.command(name="list")
    async def showsubs(self, ctx: commands.Context):
        """List current subscriptions"""
        await self._showsubs(ctx, ctx.guild)

    async def _showsubs(self, ctx: commands.Context, guild: discord.Guild):
        subs = await self.conf.guild(guild).subscriptions()
        if not len(subs):
            await ctx.send("No subscriptions yet - try adding some!")
            return
        subs_by_channel = {}
        for sub in subs:
            # Channel entry must be max 124 chars: 103 + 2 + 18 + 1
            channel = f'{sub["channel"]["name"][:103]} ({sub["channel"]["id"]})'  # Max 124 chars
            subs_by_channel[channel] = [
                # Sub entry must be max 100 chars: 45 + 2 + 24 + 4 + 25 = 100
                f"{sub.get('name', sub['id'][:45])} ({sub['id']}) - {sub.get('previous', 'Never')}",
                # Preserve previous entries
                *subs_by_channel.get(channel, []),
            ]
        if ctx.channel.permissions_for(guild.me).embed_links:
            for channel, sub_ids in subs_by_channel.items():
                page_count = (len(sub_ids) // 9) + 1
                page = 1
                while len(sub_ids) > 0:
                    # Generate embed with max 1024 chars
                    embed = discord.Embed()
                    title = f"Tube Subs for {channel}"
                    embed.description = "\n".join(sub_ids[0:9])
                    if page_count > 1:
                        title += f" ({page}/{page_count})"
                        page += 1
                    embed.title = title
                    await ctx.send(embed=embed)
                    del sub_ids[0:9]
        else:
            subs_string = ""
            for channel, sub_ids in subs_by_channel.items():
                subs_string += f"\n\n{channel}"
                for sub in sub_ids:
                    subs_string += f"\n{sub}"
            pages = pagify(subs_string, delims=["\n\n"], shorten_by=12)
            for i, page in enumerate(pages):
                title = "**Tube Subs**"
                if len(pages) > 1:
                    title += f" ({i}/{len(pages)})"
                await ctx.send(f"{title}\n{page}")

    @checks.is_owner()
    @tube.command(name="ownerlist", hidden=True)
    async def owner_list(self, ctx: commands.Context):
        """List current subscriptions for all guilds"""
        for guild in self.bot.guilds:
            await self._showsubs(ctx, guild)

    def sub_uid(self, subscription: dict):
        """A subscription must have a unique combination of YouTube channel ID and Discord channel"""
        try:
            canonicalString = f'{subscription["id"]}:{subscription["channel"]["id"]}'
        except KeyError:
            raise ValueError("Subscription object is malformed")
        return hashlib.sha256(canonicalString.encode()).hexdigest()

    @checks.admin_or_permissions(manage_guild=True)
    @commands.guild_only()
    @tube.command(name="update")
    async def get_new_videos(self, ctx: commands.Context):
        """Update feeds and post new videos"""
        await ctx.send(f"Updating subscriptions for {ctx.message.guild}")
        await self._get_new_videos(ctx.message.guild, ctx=ctx)

    @checks.admin_or_permissions(manage_guild=True)
    @commands.guild_only()
    @tube.command()
    async def demo(self, ctx: commands.Context):
        """Post the latest video from all subscriptions"""
        await self._get_new_videos(ctx.message.guild, ctx=ctx, demo=True)

    @checks.is_owner()
    @tube.command(name="ownerupdate", hidden=True)
    async def owner_get_new_videos(self, ctx: commands.Context):
        """Update feeds and post new videos for all guilds"""
        fetched = {}
        for guild in self.bot.guilds:
            await ctx.send(f"Updating subscriptions for {guild}")
            update = await self._get_new_videos(guild, fetched, ctx)
            if not update:
                continue
            fetched.update(update)

    async def _get_new_videos(
        self,
        guild: discord.Guild,
        cache: dict = {},
        ctx: commands.Context = None,
        demo: bool = False,
    ):
        try:
            subs = await self.conf.guild(guild).subscriptions()
            history = await self.conf.guild(guild).cache()
        except:
            return
        new_history = []
        altered = False
        for i, sub in enumerate(subs):
            publish = sub.get("publish", False)
            channel_id = sub["channel"]["id"]
            channel = self.bot.get_channel(int(channel_id))
            self.debug_info(
                f"Processing {sub['name']} ({sub['id']}) for {sub['channel']['name']} ({sub['channel']['id']})"
            )
            if not channel:
                if not self.has_warned_about_invalid_channels:
                    self.log_warn(f"Invalid channel in subscription: {channel_id}")
                continue
            if not channel.permissions_for(guild.me).send_messages:
                self.log_warn(f"Not allowed to post subscription to: {channel_id}")
                continue
            if not sub["id"] in cache.keys():
                try:
                    cache[sub["id"]] = feedparser.parse(await self.get_feed(sub["id"]))
                except Exception as e:
                    self.log_exception(
                        f"Error parsing feed for {sub.get('name', '')} ({sub['id']})"
                    )
                    continue
            last_video_time = datetime.datetime.fromisoformat(
                sub.get("previous", "1970-01-01T00:00:00+00:00")
            )
            self.debug_debug("Last Video: " + last_video_time.strftime("%Y-%m-%d %H:%M:%S"))
            for entry in cache[sub["id"]]["entries"][::-1]:
                published = datetime.datetime.fromisoformat(entry.get("published"))
                if not sub.get("name"):
                    altered = True
                    sub["name"] = entry["author"]
                if (published > last_video_time and not entry["yt_videoid"] in history) or (
                    demo and published > last_video_time - datetime.timedelta(seconds=1)
                ):
                    logmsg = f"Eligible Video Found {entry['yt_videoid']}"
                    logmsg = logmsg + "\npublished: " + entry.get("published")
                    logmsg = (
                        logmsg + "\npublished_parsed: " + published.strftime("%Y-%m-%d %H:%M:%S")
                    )
                    logmsg = logmsg + "\nupdated: " + entry.get("published")
                    logmsg = (
                        logmsg
                        + "\nupdated_parsed: "
                        + datetime.datetime.fromtimestamp(
                            time.mktime(entry.get("updated_parsed", TIME_TUPLE))
                        ).strftime("%Y-%m-%d %H:%M:%S")
                    )
                    logmsg = logmsg + "\nConfig previous:" + subs[i].get("previous", "None")
                    altered = True
                    subs[i]["previous"] = entry["published"]
                    new_history.append(entry["yt_videoid"])
                    # Build custom description if one is set
                    custom = sub.get("custom", False)
                    if custom:
                        for token in TOKENIZER.split(custom):
                            if token.startswith("%") and token.endswith("%"):
                                custom = custom.replace(token, entry.get(token[1:-1]))
                        description = f"{custom}\n{entry['link']}"
                    # Default descriptions
                    else:
                        if channel.permissions_for(guild.me).embed_links:
                            # Let the embed provide necessary info
                            description = entry["link"]
                        else:
                            description = (
                                f"New video from *{entry['author'][:500]}*:"
                                f"\n**{entry['title'][:500]}**\n{entry['link']}"
                            )

                    mention_id = sub.get("mention", False)
                    if mention_id:
                        if mention_id == guild.id:
                            description = f"{guild.default_role} {description}"
                            mentions = discord.AllowedMentions(everyone=True)
                        else:
                            description = f"<@&{mention_id}> {description}"
                            mentions = discord.AllowedMentions(roles=True)
                    else:
                        mentions = discord.AllowedMentions()

                    self.debug_debug(logmsg)
                    message = await channel.send(content=description, allowed_mentions=mentions)
                    if publish:
                        await message.publish()
        if altered:
            await self.conf.guild(guild).subscriptions.set(subs)
            await self.conf.guild(guild).cache.set(list(set([*history, *new_history])))
        self.has_warned_about_invalid_channels = True
        return cache

    @checks.is_owner()
    @tube.command(name="setinterval", hidden=True)
    async def set_interval(self, ctx: commands.Context, interval: int):
        """Set the interval in seconds at which to check for updates

        Very low values will probably get you rate limited

        Default is 300 seconds (5 minutes)"""
        await self.conf.interval.set(interval)
        self.background_get_new_videos.change_interval(seconds=interval)
        await ctx.send(f"Interval set to {await self.conf.interval()}")

    @checks.is_owner()
    @tube.command(name="setcache", hidden=True)
    async def set_cache(self, ctx: commands.Context, size: int):
        """Set the number of video IDs to cache

        Very low values may result in reposting of videos

        Default is 500"""
        await self.conf.cache_size.set(size)
        await ctx.send(f"Cache size set to {await self.conf.cache_size()}")

    async def fetch(self, session, url):
        try:
            async with session.get(url) as response:
                return await response.read()
        except aiohttp.client_exceptions.ClientConnectionError as e:
            await self.log_exception(f"Fetch failed for url {url}: ", exc_info=e)
            return None

    async def get_feed(self, channel):
        """Fetch data from a feed"""
        async with aiohttp.ClientSession() as session:
            res = await self.fetch(
                session, f"https://www.youtube.com/feeds/videos.xml?channel_id={channel}"
            )
        return res

    async def cog_unload(self):
        self.background_get_new_videos.cancel()

    @tasks.loop(seconds=1)
    async def background_get_new_videos(self):
        fetched = {}
        cache_size = await self.conf.cache_size()
        self.debug_info("Fetching new videos")
        for guild in self.bot.guilds:
            update = await self._get_new_videos(guild, fetched)
            if not update:
                continue
            fetched.update(update)
            # Truncate video ID cache
            cache = await self.conf.guild(guild).cache()
            await self.conf.guild(guild).cache.set(cache[-cache_size:])

    @background_get_new_videos.before_loop
    async def wait_for_red(self):
        await self.bot.wait_until_red_ready()
        interval = await self.conf.interval()
        self.background_get_new_videos.change_interval(seconds=interval)

    @tube.command(name="debugger", hidden=True)
    @commands.is_owner()
    async def _tube_debugger(self, ctx, value: bool = None):
        """Enable the feed debugger"""
        current = await self.conf.debugger()
        if value is None:
            await ctx.send(f"Current Setting: {current}\nLogging to {(cog_data_path(self))}")
        else:
            await self.conf.debugger.set(value)
            await ctx.send(f"Debugger has been {'enabled' if value else 'disabled'}")
            self.debug = value
            if value:
                self.debug = True
            else:
                self.debug = False

    async def cog_load(self):
        if await self.conf.debugger():
            self.debug = True

    def log_info(self, msg, **kwargs):
        log.info(msg, **kwargs)
        if self.debug:
            debugger.propagate = False
            debugger.info(msg)
            debugger.propagate = True

    def log_warn(self, msg, **kwargs):
        log.warning(msg, **kwargs)
        if self.debug:
            debugger.propagate = False
            debugger.warning(msg)
            debugger.propagate = True

    def log_debug(self, msg, **kwargs):
        log.debug(msg, **kwargs)
        if self.debug:
            debugger.propagate = False
            debugger.debug(msg)
            debugger.propagate = True

    def log_exception(self, msg, **kwargs):
        log.exception(msg, **kwargs)
        if self.debug:
            debugger.propagate = False
            debugger.exception(msg)
            debugger.propagate = True

    def debug_info(self, msg):
        if self.debug:
            debugger.propagate = False
            debugger.info(f"[INFO]: {msg}")
            debugger.propagate = True

    def debug_warn(self, msg):
        if self.debug:
            debugger.propagate = False
            debugger.info(f"[WARN]: {msg}")
            debugger.propagate = True

    def debug_debug(self, msg):
        if self.debug:
            debugger.propagate = False
            debugger.info(f"[DEBUG]: {msg}")
            debugger.propagate = True

    def debug_exception(self, msg):
        if self.debug:
            debugger.propagate = False
            debugger.info(f"[EXCEPTION]: {msg}")
            debugger.propagate = True

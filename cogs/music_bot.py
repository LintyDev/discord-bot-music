import discord
import dotenv
import os
import yt_dlp
from discord.ext import commands
from utils.checks import *
from utils.errors import *
from services.youtube_api import Youtube_API
from functools import partial

class MusicCog(commands.Cog):
    def __init__(self, bot: commands.Bot, youtube_api_key) -> None:
        self.bot = bot
        self.playlist = []
        self.youtube = Youtube_API(youtube_api_key)
        self.is_in_channel = False
        self.leave_check =  False
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.errors) -> discord.Message:
        await handle_error(self, ctx, error=error)
        
    def error_send(msg: str) -> None:
        raise BotError(f"{msg}")
    
    # Commande Join
    @commands.check(check_user_channel)
    @commands.check(check_bot_channel)
    @commands.guild_only()
    @commands.hybrid_command(name="join")
    async def join_command(self, ctx: commands.Context) -> discord.Message:
        channel = ctx.author.voice.channel
        bot_user = ctx.guild.me
        
        # Check if bot is already in a voice channel
        if ctx.guild.voice_client is not None:
            raise BotError(f"{bot_user.name} is already in a voice channel")
        # Connect bot and mute him
        voice_bot = await channel.connect()
        await voice_bot.guild.change_voice_state(channel=channel, self_mute=True)
        # is in channel now is true
        self.is_in_channel = True
        # Send a message ready to add in playlist
        return await ctx.send("Ready to use ./add url_youtube and ./play")

    # Command Add
    @commands.check(check_bot_channel)
    @commands.guild_only()
    @commands.hybrid_command(name="add")
    async def add_command(self, ctx: commands.Context, *, search: str) -> discord.Message:
        # Check if video exist and send to playlist
        res_yt = self.youtube.search(search)
        if res_yt["items"]:
            item = res_yt["items"][0]
            title = item["snippet"]["title"]
            id = item["id"]["videoId"]
            
            video_info = {
                "title" : title,
                "url" : f"https://www.youtube.com/watch?v={id}"
            }
            self.playlist.append(video_info)
            return await ctx.send(f"{title} : added to playlist")
        else:
            return await ctx.send("No video found")
    
    # Command LIST
    @commands.check(check_bot_channel)
    @commands.guild_only()
    @commands.hybrid_command(name="list", with_app_command=True)
    async def list_command(self, ctx: commands.Context) -> discord.Message:
        if self.playlist:
            res = "Playlist : \n" + "\n".join([item["title"] for item in self.playlist])
        else:
            res = "Empty playlist"
        return await ctx.send(res)
    
    # Command Play
    @commands.check(check_bot_is_playing)
    @commands.check(check_user_channel)
    @commands.check(check_bot_channel)
    @commands.guild_only()
    @commands.hybrid_command(name="play")
    async def play_command(self, ctx: commands.Context) -> None:
        # bot is in channel ?
        if not self.is_in_channel:
            return await ctx.send(f"{ctx.bot.user.name} must be in a voice channel use ./join")
        # playlist empty ?
        if not self.playlist:
            return await ctx.send("Can't play music if playlist is empty")
        
        to_play = self.playlist[0]["title"]
        to_play_url = self.playlist[0]["url"]
        voice_client = ctx.guild.voice_client
        
        file = self.youtube.get_audio(to_play_url)
        # a voir !!!
        # discord.opus.load_opus('/opt/homebrew/Cellar/opus/1.4/lib/libopus.dylib')
        
        # Play musique and send message
        callback = partial(self.after_playback, ctx=ctx, current_file=file)
        voice_client.play(discord.FFmpegPCMAudio(file), after=callback)
        await ctx.send(f"Playing... {to_play}")
    
    # function 
    def after_playback(self, error, ctx: commands.Context, current_file) -> None:
        os.remove(current_file)
        if error:
            self.bot.loop.create_task(ctx.send("Error append please reload the bot (type ./leave and after ./join)"))
            return
        if self.leave_check:
            self.leave_check = False
            return
        self.playlist.pop(0)
        if self.playlist:
            self.bot.loop.create_task(self.play_command(ctx))
        else:
            self.bot.loop.create_task(ctx.send("No more music in playlist (type ./add)"))
            return
        
    # Command Stop
    @commands.check(check_bot_is_not_playing)
    @commands.check(check_user_channel)
    @commands.check(check_bot_channel)
    @commands.guild_only()
    @commands.hybrid_command(name="stop")
    async def stop_command(self, ctx: commands.Context) -> discord.Message:
        self.leave_check = True
        text = ""
        self.playlist.pop(0)
        # bot is in channel ?
        if not self.is_in_channel:
            return await ctx.send(f"{ctx.bot.user.name} must be in a voice channel use ./join")
        if not self.playlist:
            text = "No more music in playlist (type ./add)"
        else:
            text = f"Next will be {self.playlist[0]["title"]} ! Type ./play"
        
        ctx.voice_client.pause()
        return await ctx.send(f"Music stopped - {text}")
    
    # Command Next
    @commands.check(check_bot_is_not_playing)
    @commands.check(check_user_channel)
    @commands.check(check_bot_channel)
    @commands.guild_only()
    @commands.hybrid_command(name="next")
    async def next_command(self, ctx: commands.Context) -> None:
        # bot is in channel ?
        if not self.is_in_channel:
            return await ctx.send(f"{ctx.bot.user.name} must be in a voice channel use ./join")
        
        await ctx.send("Next...")
        return ctx.voice_client.stop()
    
    # Command Leave
    @commands.check(check_user_channel)
    @commands.check(check_bot_channel)
    @commands.guild_only()
    @commands.hybrid_command(name="leave")
    async def leave_command(self, ctx: commands.Context) -> discord.Message:
        self.leave_check = True
        # bot is in channel ?
        if not self.is_in_channel:
            return await ctx.send(f"{ctx.bot.user.name} must be in a voice channel use ./join")
        
        ctx.voice_client.pause()
        await ctx.voice_client.disconnect()
        return await ctx.send(f"{ctx.bot.user.name} disconnected !")
        
    
async def setup(bot: commands.Bot) -> None:
    dotenv.load_dotenv()
    api_yt = os.getenv("YOUTUBE_API_KEY")
    await bot.add_cog(MusicCog(bot, api_yt))
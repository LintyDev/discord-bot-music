import discord
from discord.ext import commands
from utils.checks import *
from utils.errors import *

class MusicCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.playlist = []
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.errors) -> discord.Message:
        await handle_error(self, ctx, error=error)
    
    @commands.check(check_user_channel)
    @commands.check(check_bot_channel)
    @commands.guild_only()
    @commands.hybrid_command(name="join")
    async def join_command(self, ctx: commands.Context) -> discord.Message:
        channel = ctx.author.voice.channel
        bot_user = ctx.guild.me
        
        # Check if bot is already in a voicce channel
        if ctx.guild.voice_client is not None:
            raise BotError(f"{bot_user.name} is already in a voice channel")
        # Connect bot and mute him
        voice_bot = await channel.connect()
        await voice_bot.guild.change_voice_state(channel=channel, self_mute=True)
        # Send a message ready to add in playlist
        return await ctx.send("Ready to use ./add url_youtube and ./play")

    @commands.check(check_bot_channel)
    @commands.guild_only()
    @commands.hybrid_command(name="add")
    async def add_command(self, ctx: commands.Context, url: str) -> discord.Message:
        self.playlist.append(url)
        return await ctx.send(f"{url} added to playlist")
    
    @commands.check(check_bot_channel)
    @commands.guild_only()
    @commands.hybrid_command(name="list")
    async def list_command(self, ctx: commands.Context) -> discord.Message:
        if self.playlist:
            res = "Playlist : \n" + "\n".join(self.playlist)
        else:
            res = "Empty playlist"
        return await ctx.send(res)
    
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(MusicCog(bot))
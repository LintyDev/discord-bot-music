import discord
from discord.ext import commands
from utils.checks import *
from utils.errors import *

class MusicCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.errors) -> discord.Message:
        await handle_error(self, ctx, error=error)
    
    @commands.check(check_user_channel)
    @commands.check(check_bot_channel)
    @commands.guild_only()
    @commands.hybrid_command(name="join")
    async def join_command(self, ctx: commands.Context) -> discord.Message:
        
        return await ctx.send("Prêt à gérer la playlist.")
    
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(MusicCog(bot))
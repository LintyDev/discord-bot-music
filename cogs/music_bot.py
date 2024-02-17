import discord
from discord.ext import commands

class MusicCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        
    @commands.hybrid_command(name="join")
    async def join_command(self, ctx: commands.Context) -> discord.Message:
        return await ctx.send("Prêt à rejoindre le canal et gérer la playlist.")
    
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(MusicCog(bot))
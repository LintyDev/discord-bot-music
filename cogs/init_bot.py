import discord
from discord.ext import commands

class InitCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self) -> None:
        for guild in self.bot.guilds:
            print(f"Connected on {guild.name}")
            channel_name = "lintymusic-bot"
            existing_channel = discord.utils.get(guild.text_channels, name=channel_name)
            
            if not existing_channel:
               existing_channel = await guild.create_text_channel(channel_name)
            
            await existing_channel.send("Hello, I'm ready to work ! (make an embed message with some help)")
    
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(InitCog(bot))
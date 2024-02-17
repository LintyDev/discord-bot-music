import dotenv
import os
import discord
from discord.ext import commands

class Bot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix="!", intents=discord.Intents.all())
        
    async def setup_hook(self) -> None:
        dotenv.load_dotenv()
        await self.load_extension("cogs.init_bot")
        await self.load_extension("cogs.music_bot")
        await self.tree.sync(guild=discord.Object(id=os.getenv("GUILD_ID")))
    
    async def on_ready(self) -> None:
        
        print(f"{self.user.name} is up!")

bot = Bot()
if __name__ == "__main__":
    dotenv.load_dotenv()
    bot.run(token=os.getenv("TOKEN"))
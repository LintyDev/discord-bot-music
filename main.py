import dotenv
import os
import discord
from discord.ext import commands
from discord import app_commands

class Bot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix="!", intents=discord.Intents.all())
        
    async def setup_hook(self) -> None:
        await self.load_extension("cogs.init_bot")
        await self.load_extension("cogs.music_bot")
        await self.tree.sync()
    
    async def on_ready(self) -> None:
        print(f"{self.user.name} is up!")

bot = Bot()
if __name__ == "__main__":
    dotenv.load_dotenv()
    bot.run(token=os.getenv("TOKEN"))
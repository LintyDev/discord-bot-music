import discord
from discord.ext import commands
        
async def handle_error(self, ctx: commands.Context, error: commands.errors) -> discord.Message:
        if isinstance(error, commands.CheckFailure):
            return await ctx.send(f"{self.bot.user.name} can't go here")
        else:
            return await ctx.send(f"Error: {error}")
import discord
from discord.ext import commands

class BotError(commands.CommandError):
    def __init__(self, message=None):
        super().__init__(message)
        
async def handle_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
        if isinstance(error, BotError):
            return await ctx.send(error)
        else:
            return await ctx.send(f"Error: {error}")
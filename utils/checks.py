import discord
from discord.ext import commands
from utils.errors import BotError

def check_bot_channel(ctx: commands.Context) -> bool:
    if ctx.channel.name != "lintymusic-bot":
        raise BotError(f"{ctx.bot.user.name} can't go here")
    return True

def check_user_channel(ctx: commands.Context) -> bool:
    if ctx.author.voice is None or ctx.author.voice.channel is None:
        raise BotError("You must be in a voice channel before issuing this command")
    return True
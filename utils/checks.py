import discord
from discord.ext import commands
from utils.errors import BotError

def check_bot_channel(ctx: commands.Context) -> bool:
    if ctx.channel.name != "lintymusic-bot":
        raise BotError(f"{ctx.bot.user.name} can't go here - Type in #lintymusic_bot")
    return True

def check_user_channel(ctx: commands.Context) -> bool:
    if ctx.author.voice is None or ctx.author.voice.channel is None:
        raise BotError("You must be in a voice channel before issuing this command")
    return True

def check_bot_is_playing(ctx: commands.Context) -> bool:
    if ctx.voice_client.is_playing():
        raise BotError(f"{ctx.bot.user.name} is already playing music !")
    return True

def check_bot_is_not_playing(ctx: commands.Context) -> bool:
    if not ctx.voice_client.is_playing():
        raise BotError(f"{ctx.bot.user.name} does not play music !")
    return True
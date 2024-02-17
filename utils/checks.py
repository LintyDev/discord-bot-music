from discord.ext import commands

def check_bot_channel(ctx: commands.Context) -> bool:
    return ctx.channel.name == "lintymusic-bot"
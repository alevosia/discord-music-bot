import discord
import logging
# my modules
import config
import classes
import functions
import embeds

logging.basicConfig(level=logging.INFO)
from discord.ext import commands
discord.opus.load_opus('libopus')
Bot = commands.Bot(command_prefix=config.prefix, description=config.description)
Bot.remove_command('help')

Player = classes.Player()

#@Bot.event
#async def on_ready():
    #musicSpamChannel = Bot.get_channel(config.MusicSpamChannelID)
    #print('{} reporting for duty!'.format(Bot.user.display_name))
    #await musicSpamChannel.send('{} reporting for duty!'.format(Bot.user.display_name))

@Bot.command()
async def help(ctx):
    """sends the list of commands"""
    await embeds.SendHelp(ctx)

@Bot.command()
async def join(ctx):
    """invites the bot to join the music voice channel"""
    await functions.JoinVoiceChannel(Bot, Player, ctx)

@Bot.command()
async def disconnect(ctx):
    return

@Bot.command()
async def play(ctx):
    """plays a song using its title or youtube url"""
    await functions.PlayMusic(ctx)

@Bot.command()
async def search(ctx):
    """search a song using its title then sends a list of songs"""
    return

@Bot.command()
async def queue(ctx):
    return

@Bot.command()
async def skip(ctx):
    return

@Bot.command()
async def loop(ctx):
    return

@Bot.command()
async def rbt(ctx):
    """reboots the bot"""
    await functions.Reboot(Bot, ctx)

@Bot.command()
async def ping(ctx):
    """sends the bot's ping in seconds"""
    await ctx.send('My ping: {}ms'.format(Bot.latency))

if discord.opus.is_loaded():
    logging.info('libopus is loaded. Running bot...')
    Bot.run(config.TOKEN)
else:
    logging.error('libopus failed to load')


import discord
import logging
# my modules
import config
import classes
import functions
import helpers
import embeds

logging.basicConfig(level=logging.INFO)
from discord.ext import commands
discord.opus.load_opus('libopus')

Bot = commands.Bot(command_prefix=config.prefix, description=config.description)
Bot.owner_id = config.OwnerID
Bot.remove_command('help')

Player = classes.Player()

# when the is up and running
@Bot.event
async def on_ready():
    musicSpamChannel = Bot.get_channel(config.MusicSpamChannelID)
    print('{} reporting for duty!'.format(Bot.user.display_name))
    await musicSpamChannel.send('{} reporting for duty!'.format(Bot.user.display_name))

@Bot.event
async def on_command_error(ctx, exception):
    print(exception)
    #await ctx.send(exception)

@Bot.check
async def IsOnMusicSpamChannel(ctx):
    if ctx.message.channel.id == config.MusicSpamChannelID:
        return True
    else:
        await ctx.send('{}, please use my commands on {}.'.format(ctx.author.mention, Bot.get_channel(config.MusicSpamChannelID).name))
        return False

# BOT COMMANDS =================================================================
@Bot.command()
async def help(ctx):
    '''sends the list of commands'''
    await embeds.SendHelp(ctx)

@Bot.command()
async def say(ctx, *, message):
    '''makes the bot say something'''
    await ctx.send(message)

@Bot.command()
async def join(ctx):
    '''invites the bot to join the music voice channel'''
    await functions.JoinVoiceChannel(Bot, Player, ctx.message)

@Bot.command()
async def disconnect(ctx):
    '''disconnects the bot from the music voice channel'''
    await functions.DisconnectVoiceChannel(Player, ctx.message)

@Bot.command()
async def play(ctx):
    '''plays a song using its title or youtube url'''
    await functions.PlayMusic(Bot, Player, ctx.message)

@Bot.command()
async def search(ctx):
    '''search a song using its title then sends a list of songs'''
    await functions.SearchMusic(Bot, ctx.message, Player)

@Bot.command()
async def queue(ctx):
    await embeds.SendQueue(Bot, Player.Queue, ctx.message)

@Bot.command()
async def skip(ctx):
    await functions.SkipSong(Player, ctx.message)

@Bot.command()
async def pause(ctx):
    await functions.PauseSong(Player, ctx.message)

@Bot.command()
async def resume(ctx):
    await functions.ResumeSong(Player, ctx.message)

@Bot.command()
async def remove(ctx):
    await functions.RemoveSong(Player, ctx.message)

@Bot.command()
async def volume(ctx):
    await functions.SetVolume(Player, ctx.message)

@Bot.command()
async def mute(ctx):
    await functions.Mute(Player, ctx.message)

@Bot.command()
async def unmute(ctx):
    await functions.Unmute(Player, ctx.message)

@Bot.command()
async def loopsong(ctx):
    await functions.SetLoopSong(Player, ctx.message)

@Bot.command()
async def loopqueue(ctx):
    await functions.SetLoopQueue(Player, ctx.message)

@Bot.command()
async def rbt(ctx):
    '''reboots the bot'''
    await functions.Reboot(Bot, Player, ctx.message)

@Bot.command()
async def ping(ctx):
    '''sends the bot's ping in milli-seconds'''
    await ctx.send('My ping is {}ms'.format(int(Bot.latency*1000)))

# runs the bot if opus is loaded
if discord.opus.is_loaded():
    logging.info('libopus is loaded. Running bot...')
    Bot.run(config.TOKEN)
else:
    logging.error('libopus failed to load')


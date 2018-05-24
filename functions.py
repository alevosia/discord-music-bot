import os
import sys
# my modules
import config

async def Reboot(Bot, ctx):
    if ctx.author.id == config.OwnerID:
        await ctx.send('Rebooting...')
        await Bot.logout()
        python = sys.executable
        os.execl(python, python, 'main.py')
    else:
        await ctx.send('{}, you are not authorized to reboot me.'.format(ctx.author.mention))

async def PlayMusic(ctx):
    return True

async def JoinVoiceChannel(Bot, Player, ctx):
    Player.voice = await Bot.get_channel(config.MusicVoiceChannelID).connect()
import os
import sys
import asyncio
# my modules
import config
import helpers
import embeds

async def Reboot(Bot, Player, Message):
    if Message.author.id == config.OwnerID:
        if Player.voice != None:
            await Player.DisconnectVoiceChannel()
            
        await Message.channel.send('Rebooting...')
        await Bot.logout()
        python = sys.executable
        os.execl(python, python, 'main.py')
    else:
        await Message.channel.send('{}, you do not have the will to reboot me.'.format(Message.author.mention))

async def JoinVoiceChannel(Bot, Player, Message):
    if Player.voice == None:
        Player.SetVoice(await Bot.get_channel(config.MusicVoiceChannelID).connect())
        await Message.channel.send('Joined into the music voice channel by {}.'.format(Message.author.display_name))
    else:
        await Message.channel.send('{}, I am already connected to a voice channel.'.format(Message.author.mention))

async def DisconnectVoiceChannel(Player, Message):
    # if the bot isn't connected to any voice channel
    if Player.voice != None:
        await Player.DisconnectVoiceChannel()
        await Message.channel.send('{} disconnected me from the music voice channel.'.format(Message.author.display_name))
    else:
        await Message.channel.send('{}, I am not connected to the music voice channel.'.format(Message.author.mention))
    
async def PlayMusic(Bot, Player, Message):
    # if the bot isn't joined to a voice channel yet
    if len(Bot.voice_clients) == 0:
        await JoinVoiceChannel(Bot, Player, Message)

    query = Message.content[Message.content.find(' ')+1:]
    print('Search Query: {}'.format(query))

    if 'youtube.com/playlist?list=' in query:
        return

    else: # get song by title or video url
        Song = helpers.GetSongs(Message, 1)
        if Song == None:
            await Message.channel.send('Search failed.')
            return

        Player.Queue.AddSong(Song)
        await embeds.SendAddedToQueue(Bot, Player.Queue)

        if Player.Queue.size() == 1:
            await Player.PlaySong(Song, Bot)

async def SearchMusic(Bot, Message, Player):
    searcher = Message.author

    # if the bot isn't joined to a voice channel yet
    if len(Bot.voice_clients) == 0:
        await JoinVoiceChannel(Bot, Message, Player)

    searchSongs = helpers.GetSongs(Message, 2)
    if searchSongs == None:
        await Message.channel.send('{}, search failed.'.format(Message.author.mention))
        return

    await embeds.SendSearchResults(Bot, Message, Player, searchSongs)

    def CheckResponse(Message):
        if Message.content.lower() == 'cancel' or Message.content.lower() == 'exit':
            return True
        if Message.author == searcher:
            try:
                number = int(Message.content)
                if number >= 1 and number <= config.MaxSearchResults:
                    print('Valid number caught!')
                    return True
                else:
                    print('Invalid number caught!')
                    asyncio.run_coroutine_threadsafe(Message.channel.send('Number {} is not in search results.'.format(number)), Bot.loop)
                    return False
            except ValueError:
                print('Value Error Exception!')
                asyncio.run_coroutine_threadsafe(Message.channel.send('Invalid input. Make sure to enter a number.'), Bot.loop)
                return False


    response = await Bot.wait_for('message', check=CheckResponse)
    if response != None:
        if (response.content.lower() == 'cancel' or response.content.lower() == 'exit'):
            await Message.channel.send('Search cancelled.')
        else:
            position = int(response.content)
            Song = searchSongs[position-1]
            Player.Queue.AddSong(Song)
            await embeds.SendAddedToQueue(Bot, Player.Queue)
            print('Queue Size: {}'.format(Player.Queue.size()))
            if Player.Queue.size() == 1:
                await Player.PlaySong(Song, Bot)
    else:
        await Message.channel.send('Search timed out.')

async def SkipSong(Player, Message):
    if (Player.Queue.size() > 0):
        await Message.channel.send('{} skipped {}.'.format(Message.author.display_name, Player.Queue.songs[0].title))
        Player.SkipSong()
    else:
        await Message.channel.send('{}, there is no song playing.'.format(Message.author.mention))

async def RemoveSong(Player, Message):
    if (Player.Queue.size() > 1):
        try:
            pos = int(Message.content[Message.content.find(' '):])
            await Message.channel.send('{} removed {}'.format(Message.author.display_name, Player.Queue.songs[pos-1].title))
            Player.Queue.RemoveSong(pos)
        except ValueError:
            await Message.channel.send('{}, invalid input. Please enter a number.'.format(Message.author.mention))
    else:
        await Message.channel.send('{}, no song available to be removed.'.format(Message.author.mention))

async def PauseSong(Player, Message):
    if (Player.Queue.size() > 0):
        if (Player.voice.is_playing):
            await Message.channel.send('{} paused {}.'.format(Message.author.display_name, Player.Queue.songs[0].title))
            Player.PauseSong()
        else:
            await Message.channel.send('{}, I am already paused.'.format(Message.author.mention))
    else:
        await Message.channel.send('{}, there is no song in the queue.'.format(Message.author.mention))

async def ResumeSong(Player, Message):
    if (Player.Queue.size() > 0):
        if (Player.voice.is_paused):
            await Message.channel.send('{} resumed {}.'.format(Message.author.display_name, Player.Queue.songs[0].title))
            Player.PauseSong()
        else:
            await Message.channel.send('{}, I am already playing.'.format(Message.author.mention))
    else:
        await Message.channel.send('{}, there is no song in the queue.'.format(Message.author.mention))

async def SetLoopSong(Player, Message):
    Player.Queue.SetLoopSong()
    if Player.Queue.isLoopingSong: loopsong = 'enabled'
    else: loopsong = 'disabled'

    await Message.channel.send('{} {} song loop.'.format(Message.author.display_name, loopsong))

async def SetLoopQueue(Player, Message):
    Player.Queue.SetLoopQueue()
    if Player.Queue.isLoopingQueue: loopqueue = 'enabled'
    else: loopqueue = 'disabled'

    await Message.channel.send('{} {} queue loop.'.format(Message.author.display_name, loopqueue))

async def SetVolume(Player, Message):
    if Player.source != None:
        try:
            volume = float(Message.content[Message.content.find(' ')+1:])
            Player.SetVolume(volume)
            await Message.channel.send('{} set my volume to {}.'.format(Message.author.mention, Player.source.volume))
        except ValueError:
            await Message.channel.send('{}, invalid volume. Number must be between 0 to 2.0.'.format(Message.author.mention))
    else:
        await Message.channel.send('{}, no song is playing.'.format(Message.author.mention))

async def Mute(Player, Message):
    if Player.source.volume > 0:
        Player.SetVolume(0)
        await Message.channel.send('{} muted me.'.format(Message.author.display_name))
    else:
        await Message.channel.send('{}, I am already muted.'.format(Message.author.mention))

async def Unmute(Player, Message):
    if Player.source.volume <= 0:
        Player.SetVolume(.5)
        await Message.channel.send('{} unmuted me. Thank you! :heartpulse:'.format(Message.author.display_name))
    else:
        await Message.channel.send('{}, I\'m not muted.'.format(Message.author.mention))

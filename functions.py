import os
import sys
import asyncio
# my modules
import config
import helpers
import embeds

async def Reboot(Bot, Player, Message):
    # checks if the one executing the command is the owner of the bot
    # which can be set on the config.py module
    if Message.author.id == config.OwnerID:
        # if the bot is currently connected to a voice channel, disconnect it first
        if Player.voice != None:
            await Player.DisconnectVoiceChannel()
        
        await Message.channel.send('Rebooting...')
        await Bot.logout()
        # reruns the python script
        python = sys.executable
        os.execl(python, python, 'main.py')
    else:
        await Message.channel.send('{}, you do not have the will to reboot me.'.format(Message.author.mention))

async def JoinVoiceChannel(Bot, Player, Message):
    # if the bot is not connected to any voice channel
    if Player.voice == None:
        Player.SetVoice(await Bot.get_channel(config.MusicVoiceChannelID).connect())
        await Message.channel.send('Joined into the music voice channel by {}.'.format(Message.author.display_name))
    else:
        await Message.channel.send('{}, I am already connected to a voice channel.'.format(Message.author.mention))

async def DisconnectVoiceChannel(Player, Message):
    # if the bot is connected to any voice channel
    if Player.voice != None:
        await Player.DisconnectVoiceChannel()
        await Message.channel.send('{} disconnected me from the music voice channel.'.format(Message.author.display_name))
    else:
        await Message.channel.send('{}, I am not connected to the music voice channel.'.format(Message.author.mention))
    
async def PlayMusic(Bot, Player, Message):
    # if the bot isn't joined to a voice channel yet, join it first
    if len(Bot.voice_clients) == 0:
        await JoinVoiceChannel(Bot, Player, Message)

    # gets the search query or the song title from the command
    query = Message.content[Message.content.find(' ')+1:]
    print('Search Query: {}'.format(query))

    # if the query is a youtube playlist
    if 'youtube.com/playlist?list=' in query:
        return

     # get song by title or video url
    else:
        # a helper function from another module (helpers.py) 
        # which uses the Youtube Data API to search for Youtube videos and gather content details
        Song = helpers.GetSongs(Message, 1)

        # if a song was found, add the song to the queue
        if Song:
            Player.Queue.AddSong(Song)
        else:
            await Message.channel.send('Search failed.')
            return

        # sends an embedded message (for aesthetics) of the details of the song that's added to the queue
        await embeds.SendAddedToQueue(Bot, Player.Queue)

        # if the queue size is equal to one after adding a song, play it immediately
        if Player.Queue.size() == 1:
            await Player.PlaySong(Song, Bot)

async def SearchMusic(Bot, Player, Message):
    searcher = Message.author

    # if the bot isn't joined to a voice channel yet
    if len(Bot.voice_clients) == 0:
        await JoinVoiceChannel(Bot, Player, Message)

    # a helper function from another module (helpers.py) 
    # which uses the Youtube Data API to search for Youtube videos and gather content details
    searchSongs = helpers.GetSongs(Message, 2)
    if searchSongs == None:
        await Message.channel.send('{}, search failed.'.format(Message.author.mention))
        return

    # sends an embedded message containing the songs that matched the search
    await embeds.SendSearchResults(Bot, Message, Player, searchSongs)

    # a custom checker to check the response of the searcher or if the responder is the searcher
    # this returns true if a valid response is receive which is either a cancel or a search number
    # returns 
    def CheckResponse(Message):
        if Message.author == searcher:
            # cancels the search
            if Message.content.lower() == 'cancel' or Message.content.lower() == 'exit':
                return True

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

    # executes the checker function above to filter the responses
    # will keep checking until a True is received or it times out which returns a None
    response = await Bot.wait_for('message', check=CheckResponse, timeout=config.SearchTimeOut)

    # if a valid (True) response is received and did not timeout
    if response != None:
        # if the response is a cancel
        if (response.content.lower() == 'cancel' or response.content.lower() == 'exit'):
            await Message.channel.send('Search cancelled.')
        else:
            # gets the position number from the response
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
    # if the queue is not empty
    if (Player.Queue.size() > 0):
        await Message.channel.send('{} skipped {}.'.format(Message.author.display_name, Player.Queue.songs[0].title))
        Player.SkipSong()
    else:
        await Message.channel.send('{}, there is no song playing.'.format(Message.author.mention))

async def RemoveSong(Player, Message):
    # only executes if the queue size is greater than 1
    # to prevent removal of the first song
    if (Player.Queue.size() > 1):
        try:
            pos = int(Message.content[Message.content.find(' '):])
            await Message.channel.send('{} removed {}'.format(Message.author.display_name, Player.Queue.songs[pos-1].title))

            # a position is valid if it's greater than one and is within the queue size
            if pos > 1 or pos < Player.Queue.size():
                Player.Queue.RemoveSong(pos)
            
        # if no number is parsed from the command
        except ValueError:
            await Message.channel.send('{}, invalid input. Please enter a number.'.format(Message.author.mention))
    else:
        await Message.channel.send('{}, no song available to be removed.'.format(Message.author.mention))

async def PauseSong(Player, Message):
    # checks if the queue size is not empty
    if (Player.Queue.size() > 0):
        # only executes if the player is playing a song
        if (Player.voice.is_playing):
            await Message.channel.send('{} paused {}.'.format(Message.author.display_name, Player.Queue.songs[0].title))
            Player.PauseSong()
        else:
            await Message.channel.send('{}, I am already paused.'.format(Message.author.mention))
    else:
        await Message.channel.send('{}, there is no song in the queue.'.format(Message.author.mention))

async def ResumeSong(Player, Message):
    # checks if the queue is not empty
    if (Player.Queue.size() > 0):
        # only executes if the player is paused
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

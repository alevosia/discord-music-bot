import os
import sys
import asyncio
# my modules
import config
import helpers

async def Reboot(Bot, Message):
    if Message.author.id == config.OwnerID:
        await Message.channel.send('Rebooting...')
        await Bot.logout()
        python = sys.executable
        os.execl(python, python, 'main.py')
    else:
        await Message.channel.send('{}, you are not authorized to reboot me.'.format(Message.author.mention))

async def JoinVoiceChannel(Bot, Player, Message):
    if Player.voice == None:
        Player.SetVoice(await Bot.get_channel(config.MusicVoiceChannelID).connect())
        await Message.channel.send('Joined into the music voice channel by {}'.format(Message.author.display_name))
    else:
        Message.channel.send('{}, I am already connected to a voice channel.'.format(Message.author.mention))

async def DisconnectVoiceChannel(Player, Message):
    # if the bot isn't connected to any voice channel
    if Player.voice != None:
        await Player.DisconnectVoiceChannel()
        await Message.channel.send('{} disconnected me from the music voice channel'.format(Message.author.display_name))
    else:
        await Message.channel.send('{}, I am already connected to the music voice channel'.format(Message.author.mention))
    
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

        if Player.Queue.size() == 1:
            await Player.PlaySong(Song, Bot)

async def SearchMusic(Bot, Message, Player):
    # if the bot isn't joined to a voice channel yet
    if len(Bot.voice_clients) == 0:
        await JoinVoiceChannel(Bot, Message, Player)

    searchSongs = helpers.GetSongs(Message, 2)
    if searchSongs == None:
        await Message.channel.send('{}, search failed.'.format(Message.author.mention))
        return

    #await embeds.SendSearchResults(Bot, Message, Player, searchSongs)
    def CheckResponse(Message):
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


    #response = await Bot.wait_for('message', check=CheckResponse)
    
    #await Player.DeleteSearchResultsMessage(Bot)

async def SetVolume(Player, Message):
    if Player.source != None:
        try:
            volume = float(Message.content[Message.content.find(' ')+1:])
            Player.SetVolume(volume, Message)
        except ValueError:
            await Message.channel.send('{}, invalid volume. Number must be between 0 to 2.0'.format(Message.author.mention))
    else:
        await Message.channel.send('{}, no song is playing.'.format(Message.author.mention))
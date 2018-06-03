from discord import Embed
import config

async def SendHelp(ctx):
    embed = Embed(title='Commands List - Use the prefix {} before the command'.format(config.prefix), description='', color=0xFF0080)
    embed.add_field(name='join', value='makes me join the music voice channel', inline=False)
    embed.add_field(name='disconnect', value='makes me leave the music voice channel', inline=False)
    embed.add_field(name='play', value='play a song using its title or youtube url', inline=False)
    embed.add_field(name='search', value='search a song using its title then sends a list of songs', inline=False)
    embed.add_field(name='queue', value='sends the list of songs in the queue', inline=False)
    embed.add_field(name='skip', value='skips the currently playing song', inline=False)
    embed.add_field(name='pause', value='pauses the currenly playing song', inline=False)
    embed.add_field(name='resume', value='resumes the currently playing song', inline=False)
    embed.add_field(name='remove', value='removes a song in the queue using its position in the queue', inline=False)
    embed.add_field(name='volume', value='sets the volume of the song usgin 0 to 3.0', inline=False)
    embed.add_field(name='mute', value='mutes the song while it plays', inline=False)
    embed.add_field(name='unmute', value='unmutes the bot, obviously', inline=False)
    embed.add_field(name='loopsong', value='loops the currently playing song', inline=False)
    embed.add_field(name='loopqueue', value='loops the whole queue', inline=False)

    await ctx.send(embed=embed)

async def SendNowPlaying(Bot, Song):
    desc = '[{}]({})'.format(Song.title, Song.url)
    embed = Embed(title=None, description=desc, color=0x7CFC00)
    embed.set_author(name='Now playing\n', icon_url=Song.queuer.imageURL)
    embed.set_thumbnail(url=config.NowPlayingImagURL)
    embed.set_footer(text='Duration: {}'.format(Song.duration))
    channel = Bot.get_channel(config.MusicSpamChannelID)
    await channel.send(embed=embed)

async def SendAddedToQueue(Bot, Queue):
    pos = Queue.size()
    Song = Queue.songs[pos-1]
    desc = '[{}]({})'.format(Song.title, Song.url)
    authorText = '{} added to queue'.format(Song.queuer.name)
    footerText = 'Position: {} | Duration: {}'.format(pos, Song.duration)

    embed = Embed(title=None, description=desc, color=0xFF7F50)
    embed.set_author(name=authorText, icon_url=Song.queuer.imageURL)
    embed.set_thumbnail(url=Song.imageURL)
    embed.set_footer(text=footerText)
    channel = Bot.get_channel(config.MusicSpamChannelID)
    await channel.send(embed=embed)

async def SendSearchResults(Bot, Message, Player, searchSongs):
    searchQuery = Message.content[Message.content.find(' ')+1:]
    desc = ''
    i = 1
    for Song in searchSongs:
        desc += '{}. [{}]({}) | {}\n\n'.format(i, Song.title, Song.url, Song.duration)
        i += 1
    embed = Embed(title=None, color=0xFF0080, description=desc)
    embed.set_author(name='{}\'s Search Query: {}'.format(Message.author.display_name, searchQuery),icon_url=Message.author.avatar_url)
    await Message.channel.send(embed=embed)

async def SendQueue(Bot, Queue, Message):

    desc = 'Now playing'
    totalDuration = Queue.totalDuration
    m=s=0

    i=1
    for Song in Queue.songs:
        desc += '{}. [{}]({})\n{} | {}\n\n'.format(i, Song.title, Song.url, Song.duration, Song.queuer.name)
        i+=1

    if totalDuration >= 60:
        m = int(totalDuration / 60)
        s = int(totalDuration % 60)
        totalDuration = '{} minute(s), {} second(s)'.format(m,s)
    else:
        s = int(totalDuration)
        totalDuration = '{} second(s)'.format(s)

    embed = Embed(title=None, description=desc, color=0xFF0080)
    embed.set_author(name='Music Queue', icon_url=Message.author.avatar_url)
    embed.set_thumbnail(url=config.QueueImageURL)
    embed.set_footer(text='Total Duration: {}'.format(totalDuration))
    await Message.channel.send(embed=embed)
    
from discord import Embed
import config

async def SendHelp(ctx):
    embed = Embed(title='Commands List - Use the prefix {} before the command'.format(config.prefix), description='', color=0xFF0080)
    embed.add_field(name='join', value='makes me join the music voice channel', inline=False)
    embed.add_field(name='play', value='play a song using its title or youtube url', inline=False)
    embed.add_field(name='search', value='search a song using its title then sends a list of songs', inline=False)
    embed.add_field(name='queue', value='sends the list of songs in the queue', inline=False)
    embed.add_field(name='skip', value='skips the currently playing song', inline=False)
    embed.add_field(name='remove', value='removes a song in the queue using its position in the queue', inline=False)
    embed.add_field(name='loopsong', value='loops the currently playing song', inline=False)
    embed.add_field(name='loopqueue', value='loops the whole queue', inline=False)
    embed.add_field(name='disconnect', value='makes me leave the music voice channel', inline=False)

    await ctx.send(embed=embed)

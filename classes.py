import discord
import asyncio
import youtube_dl
# the user that queued the song/playlist
class Queuer:
    def __init__(self, queuerName, queuerImageURL):
        self.name = queuerName
        self.imageURL = queuerImageURL

# the songs to be added to the music queue
class Song:
    def __init__(self, songURL, songTitle, songDuration, songImageURL, queuerObject):
        self.url = songURL
        self.title = songTitle
        self.duration = songDuration
        self.imageURL = songImageURL
        self.queuer = queuerObject

class Queue:
    def __init__(self):
        self.songs = []

    def AddSong(self, Song):
        """adds a song to the end of the queue"""
        self.songs.append(Song)

    def RemoveSong(self, position):
        """removes a song from the queue using it position"""
        self.songs.pop(position-1)

    def size(self):
        """returns the number of songs in the queue"""
        return len(self.songs)

class Player:
    def __init__(self):
        self.voice = None
        self.source = None
        self.volume = 0.3
        self.opts = {
            'format': 'webm[abr>0]/bestaudio/best',
            'default_search': 'auto',
            'quiet': True
        }
        self.ydl = youtube_dl.YoutubeDL(self.opts)
        self.Queue = Queue()

    def SetVoice(self, VoiceClient):
        """Sets the voice client of the Player object after joining a voice channel"""
        self.voice = VoiceClient

    async def DisconnectVoiceChannel(self):
        """Disconnects the bot from the voice channel and reinitializes the Player object"""
        await self.voice.disconnect()
        self.__init__()
        
    def SetVolume(self, volume: float, Message):
        """Sets the volume of the Player's source using a float number"""
        self.volume = volume
        self.source.volume = self.volume

    async def PlaySong(self, Song, Bot):
        """Plays a song and updates the bot's presence with the title of the song"""
        await Bot.change_presence(activity=discord.Game(name=Song.title))
        info = self.ydl.extract_info(Song.url, download=False)
        self.source = discord.FFmpegPCMAudio(info['url'])
        # transforms the source so that it can handle volume commands
        self.source = discord.PCMVolumeTransformer(self.source, volume=self.volume)

        self.voice.play(self.source, after=lambda x: self.SongEnds(Bot))

    def SongEnds(self, Bot):
        """A function that executes whenever a song finishes playing"""
        self.source.cleanup()
        self.Queue.RemoveSong(1) # remove the first song
        if self.Queue.size() > 0:
            asyncio.run_coroutine_threadsafe(self.PlaySong(self.Queue.songs[0], Bot), Bot.loop)
        else:
            asyncio.run_coroutine_threadsafe(Bot.change_presence(activity=None), Bot.loop)


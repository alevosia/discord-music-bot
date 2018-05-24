from discord.ext import commands
import requests
import isodate
# my modules
import config
import classes

def GetSongs(Message, type):
    """
    Returns a song or a list of songs depending on the type parameter

    Parameters:  
    Message - the discord.Message object which should be from the queuer/searcher of the song

    type (int) - the type that indicates whether this should return a single song or a list of search songs  
    Possible types:    
        1 - single
        2 - list of search songs
    """
    searchSongs = []
    searchQuery = Message.content[Message.content.find(' ')+1:]
    print('GetSongs Query: {}'.format(searchQuery))

    url = 'https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&maxResults={}&key={}&q={}'.format(
        config.MaxSearchResults, config.YoutubeAPIKey, searchQuery)
    req = requests.get(url)
    if req.status_code == 200:
        results = req.json()

        for video in results['items']:
            videoID = video['id']['videoId']
            songURL = 'https://youtube.com/watch?v={}'.format(videoID)
            songTitle = video['snippet']['title']
            songImageURL = video['snippet']['thumbnails']['default']['url']

            url2 = 'https://www.googleapis.com/youtube/v3/videos?part=contentDetails&id={}&key={}'.format(videoID,config.YoutubeAPIKey)
            req2 = requests.get(url2)
            if req.status_code == 200:
                results2 = req2.json()
                songDuration = isodate.parse_duration(results2['items'][0]['contentDetails']['duration'])
                queuerName = Message.author.display_name
                queuerImageURL = Message.author.avatar_url
                Queuer = classes.Queuer(queuerName, queuerImageURL)
                Song = classes.Song(songURL, songTitle, songDuration, songImageURL, Queuer)
                if type == 1: return Song
                elif type == 2: searchSongs.append(Song)
            else:
                return None

        print('searchSongs Size: {}'.format(len(searchSongs)))
        if len(searchSongs) > 0:
            return searchSongs
        else:
            return None
    else:
        return None
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

    # the url to be executed to perform a GET request which returns a list of videos that matches the search query
    url = 'https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&maxResults={}&key={}&q={}'.format(
        config.MaxSearchResults, config.YoutubeAPIKey, searchQuery)
    req = requests.get(url) # executes the request

    # if the request status is successful
    if req.status_code == 200:
        results = req.json() # converts the results to json form for easier parsing of data

        # gets the details for each video in the search results
        for video in results['items']:
            videoID = video['id']['videoId']
            songURL = 'https://youtube.com/watch?v={}'.format(videoID)
            songTitle = video['snippet']['title']
            songImageURL = video['snippet']['thumbnails']['default']['url']

            # another request to get the content details of the current video in the loop
            url2 = 'https://www.googleapis.com/youtube/v3/videos?part=contentDetails&id={}&key={}'.format(videoID,config.YoutubeAPIKey)
            req2 = requests.get(url2)
            if req.status_code == 200:
                # converts the results to json form for easier parsing of data
                results2 = req2.json()
                # sets the details of the songs to be used to instantiate a Song object
                songDuration = isodate.parse_duration(results2['items'][0]['contentDetails']['duration'])
                queuerName = Message.author.display_name
                queuerImageURL = Message.author.avatar_url

                # the object which represents the queuer of the song
                Queuer = classes.Queuer(queuerName, queuerImageURL)
                # the object which contains the details of the song including the Queuer object
                # indices               0         1           2            3           4
                Song = classes.Song(songURL, songTitle, songDuration, songImageURL, Queuer)

                # if this function is ran to get a single song, return the song immediately
                if type == 1: return Song 

                # else if this function is executed to search for a list of songs
                # append the current song details to the list of search songs
                elif type == 2: searchSongs.append(Song)

            else:
                return None

        # if the search songs list is not empty
        if len(searchSongs) > 0:
            return searchSongs
        else:
            return None
    
    else: # else statement for the first request status code check in case I'm.. you're lost
        return None
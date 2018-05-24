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


class Player():
    def __init__(self):
        self.voice = None

    def PlaySong(self, Song):
        return

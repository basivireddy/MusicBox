from django.contrib.auth.models import Permission, User
from django.db import models

class Album(models.Model):
    artist = models.CharField(max_length=250)
    album_title = models.CharField(max_length=500)
    genre = models.CharField(max_length=100)
    album_logo = models.FileField()
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.album_title + ' - ' + self.artist


class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    song_title = models.CharField(max_length=250)
    audio_file = models.FileField(default='')
    lyricist = models.CharField(default='',max_length=250)
    singers = models.CharField(default='',max_length=250)
    lyrics_file = models.FileField(default='')
    #lyric = models.TextField(max_length=1000,default='')
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.song_title



class PlayList(models.Model):
    playlist_title = models.CharField(max_length=100)
    user = models.ForeignKey(User, default=1)

    def __str__(self):
        return self.playlist_title


class PlayListSong(models.Model):
    playlist = models.ForeignKey(PlayList, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.playlist) + ' - ' + str(self.song)


class Language(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Lyrics(models.Model):
    song = models.ForeignKey(Song,on_delete=models.CASCADE)
    language = models.ForeignKey(Language)
    #language = models.CharField(max_length=1000)
    lyric = models.TextField(max_length=1000)

    def __str__(self):
        return str(self.song) + ' - ' + str(self.language)



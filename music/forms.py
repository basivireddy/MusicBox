from django import forms
from django.contrib.auth.models import User

from .models import Album, Song, PlayList, PlayListSong


class AlbumForm(forms.ModelForm):

    class Meta:
        model = Album
        fields = ['artist', 'album_title', 'genre', 'album_logo']


class SongForm(forms.ModelForm):

    class Meta:
        model = Song
        fields = ['song_title', 'audio_file']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class PlayListForm(forms.ModelForm):

    class Meta:
        model = PlayList
        fields = ['playlist_title']


class PlayListSongForm(forms.ModelForm):

    class Meta:
        model = PlayListSong
        fields = ['playlist', 'song']
from django.contrib import admin
from .models import Album, Song, PlayList, PlayListSong

admin.site.register(Album)
admin.site.register(Song)
admin.site.register(PlayList)
admin.site.register(PlayListSong)


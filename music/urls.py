from django.conf.urls import url
from . import views

app_name = 'music'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    #url(r'^albums/$',views.index, name='albums'),
    url(r'album/(?P<album_id>[0-9]+)/$', views.album_detail, name='album_detail'),
    url(r'album/song/(?P<song_id>[0-9]+)/favorite/$', views.favorite, name='favorite'),
    url(r'^songs/(?P<filter_by>[a-zA_Z]+)/$', views.songs, name='songs'),
    url(r'^create_album/$', views.create_album, name='create_album'),
    url(r'^album/(?P<album_id>[0-9]+)/create_song/$', views.create_song, name='create_song'),
    url(r'^album/(?P<album_id>[0-9]+)/delete_song/(?P<song_id>[0-9]+)/$', views.delete_song, name='delete_song'),
    url(r'^album/(?P<album_id>[0-9]+)/favorite_album/$', views.favorite_album, name='favorite_album'),
    url(r'^album/(?P<album_id>[0-9]+)/delete_album/$', views.delete_album, name='delete_album'),
    url(r'^playlists/$',views.playlists,name='playlists'),
    url(r'^create_playlist/$', views.create_playlist, name='create_playlist'),
    url(r'^playlist/(?P<playlist_id>[0-9]+)/delete_playlist/$', views.delete_playlist, name='delete_playlist'),
    url(r'^playlist/(?P<playlist_id>[0-9]+)/$', views.playlist_detail, name='playlist_detail'),
    url(r'^album/(?P<album_id>[0-9]+)/add_song_playlist/$',views.add_song_playlist,name='add_song_playlist'),
    url(r'^playlist/(?P<playlist_id>[0-9]+)/(?P<song_id>[0-9]+)/remove_song_playlist/$', views.remove_song_playlist, name='remove_song_playlist'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
]

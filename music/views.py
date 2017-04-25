from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse,HttpResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .forms import AlbumForm, SongForm, UserForm, PlayListForm ,PlayListSongForm
from .models import Album, Song, PlayList, PlayListSong,Lyrics

AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


def create_album(request):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        form = AlbumForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            album = form.save(commit=False)
            album.album_logo = request.FILES['album_logo']
            file_type = album.album_logo.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'album': album,
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request, 'music/create_album.html', context)
            album.save()
            return render(request, 'music/album_detail.html', {'album': album})
        context = {
            "form": form,
        }
        return render(request, 'music/create_album.html', context)


def create_song(request, album_id):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        form = SongForm(request.POST or None, request.FILES or None)
        album = get_object_or_404(Album, pk=album_id)
        if form.is_valid():
            albums_songs = album.song_set.all()
            for s in albums_songs:
                if s.song_title == form.cleaned_data.get("song_title"):
                    context = {
                        'album': album,
                        'form': form,
                        'error_message': 'You already added that song',
                    }
                    return render(request, 'music/create_song.html', context)
            song = form.save(commit=False)
            song.album = album
            song.audio_file = request.FILES['audio_file']
            file_type = song.audio_file.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in AUDIO_FILE_TYPES:
                context = {
                    'album': album,
                    'form': form,
                    'error_message': 'Audio file must be WAV, MP3, or OGG',
                }
                return render(request, 'music/create_song.html', context)

            song.save()
            return render(request, 'music/album_detail.html', {'album': album})
        else:
            context = {
                'album': album,
                'form': form,
            }
            return render(request, 'music/create_song.html', context)


def delete_album(request, album_id):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        album = Album.objects.get(pk=album_id)
        album.delete()
        albums = Album.objects.all()
        return render(request, 'music/index.html', {'albums': albums})


def delete_song(request, album_id, song_id):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        album = get_object_or_404(Album, pk=album_id)
        song = Song.objects.get(pk=song_id)
        song.delete()
        album = get_object_or_404(Album, pk=album_id)
        return render(request, 'music/album_detail.html', {'album': album})


def album_detail(request, album_id):
        album = get_object_or_404(Album, pk=album_id)
        return render(request, 'music/album_detail.html', {'album': album})


def favorite(request, song_id):
    song = get_object_or_404(Song, pk=song_id)
    try:
        if song.is_favorite:
            song.is_favorite = False
        else:
            song.is_favorite = True
        song.save()
    except (KeyError, Song.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def favorite_album(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    try:
        if album.is_favorite:
            album.is_favorite = False
        else:
            album.is_favorite = True
        album.save()
    except (KeyError, Album.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def index(request):
    albums = Album.objects.all()
    song_results = Song.objects.all()
    query = request.GET.get("q")
    if query:
        albums = albums.filter(
            Q(album_title__icontains=query) |
            Q(artist__icontains=query)
        ).distinct()
        song_results = song_results.filter(
            Q(song_title__icontains=query)
        ).distinct()
        return render(request, 'music/index.html', {
            'albums': albums,
            'songs': song_results,
        })

    return render(request, 'music/index.html', {'albums': albums})


def songs(request, filter_by):
        try:
            song_ids = []
            for album in Album.objects.all():
                for song in album.song_set.all():
                    song_ids.append(song.pk)
            users_songs = Song.objects.filter(pk__in=song_ids)
            if filter_by == 'favorites':
                users_songs = users_songs.filter(is_favorite=True)
        except Album.DoesNotExist:
            users_songs = []
        return render(request, 'music/songs.html', {
            'song_list': users_songs,
            'filter_by': filter_by,
        })


def playlists(request):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        playlists = PlayList.objects.filter(user=request.user)
        return render(request, 'music/playlists.html', {'playlists': playlists})



def create_playlist(request):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        form = PlayListForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            playlist = form.save(commit=False)
            playlist.user = request.user
            playlist.save()
            playlists = PlayList.objects.filter(user=request.user)
            return render(request, 'music/playlists.html', {'playlists': playlists})
        else:
            context = {
                "form": form,
            }
            return render(request, 'music/create_playlist.html', context)


def delete_playlist(request, playlist_id):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        playlist = PlayList.objects.get(pk=playlist_id)
        playlist.delete()
        playlists = PlayList.objects.filter(user=request.user)
        return render(request, 'music/playlists.html', {'playlists': playlists})


def playlist_detail(request,playlist_id):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        playlist = get_object_or_404(PlayList, pk=playlist_id)
        song_ids = []
        for playlistsong in PlayListSong.objects.filter(playlist=PlayList.objects.filter(id=playlist_id)):
                song_ids.append(playlistsong.song.id)
        songs = Song.objects.filter(pk__in=song_ids)
        return render(request, 'music/playlist_detail.html', {'songs': songs,'playlist':playlist})


def add_song_playlist(request,album_id):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        form = PlayListSongForm(request.POST or None, request.FILES or None)
        album = get_object_or_404(Album, pk=album_id)
        if form.is_valid():
            playlistsong = form.save(commit=False)
            playlistsong.save()
            playlists = PlayList.objects.filter(user=request.user)
            return render(request, 'music/album_detail.html', {'album': album})
        else:
            context = {
                "form": form,
            }
            return render(request, 'music/add_song_playlist.html', context)

def remove_song_playlist(request, playlist_id, song_id):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        playlistsong = PlayListSong.objects.get(song_id=song_id,playlist_id=playlist_id)
        playlistsong.delete()
        playlist = get_object_or_404(PlayList, pk=playlist_id)
        song_ids = []
        for playlistsong in PlayListSong.objects.filter(playlist=PlayList.objects.filter(id=playlist_id)):
            song_ids.append(playlistsong.song.id)
        songs = Song.objects.filter(pk__in=song_ids)
        return render(request, 'music/playlist_detail.html', {'songs': songs,'playlist':playlist})

'''
def add_song_playlist(request,playlist_id,song_id):
    form = PlayListSongForm(request.POST or None, request.FILES or None)
    album = get_object_or_404(Album, pk=album_id)
    if form.is_valid():
        playlist_songs = PlayListSong.objects.filter(playlist=PlayList.objects.filter(id=playlist_id))
        song = get_object_or_404(Song, pk=song_id)
        playlist = get_object_or_404(PlayList, pk=playlist_id)
        for s in playlist_songs:
            playlist_song = get_object_or_404(Song, pk=s.song.id)
            if song.song_title == playlist_song.song_title:
                context = {
                    'playlist':playlist ,
                    'form': form,
                    'error_message': 'You already added that song',
                }
                return render(request, 'music/album_detail.html', context)
        playlistsong = form.save(commit=False)
        playlistsong.save()
        return render(request, 'music/album_detail.html', {'playlists': playlists})
    else:
        context = {
            "form": form,
        }
        return render(request, 'music/_detail.html', context)
'''
def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'music/login.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                albums = Album.objects.all()
                return render(request, 'music/index.html', {'albums': albums})
            else:
                return render(request, 'music/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'music/login.html', {'error_message': 'Invalid login'})
    return render(request, 'music/login.html')


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                albums = Album.objects.all()
                return render(request, 'music/index.html', {'albums': albums})
    context = {
        "form": form,
    }
    return render(request, 'music/register.html', context)



def lyrics(request,song_id):
     lyricid = Lyrics.objects.filter(song_id=song_id,language_id=1)
     lyric = get_object_or_404(Lyrics, pk=lyricid)
     return HttpResponse(lyric.lyric)


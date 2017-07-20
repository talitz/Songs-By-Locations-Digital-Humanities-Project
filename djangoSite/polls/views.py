from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import Song
from .models import CitiesInSong
from django.shortcuts import render
import json
from . import helper
import collections

def cityName(request, song_cities):
    return HttpResponse("You're looking at song")

def results(request, song_id):
    response = "You're looking at the cities of song %s."
    return HttpResponse(response % song_id)


def song_list(request):
    return HttpResponse(Song.objects.all())


def index(request):
    all_songs = Song.objects.all()
    songs_ids = [q.id for q in all_songs]
    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'index.html',
        context={'songs_name': Song.objects.all(),'songs_id': songs_ids},
    )

def contact(request):
    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'contact.html',
        context={},
    )

def search(request):
    print("DEBUG: VIEWS.py: search")
    songs_to_show = ""
    artist = request.GET.get('search_box_artist')
    song_name = request.GET.get('search_box_song')
    city = request.GET.get('search_box_city')
    if artist is not None:
        songs_to_show = Song.get_song_by_artist(artist)

    if song_name is not None:
        songs_to_show = Song.get_song_by_name(song_name)

    if city is not None:
        songs_to_show = CitiesInSong.get_song_by_city(city)

    songs_ids = [q.id for q in songs_to_show]
    stats = []
    for song in songs_ids:
        temp = CitiesInSong.get_locations_in_song(song)
        for loc in temp:
            stats.append(loc)

    #stats = list(set(stats))
    # Render the HTML template index.html with the data in the context variable
    print dict(collections.Counter(stats))
    return render(
        request,
        'search.html',
        context={'songs_list': songs_to_show,'songs_id': songs_ids, 'stats':dict(collections.Counter(stats)), },
    )


def find_song_by_id(request, song_id):
    # Render the HTML template index.html with the data in the context variable
    _song = Song.get_song_by_id(song_id)
    _locations = CitiesInSong.get_locations_in_song(song_id)
    _loc = []
    for loc in _locations:
        if loc not in _loc:
            _loc.append(loc)

    return render(
        request,
        'song.html',
        context={'song': _song, 'locations' : json.dumps(_locations)},
    )


def remove_city_by_song_id(request, song_id, city_name):
    CitiesInSong.remove_city_by_song_id_and_city(song_id, city_name)
    return HttpResponseRedirect('/findbyid/'+ str(song_id) +'/')


def find_song_by_name(request, song_name):
    # Render the HTML template index.html with the data in the context variable
    _song = Song.get_song_by_name(song_name)
    return render(
        request,
        'search.html',
        context={'song': _song},
    )


def find_song_by_artist(request, song_artist):
    # Render the HTML template index.html with the data in the context variable
    _song = Song.get_song_by_artist(song_artist)

    return render(
        request,
        'search.html',
        context={'song': _song},
    )


def download_ti_by_song_id(request, song_id):
    _song = Song.get_song_by_id(song_id)
    print 'im here'
    return helper.get_tei_template(_song.song_artist, _song.song_name, _song.song_text)

from django.http import HttpResponse
from .models import Song


def cityName(request, song_cities):
    return HttpResponse("You're looking at song %s." % Song.get_cities_in_song(song_cities))


def results(request, song_id):
    response = "You're looking at the cities of song %s."
    return HttpResponse(response % song_id)


def index(request):
    all_songs = Song.objects.all()
    output = ', '.join([q.song_artist for q in all_songs])
    return HttpResponse(output)

# Leave the rest of the views (detail, results, vote) unchanged
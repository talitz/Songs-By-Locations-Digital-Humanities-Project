from django.db import models


class Song(models.Model):
    song_name = models.CharField(max_length=200)
    song_artist = models.CharField(max_length=200)
    song_text = models.CharField(max_length=200)
    song_cities = models.CharField(max_length=200)

    def __str__(self):
        return self.song_text
    #pub_date = models.DateTimeField('date published')

    @staticmethod
    def get_cities_in_song(song_cities):
        return Song.objects.get(song_cities=song_cities)


class City(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    #votes = models.IntegerField(default=0)
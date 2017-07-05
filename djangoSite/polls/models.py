from django.db import models


class Song(models.Model):
    id = models.AutoField(primary_key=True, db_column='songId')
    song_name = models.CharField(max_length=200, db_column='songName')
    song_artist = models.CharField(max_length=200, db_column='songArtist')
    song_text = models.CharField(max_length=1000, db_column='songText')

    def __int__(self):
        return self.song_text

    @staticmethod
    def get_cities_in_song(song_cities):
        return Song.objects.get(song_cities=song_cities)


class CitiesInSong(models.Model):
    song_id = models.ForeignKey(Song, db_column='songId')
    city = models.CharField(primary_key=True, max_length=200, db_column='city')

    def __str__(self):
        return self.city


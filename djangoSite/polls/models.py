from django.db import models
import json

class Song(models.Model):
    id = models.AutoField(primary_key=True, db_column='songId')
    song_name = models.CharField(max_length=200, db_column='songName')
    song_artist = models.CharField(max_length=200, db_column='songArtist')
    song_text = models.CharField(max_length=1000, db_column='songText')

    def __int__(self):
        return self.song_text

    @staticmethod
    def get_song_by_id(id_song):
        return Song.objects.get(id=id_song)

    @staticmethod
    def get_song_by_name(name):
       return Song.objects.filter(song_name__contains=name)

    @staticmethod
    def get_song_by_artist(artist):
        return Song.objects.filter(song_artist=artist)

    @staticmethod
    def get_number_of_cities_by_artist(artist, city, art):
        songs = CitiesInSong.get_song_by_city(city)
        count = 0;
        #for song in songs:
         #   if song.song_artist == artist:
          #      count += 1
        return count


class CitiesInSong(models.Model):
    id = models.AutoField(primary_key = True, db_column = 'cityId')
    song = models.ForeignKey(Song, db_column = 'songId')
    city = models.CharField(max_length = 200, db_column = 'city')
    googleLoc = models.CharField(max_length = 200, db_column = 'googleLoc')

    @staticmethod
    def get_song_by_city(city_in_song):
        ob = CitiesInSong.objects.filter(googleLoc = city_in_song)
        songs = []
        for o in ob:
            if o.song not in songs:
                songs.append(o.song)
        return songs

    @staticmethod
    def get_song_by_city_with_dups(city_in_song):
        ob = CitiesInSong.objects.filter(googleLoc = city_in_song)
        songs = []
        for o in ob:
            songs.append(o.song)
        return songs

    @staticmethod
    def get_locations_in_song(id):
        ob = CitiesInSong.objects.filter(song_id = id)
        ret = []
        for i in ob:
            ret.append(i.city)
        return ret

    @staticmethod
    def get_google_locations_in_song(id):
        ob = CitiesInSong.objects.filter(song_id = id)
        ret = []
        for i in ob:
            ret.append(i.googleLoc)
        return ret

    @staticmethod
    def remove_city_by_song_id_and_city(song_id_to_delete, city_name_to_delete):
        print(song_id_to_delete)
        print(city_name_to_delete)
        city_to_delete = CitiesInSong.objects.filter(song_id=song_id_to_delete, city=city_name_to_delete)
        print(city_to_delete)
        city_to_delete.delete()



    def __str__(self):
        return self.city


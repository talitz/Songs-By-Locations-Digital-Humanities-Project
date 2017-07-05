from django.http import HttpResponse
from .models import Song
from .models import CitiesInSong
import os


def insert_to_db_from_file(request, file_name_to_open):
    print("insert_to_db_from_file")
    base_path = os.getcwd() + "/Db/TEIToText/results/gimel/"
    csv_file_path = base_path + file_name_to_open
    songs_data_path = base_path + "songs"
    print("file Name    " + "name   " + "city ")
    first = True
    with open(csv_file_path + '.tsv') as csvfile:
        lines = csvfile.readlines()
        for line in lines:
            if first:
                first = False
            else:
                add_line_to_db(line, songs_data_path)
        return HttpResponse("The db was updated with %s." % file_name_to_open)


def add_line_to_db(line, songs_data_path):
    new_line = line.split("\t")
    song_file_name = new_line[0].strip()
    artist = new_line[1].strip()
    city_song = new_line[2].strip()

    song_path = songs_data_path + "/" + artist + "/" + song_file_name
    with open(song_path) as csvfile:
        song_text = csvfile.readlines()
    song = Song()
    song.song_name = song_file_name[:-4]
    song.song_artist = artist
    song.song_text = song_text
    print("ADDING TO SONG:" + " song name: " + song.song_name + " song artist: " + song.song_artist)
    #print("song text: " + song.song_text)
    song.save()

    city_in_song = CitiesInSong()
    city_in_song.city = city_song
    city_in_song.song_id = song
    str = "ADDING TO CITIES IN SONG" + " song id: {} city: " + city_in_song.city
    print(str.format(song.id))
    city_in_song.save()

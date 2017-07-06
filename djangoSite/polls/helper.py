from django.http import HttpResponse
from .models import Song
from .models import CitiesInSong
import os
import csv


def insert_songs_to_db_from_db_folder(request):
    print("INSERTING SONGS TO DATABASE FROM DB FOLDER")
    base_path = os.getcwd()
    db_path = base_path + "/Db/songsText/"

    for dirName in os.listdir(db_path):
        if os.path.isdir(db_path + dirName):
            print(dirName)
            for songName in os.listdir(db_path + dirName):
                print(songName)
                song_path = db_path + dirName + "/" + songName
                with open(song_path) as songfile:
                    song_text = songfile.read()
                add_song_to_db(dirName, songName[:-4], song_text)
    return HttpResponse("The database was updated from :" + db_path)


def add_song_to_db(artistName, songName, song_text):
    print("INSERT: Song: " + songName + " Artist: " + artistName)
    song = Song()
    song.song_name = songName
    song.song_artist = artistName
    song.song_text = song_text
    song.save()


def insert_cities_in_song_to_db_from_file(request):
    print("INSERTING CITIES TO DATABASE FROM FILE")
    base_path = os.getcwd()
    file_to_load_path = base_path + "/Db/TEIToText/results/gimel/lexicon.tsv"
    with open(file_to_load_path) as tsv_file:
        tsv_file = csv.reader(tsv_file, delimiter='\t')
        for row in tsv_file:
            name = row[0][:-4]
            artist = row[1]
            city = row[2]
            add_city_to_db(name, artist, city)

    return HttpResponse("The database was updated from file")


def add_city_to_db(name, artist, city):
    song = Song.objects.filter(song_name=name, song_artist=artist).first()
    if song is not None:
            city_to_add = CitiesInSong()
            city_to_add.song = song
            city_to_add.city = city
            city_to_add.save()



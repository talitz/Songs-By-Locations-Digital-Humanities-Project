from django.http import HttpResponse
from .models import Song
from .models import CitiesInSong
import os



def insert_songs_to_db_from_db_folder(request):
    print("INSERTING SONGS TO DATABASE DB FOLDER")
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

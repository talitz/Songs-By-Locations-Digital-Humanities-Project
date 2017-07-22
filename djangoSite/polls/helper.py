from django.http import HttpResponse
from .models import Song
from .models import CitiesInSong
import os
import csv
import time
filepath = '/some/path/to/local/file.txt'
from django.views.static import serve
from django.utils.encoding import smart_str

def insert_songs_to_db_from_db_folder(request):
    base_path = os.getcwd()
    db_path = base_path + "/Db/TEIToText/results/zain/OnlySongs/"
    for dirName in os.listdir(db_path):
        if os.path.isdir(db_path + dirName):
            for songName in os.listdir(db_path + dirName):
                song_path = db_path + dirName + "/" + songName
                with open(song_path) as songfile:
                    song_text = songfile.read()
                add_song_to_db(dirName, songName[:-4], song_text)
    return HttpResponse("The database was updated from :" + db_path)


def add_song_to_db(artistName, songName, song_text):
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


def get_tei_template(autor, song_name, song_text, song_id):
    _locations = CitiesInSong.get_locations_in_song(song_id)
    print(_locations)
    for loc in _locations:
        song_text = song_text.replace(loc, "<placeName>" + loc + "</placeName>")

    tei = "<TEI>\n <teiHeader>\n <fileDesc>\n <titleStmt>\n <title>" + song_name +\
          "</title> \n<author>" + autor + "</author>\n </titleStmt>\n <publicationStmt>" +\
           "<publisher>Tal Yitzhak, Aviv Gorlik and Yoav Cohen, Ben Gurion University</publiser></publicationStmt>\n <sourceDesc><p>The website SongLyrics: http://songlyrics.co.il</p></sourceDesc>" +\
          "<p>created on" + time.strftime("%c") + "</p> </sourceDesc>\n </fileDesc>\n"+\
          "<profileDesc>\n<langUsage><language ident=""he"">Hebrew</language></langUsage>\n</profileDesc>\n</teiHeader>\n <text>\n" + "<body>\n <p>"
     
    counter = 1
     
    for stanza in song_text.split("\n\n")[:-1]:
    	tei = tei + "\n<lg number=""" + str(counter)  + " type=""stanza"">" + stanza + "</lg>"
    	counter = counter + 1

    tei = tei + "\n</p>\n </body>\n </text>\n </TEI>\n"

    output = StringIO.StringIO()
    output.write(tei)
    response = HttpResponse(output.getvalue(),content_type='application/force-download') # mimetype is replaced by content_type for django 1.7
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(song_name.encode('utf-8')+'.tei')
    return response

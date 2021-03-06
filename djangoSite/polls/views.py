from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import Song
from .models import CitiesInSong
from django.shortcuts import render
import json
from . import helper
import collections
from collections import Counter
from django.template.defaulttags import register
import pickle

@register.filter
def get_item(dictionary, key):
   # print int(key) , '####'
	return dictionary.get(int(key))

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


def create_dict(request):
	import requests
	from bs4 import BeautifulSoup
	dic={}
	pickle.dump(dic, open( "locs_list.p", "wb" ) )
	for entry in CitiesInSong.objects.all():
		lng = None
		lat = None
		try:
			if entry.googleLoc not in dic:
				url = 'https://maps.googleapis.com/maps/api/geocode/xml?language=he&address=' + entry.googleLoc+ '&key=AIzaSyCogn8eumPsEriVg11B9bbT0HOLiKob3CI'
				r = requests.get(url, timeout=30)
				soup = BeautifulSoup(r.content)
				lng = soup.find('lng').text
				lat = soup.find('lat').text
				if lng and lat:
					dic[entry.googleLoc] = (lng, lat)
			else:
				print 'already here'
		except:
			print 'no'

	pickle.dump(dic, open( "locs_list.p", "wb" ) )
	return HttpResponse('wow finish')


def search(request):
	str_to_return_by_title = ""
	str_to_return_by_content = ""
	str_to_return_by_artist = ""
	songs_to_show = ""
	artist = request.GET.get('search_box_artist')
	song_name = request.GET.get('search_box_song')
	city = request.GET.get('search_box_city')
	songs_ids = []
	artists_cities = []
	page_to_rend = "searchArtist.html";
	artists_city_count = {}
	songs_to_locations = {}
	stats = []
	artist_map = []
	
	
	artist_map = get_loc_map(artist)

	songs_to_show = Song.get_song_by_artist(artist)
	songs_ids = [q.id for q in songs_to_show]
	#locs_list = [CitiesInSong.get_google_locations_in_song(id) for id in songs_ids]

	# Get the cities in songs
	for song in songs_ids:
		songs_to_locations[song] = []
		cities_in_song = CitiesInSong.get_google_locations_in_song(song)
		for city_artist in cities_in_song:
				artists_cities.append(city_artist)
				songs_to_locations[song].append(city_artist)
		songs_to_locations[song] = list(set(songs_to_locations[song]))
		songs_to_locations[song] = ', '.join(songs_to_locations[song])
			
			
	if artist is not None:
		top_10 = collections.Counter(artists_cities).most_common(10)
		artists_cities2 = []
		page_to_rend = "searchArtist.html";
		for index, val in top_10:
			artists_cities2.append(index)
		
		for city_to_add in artists_cities2:
			songs_by_city = CitiesInSong.get_song_by_city(city_to_add)
			for song in set(songs_by_city):
				artist_to_add = song.song_artist
				stats.append(artist_to_add)

		temp = collections.Counter(stats).most_common(15)
		stats = []
		for x,y in temp:
			stats.append(x)

		if artist in stats:
			stats.remove(artist)

	if song_name is not None:
		songs_to_show = Song.get_song_by_name(song_name)
		songs_ids = [q.id for q in songs_to_show]
		page_to_rend = "searchTitle.html";
		
		# Get the cities in songs
		for song in songs_ids:
			cities_in_song = CitiesInSong.get_locations_in_song(song)
			for city_artist in cities_in_song:
					artists_cities.append(city_artist)

		# Get the artists which sing about the cities above
		for city_to_add in artists_cities:
			songs_by_city = CitiesInSong.get_song_by_city(city_to_add)
			for song in songs_by_city:
				artist_to_add = song.song_artist
				if artist_to_add not in stats:
					stats.append(artist_to_add)
		stats = []

	if city is not None:
		stats = []
		songs_to_show = CitiesInSong.get_song_by_city(city)
		songs_ids = [q.id for q in songs_to_show]
		page_to_rend = "searchCity.html";
		art = CitiesInSong.get_song_by_city_with_dups(city)
		artist_list = [song.song_artist for song in art]
		top_20 = collections.Counter(artist_list).most_common(20)
		artists_city_count = {}
		for index , val in top_20:
			artists_city_count[index] = val
	
	for song in songs_to_show:
		str_to_return_by_title += song.song_name + ',' + song.song_artist + '!'
		
	for song in songs_to_show:
		str_to_return_by_content += song.song_name + ',' + song.song_artist + '!'
			
	for song in songs_to_show:
		if song.id in songs_to_locations:
			str_to_return_by_artist += songs_to_locations[song.id] + ',' + song.song_name + ',' + song.song_artist + '!'
		else:
			str_to_return_by_artist += song.song_name + ',' + song.song_artist + '!'
			
	# Render the HTML template index.html with the data in the context variable
	return render(
		request,
		page_to_rend,
		context={'songs_list'		     	 	 :    songs_to_show,
				 'songs_id'  		    		 :    songs_ids,
				 'cities_in_song'	    		 :    json.dumps(dict(collections.Counter(artists_cities))), 
				 'artists_same_cities'  		 :    stats, 
				 'artists_city_count'   		 :    json.dumps(artists_city_count),
				 'songs_to_locations'    		 : 	  songs_to_locations,
				 'string_for_csv_by_artist'      :    str_to_return_by_artist,
				 'string_for_csv_by_content'     :    str_to_return_by_content,
				 'string_for_csv_by_title'	     :    str_to_return_by_title,
				 'locations'                     :    artist_map,
				 },
	)


def find_song_by_id(request, song_id):
	# Render the HTML template index.html with the data in the context variable
	_song = Song.get_song_by_id(song_id)
	_locations = CitiesInSong.get_locations_in_song(song_id)

	city_add = request.GET.get('add_box_city')
	song_id = request.GET.get('songId')

	if city_add and song_id is not None:
		if city_add in Song.get_song_by_id(song_id).song_text:
			city_to_add = CitiesInSong()
			city_to_add.song = Song.get_song_by_id(song_id)
			city_to_add.city = city_add
			city_to_add.googleLoc = city_add
			city_to_add.save()
		return HttpResponseRedirect('/findbyid/'+ str(song_id) +'/')

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


def create_point_object(name, song_name, lng, alt):
	point = {
		'type': 'Feature',
		'geometry': {
				'type': 'Point',
				'coordinates': [lng, alt]
					},
		'properties': {
				'name': name,
				'song_name' : song_name
					 }
			  }
	return point


def get_locations_to_map(request):
    locs_dict = pickle.load( open( "locs_list.p", "rb" ) )
    ret = pickle.load( open( "locarr.p", "rb" ) )
    '''
    songs_of_artist = Song.objects.all()
    for x in songs_of_artist:
        for loc in CitiesInSong.get_google_locations_in_song(x.id):
            if loc in locs_dict:           
                lng, lat = locs_dict[loc]
                ret.append([float(lat),float(lng),x.song_name,x.song_artist,loc])
    '''
    #pickle.dump( ret, open( "locarr.p", "wb" ) )
    return render(
    request,
    'map.html',
    context={'locations': json.dumps(ret)},
    )
       
def get_loc_map(id):
	locs_dict = pickle.load( open( "locs_list.p", "rb" ) )
	ret = []
	songs_of_artist = Song.objects.filter(song_artist=id)
	for x in songs_of_artist:
		for loc in CitiesInSong.get_google_locations_in_song(x.id):
			if loc in locs_dict:           
				lng, lat = locs_dict[loc]
				ret.append([float(lat),float(lng),x.song_name,loc])

	return json.dumps(ret)

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
	return helper.get_tei_template(_song.song_artist, _song.song_name, _song.song_text, song_id)
	


def get_locations_list(request):
	if request.is_ajax():
		q = request.GET.get('term', '')
		locs = CitiesInSong.objects.filter(googleLoc__icontains = q )[:20]
		#locs = ['tel aviv' , 'haifa' ,'brazil' , 'israel']
		results = []
		for loc in locs:
			if loc.googleLoc not in results:
				results.append(loc.googleLoc)
		data = json.dumps(results)
	else:
		data = 'fail'
	mimetype = 'application/json'
	return HttpResponse(data)

def get_artists_list(request):
	if request.is_ajax():
		q = request.GET.get('term', '')
		locs = Song.objects.filter(song_artist__icontains = q )[:20]
		results = []
		for loc in locs:
			if loc.song_artist not in results:
				results.append(loc.song_artist)
		data = json.dumps(results)
	else:
		data = 'fail'
	mimetype = 'application/json'
	return HttpResponse(data)

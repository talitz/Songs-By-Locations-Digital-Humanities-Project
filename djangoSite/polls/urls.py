from django.conf.urls import url
from django.contrib import admin
from . import views
from . import helper

urlpatterns = [
    # ex: /polls/
    url('index', views.index, name='index'),
    url('contact', views.contact, name='contact'),
    url('search', views.search, name='search'),
   # url(r'^LoadDbFolder/', helper.insert_songs_to_db_from_db_folder, name='insert to db all songs from db folder'),
    url(r'^LoadTsvFile/', helper.insert_cities_in_song_to_db_from_file,name='insert to db all songs from file'),
    url(r'^deletelocations/', helper.delete_locations,name='delete all locations'),
    url(r'^findbyid/([0-9]+)/$', views.find_song_by_id, name = 'find by id'),
    url(r'^findbyid/([0-9]+)/delete/(.*)/$', views.remove_city_by_song_id, name='delete city by id'),
    url(r'^removebyid/([0-9]+)/$', views.remove_city_by_song_id, name='find by id'),
    url(r'^downloadti/([0-9]+)/$', views.download_ti_by_song_id, name='find by id'),
    url(r'^admin/', admin.site.urls),
    url(r'^api/get_drugs/', views.get_locations_list, name='get_drugs'),
    url(r'^api/get_artists/', views.get_artists_list, name='get_artists'),
    url(r'^map/(.*)/$', views.get_locations_to_map, name='get_map'),
    url(r'^createdict/', views.create_dict,name='insert to db all songs from file'),

]
#
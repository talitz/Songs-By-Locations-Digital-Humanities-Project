from django.conf.urls import url
from django.contrib import admin
from . import views
from . import helper

urlpatterns = [
    # ex: /polls/
    url('index', views.index, name='index'),
    url('contact', views.contact, name='contact'),
    url('search', views.search, name='search'),
    url(r'^LoadDbFolder/', helper.insert_songs_to_db_from_db_folder, name='insert to db all songs from db folder'),
    url(r'^LoadTsvFile/', helper.insert_cities_in_song_to_db_from_file,name='insert to db all songs from file'),
    url(r'^findbyid/([0-9]+)/$', views.find_song_by_id, name = 'find by id'),
    url(r'^findbyid/([0-9]+)/delete/(.*)/$', views.remove_city_by_song_id, name='delete city by id'),
    url(r'^removebyid/([0-9]+)/$', views.remove_city_by_song_id, name='find by id'),
    url(r'^downloadti/([0-9]+)/$', views.download_ti_by_song_id, name='find by id'),
    url(r'^admin/', admin.site.urls),
]

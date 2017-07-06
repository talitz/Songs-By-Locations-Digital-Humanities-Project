from django.conf.urls import url
from django.contrib import admin
from . import views
from . import helper

urlpatterns = [
    # ex: /polls/
    url('index', views.index, name='index'),
    # ex: /polls/5/
    url(r'^addSongsToDbFromDbFolder/', helper.insert_songs_to_db_from_db_folder, name='insert to db all songs from file'),
    # ex: /polls/5/results/
    url(r'^findbyid/([0-9]+)/$', views.find_song_by_id, name = 'find by id'),
    url(r'^admin/', admin.site.urls),
]

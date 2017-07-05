from django.conf.urls import url
from django.contrib import admin
from . import views
from . import helper

urlpatterns = [
    # ex: /polls/
    url('index', views.index, name='index'),
    # ex: /polls/5/
    url(r'^(?P<file_name_to_open>[a-z]+)/updateDb/$', helper.insert_to_db_from_file, name='insert to db from file'),
    # ex: /polls/5/results/
    url(r'^findbyid/([0-9]+)/$', views.find_song, name = 'find by id'),
    url(r'^admin/', admin.site.urls),
]

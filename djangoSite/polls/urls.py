from django.conf.urls import url

from . import views
from . import helper

urlpatterns = [
    # ex: /polls/
    url(r'^$', views.index, name='index'),
    # ex: /polls/5/
    url(r'^(?P<file_name_to_open>[a-z]+)/updateDb/$', helper.insert_to_db_from_file, name='insert to db from file'),
    # ex: /polls/5/results/
    url(r'^(?P<song_id>[0-9]+)/results/$', views.results, name='results'),
]

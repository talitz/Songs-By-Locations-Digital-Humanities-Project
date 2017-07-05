from django.conf.urls import url

from . import views

urlpatterns = [
    #url(r'^$', views.index, name='index'),
    # ex: /polls/5/
    url(r'^(?P<song_cities>[a-z]+)/$', views.cityName, name='detail'),
    # ex: /polls/5/results/
    url(r'^(?P<song_id>[0-9]+)/results/$', views.results, name='results'),
]

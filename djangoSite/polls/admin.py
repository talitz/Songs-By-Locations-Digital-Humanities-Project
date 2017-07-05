from django.contrib import admin

from .models import Song
from .models import CitiesInSong

admin.site.register(Song)
admin.site.register(CitiesInSong)

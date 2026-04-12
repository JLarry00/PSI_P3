from django.contrib import admin

# Register your models here.
from .models import Song, SongUser

admin.site.register(Song)
admin.site.register(SongUser)

from django.contrib import admin
from .models import Artist, Genre, Language, Song, Group, WaitList, Actions, Blocus
# Register your models here.

admin.site.register(Artist)
admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(Song)
admin.site.register(Group)
admin.site.register(WaitList)
admin.site.register(Actions)
admin.site.register(Blocus)

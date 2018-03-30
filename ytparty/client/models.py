from django.db import models
import uuid
from django.urls import reverse


# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=20, help_text="Entrez un genre musical.")

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=20, help_text="Entrez la langue des paroles.")

    def __str__(self):
        return self.name



class Artist(models.Model):
    name = models.CharField(max_length=100, help_text="Entrez un nom d'artiste.")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('artist-detail', args=[str(self.id)])

    def get_update_url(self):
        return reverse('artist-update', args=[str(self.id)])

    def get_delete_url(self):
        return reverse('artist-delete', args=[str(self.id)])

class Group(models.Model):
    name = models.CharField(max_length=50, help_text="Entrez un nom de groupe.")
    members = models.ManyToManyField(Artist, help_text="Choisissez les membres du groupe.",blank="True")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]

    def get_absolute_url(self):
        return reverse('group-detail', args=[str(self.id)])

    def get_update_url(self):
        return reverse('group-update', args=[str(self.id)])

    def get_delete_url(self):
        return reverse('group-delete', args=[str(self.id)])


class Song(models.Model):
    title = models.CharField(max_length=50, help_text="Titre de la chanson")
    ytid = models.CharField(max_length=30, help_text="Youtube Id.")
    genre = models.ManyToManyField(Genre, help_text="Choisissez un genre musical.", blank=True)
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True, blank=True)
    artist = models.ManyToManyField(Artist, help_text="Choisissez les artistes.", blank=True)
    group = models.ForeignKey('Group', on_delete=models.SET_NULL, null=True, blank=True)
    duration = models.CharField(max_length=20, help_text="Durée de la chanson")
    img = models.CharField(max_length=100, help_text="Image de la chanson")


    def __str__(self):
        return self.title

    class Meta:
        ordering = ["title"]

    def get_absolute_url(self):
        return reverse('song-detail', args=[str(self.id)])

    def get_update_url(self):
        return reverse('song-update', args=[str(self.id)])

    def get_delete_url(self):
        return reverse('song-delete', args=[str(self.id)])


class WaitList(models.Model):
    title = models.CharField(max_length=100, help_text="Titre")
    img = models.CharField(max_length=100, help_text="Image de la chanson")
    ytid = models.CharField(max_length=30, help_text="Youtube Id.")
    duration = models.CharField(max_length=20, help_text="Durée de la chanson")
    time = models.DateTimeField(auto_now_add=True)
    requestid = models.UUIDField(default=uuid.uuid4, help_text="Unique request ID")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["time"]

class Actions(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=10, help_text="Titre")

    class Meta:
        ordering = ["time"]

class Blocus(models.Model):
    name = models.CharField(max_length=20, help_text="Blocus des commandes.")

    def __str__(self):
        return self.name

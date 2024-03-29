import time
from django.db import models


class Artist(models.Model):

    name = models.CharField(max_length=100)
    img = models.CharField(max_length=250)
    bio = models.TextField(max_length=500)
    verified_artist = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Song(models.Model):

    title = models.CharField(max_length=150)
    length = models.IntegerField(default=0)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name="songs")

    def __str__(self):
        return self.title

    def get_length(self):
        return time.strftime("%-M:%S", time.gmtime(self.length))

class Playlist(models.Model):

    title = models.CharField(max_length=150)
    # this is going to create the many to many relationship and join table
    songs = models.ManyToManyField(Song)

    def __str__(self):
        return self.title

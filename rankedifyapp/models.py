from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class Profile(models.Model):
    spotify_username = models.CharField(max_length=100, unique=True)
    forename = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    email = models.EmailField()
    picture = models.ImageField(upload_to='images', blank=True)
    favourite_song = models.CharField(max_length=100)
    favourite_album = models.CharField(max_length=100)
    favourite_artist = models.CharField(max_length=100)
    rank = models.IntegerField()
    listening_minutes = models.IntegerField()
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.spotify_username

    def save(self, *args, **kwargs):
        self.slug = slugify(self.spotify_username)
        super(Profile, self).save(*args, **kwargs)

class Song(models.Model):
    title = models.CharField(max_length=100)
    length = models.CharField(max_length=200)
    song_ID = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.title

class Artist(models.Model):
    name = models.CharField(max_length=100)
    artist_ID = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=100)
    genre_ID = models.CharField(max_length=100, unique=True)



    def __str__(self):
        return self.name
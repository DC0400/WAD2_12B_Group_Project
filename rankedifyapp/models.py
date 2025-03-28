from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.db import models

class Profile(User):
    forename = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='user_photos/', blank=True)
    spotify_username = models.CharField(max_length=150, blank=True, null=True)
    rank = models.IntegerField(default=0)
    top_song = models.CharField(max_length=100, null=True, blank=True)
    listening_minutes = models.IntegerField(default=0)
    last_logged_in = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def name(self):
        return f"{self.forename} {self.surname} - {self.spotify_username}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return self.username

class ListeningMinutesPerTime(models.Model):
    username_minutes = models.ForeignKey(Profile, on_delete=models.CASCADE)
    listening_minutes = models.IntegerField(default=0)
    last_logged_in = models.IntegerField(default=0)


class Artist(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Song(models.Model):
    title = models.CharField(max_length=255)
    length = models.IntegerField()

    def __str__(self):
        return self.title

class Friends(models.Model):
    user1 = models.ForeignKey(Profile, related_name='friends1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(Profile, related_name='friends2', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user1', 'user2')


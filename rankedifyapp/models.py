from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.db import models

class Profile(User):
    forename = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='user_photos/', blank=True, null=True)
    spotify_username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    rank = models.IntegerField(default=0)
    top_song = models.CharField(max_length=100, null=True, blank=True)
    last_logged_in = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def name(self):
        return f"{self.forename} {self.surname} - {self.spotify_username}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.spotify_username)
        super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return self.username


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


class FriendRequest(models.Model):
    from_user = models.ForeignKey(Profile, related_name='sent_friend_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(Profile, related_name='received_friend_requests', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        status = "Accepted" if self.accepted else "Pending"
        return f"{self.from_user.username} -> {self.to_user.username} ({status})"


class Friends(models.Model):
    user1 = models.ForeignKey(Profile, related_name='friends1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(Profile, related_name='friends2', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user1', 'user2')


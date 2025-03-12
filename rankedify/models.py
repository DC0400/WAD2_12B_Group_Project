from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_minutes_listened = models.IntegerField(default=0)  # Stores listening time
    favourite_album = models.CharField(max_length=255, blank=True, null=True)
    favourite_artist = models.CharField(max_length=255, blank=True, null=True)
    favourite_song = models.CharField(max_length=255, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default.jpg', blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.total_minutes_listened} minutes"

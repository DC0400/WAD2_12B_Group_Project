from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["favourite_album", "favourite_artist", "favourite_song", "profile_picture"]

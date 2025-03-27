from django.shortcuts import redirect
from django.urls import path
from rankedifyapp import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'rankedifyapp'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('friends/', views.friends, name='friends'),
    path('error-page/', views.error_page, name="error-page"),
    path('callback/', views.get_spotify_data, name="callback"),
    path('api/receive_tracks/', views.receive_tracks, name='receive_tracks'),
    path('api/receive_minutes/', views.receive_minutes, name='receive_minutes'),
    path('api/receive_profile/', views.receive_profile, name='receive_profile'),
    path('api/receive_photo/', views.receive_photo, name='receive_photo'),
    path('api/receive_spotify_username/', views.receive_spotify_username, name='receive_spotify_username'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
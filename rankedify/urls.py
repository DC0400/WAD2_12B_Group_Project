from django.urls import path
from rankedify import views
from .views import receive_tracks

app_name = 'rankedify'

urlpatterns = [
    path('', views.index, name='index'),
	path("api/receive_tracks/", receive_tracks, name="receive_tracks"),
]
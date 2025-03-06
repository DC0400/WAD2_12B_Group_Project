from django.urls import path
from rankedify import views

app_name = 'rankedify'

urlpatterns = [
    path('', views.index, name='index'),
]
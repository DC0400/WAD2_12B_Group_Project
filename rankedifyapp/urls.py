from django.urls import path
from rankedifyapp import views

app_name = 'rankedifyapp'

urlpatterns = [
    path('/home', views.home, name='home'),
]

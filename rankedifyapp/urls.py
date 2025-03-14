from django.urls import path
from rankedifyapp import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'rankedifyapp'

urlpatterns = [
    path('/home', views.home, name='home'),
    path('/signup', views.signup, name='signup'),
    path('/login', views.login, name='login'),
    path('/friends', views.friends, name='friends')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
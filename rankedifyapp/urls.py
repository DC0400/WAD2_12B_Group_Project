from django.urls import path
from rankedifyapp import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'rankedifyapp'

urlpatterns = [
    path('/home', views.home, name='home'),
    path('/signup', views.signup, name='signup'),
    path('/login', views.user_login, name='login'),
    path('/profile', views.profile, name='profile'),
    path('/friends', views.friends, name='friends'),
    path('/error-page', views.error_page, name="error-page")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
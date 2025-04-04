"""rankedify URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from rankedifyapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.default_page, name='default_page'),
    path('rankedify/', include('rankedifyapp.urls')),
    path('admin/', admin.site.urls),
    path('callback/', views.profile, name='callback'),
    path('new_friend/', views.add_friend, name='add_friend'),
    path('remove_friend/', views.remove_friend, name='remove_friend'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

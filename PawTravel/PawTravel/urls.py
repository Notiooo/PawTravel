"""PawTravel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
# The solution below is experimental and PyCharm's IntelliSense doesn't seem to like it.
# Feel free to change it if you find a more elegant solution.
# # # # # #
import sys

from django.contrib import admin
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from rest_framework import routers
from django.urls import path, include

from . import settings

sys.path.append('..')

from users.views import CustomUserViewSet

# # # # # #

router = routers.DefaultRouter()
router.register(r'users', CustomUserViewSet)

urlpatterns = [
    path('', include('like_system.urls')),
    path('admin/', admin.site.urls),
    path('guides/', include('travel_guides.urls', namespace='travel_guides')),
    path('tinymce/', include('tinymce.urls')),
    path('offers/', include('offers.urls')),
    path('users/', include('django.contrib.auth.urls')),  # logout
    path('users/', include('users.urls')),
    path('avatar/', include('avatar.urls')),


]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

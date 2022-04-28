from rest_framework import viewsets
from django.contrib.auth import views as auth_views

from .models import CustomUser
from .serializers import CustomUserSerializer
from . import forms

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all().order_by('id')
    serializer_class = CustomUserSerializer

class CustomLoginView(auth_views.LoginView):
    # authentication_form = forms.CustomAuthenticationForm
    # Will this view be needed?
    ...
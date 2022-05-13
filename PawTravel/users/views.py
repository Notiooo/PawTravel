from rest_framework import viewsets
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.views import generic

from .models import CustomUser
from .serializers import CustomUserSerializer
from .forms import CustomUserCreationForm

class  SignUpView(generic.CreateView):
    template_name = 'signup.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all().order_by('id')
    serializer_class = CustomUserSerializer
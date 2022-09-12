from django.urls import reverse_lazy
from django.views import generic
from rest_framework import viewsets

from .forms import CustomUserCreationForm
from .models import CustomUser
from .serializers import CustomUserSerializer


class RegisterView(generic.CreateView):
    template_name = 'users/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all().order_by('id')
    serializer_class = CustomUserSerializer


class SignUpView(generic.CreateView):
    template_name = 'users/signup.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')


class ProfileActivitiesView(generic.CreateView):
    template_name = 'users/user_profile_activities.html'
    model = CustomUser
    fields = '__all__'


class ProfileAddedView(generic.CreateView):
    template_name = 'users/user_profile_added.html'
    model = CustomUser
    fields = '__all__'

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


class ProfileActivitiesView(generic.DetailView):
    template_name = 'users/user_profile_activities.html'
    model = CustomUser
    context_object_name = 'user'


class ProfileView(generic.DetailView):
    template_name = 'users/user_profile.html'
    model = CustomUser
    context_object_name = 'user'


class EditProfileView(generic.UpdateView):
    template_name = 'users/edit_profile.html'
    model = CustomUser
    fields = '__all__'


class ManageProfileView(generic.UpdateView):
    template_name = 'users/manage_profile.html'
    model = CustomUser
    fields = '__all__'



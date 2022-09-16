from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import forms
from django.urls import reverse_lazy, reverse
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
    context_object_name = 'user_profile'


class ProfileView(generic.DetailView):
    template_name = 'users/user_profile.html'
    model = CustomUser
    context_object_name = 'user_profile'


class EditProfileView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'users/edit_profile.html'
    model = CustomUser
    fields = ('about_me', )

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('edit_profile')


class ManageProfileView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'users/manage_profile.html'
    model = CustomUser
    fields = ('email', )

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('manage_profile')
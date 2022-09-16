from django import forms
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    about_me = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True)

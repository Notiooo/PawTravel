from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    aboutMe = models.CharField(max_length=100, blank=True),
    email = models.EmailField(unique=True)
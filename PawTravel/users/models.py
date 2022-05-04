from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ... # any additional fields are welcome
    avatar = models.ImageField(default="avatars/default.png")
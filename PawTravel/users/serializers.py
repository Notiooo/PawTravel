from rest_framework import serializers
from .models import CustomUser

# Create your serializers here.

# Serializer for CustomUser model


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
        'id', 'password', 'last_login', 'is_superuser', 'username', 'first_name', 'last_name', 'email', 'is_staff',
        'is_active', 'date_joined', 'groups', 'user_permissions')
        read_only_fields = (
        'id', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'groups', 'user_permissions')

from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistrationSerializer(BaseUserRegistrationSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'first_name', 'last_name', 'phone', 'email', 'password', 'pk', ]
        extra_kwargs = {
            'password': {'write_only': True}
        }


class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'first_name', 'last_name', 'phone', 'email', 'image', 'password', 'pk', ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

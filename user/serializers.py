""" Serializers de Usuario y Perfil """

# Django REST Framework
from rest_framework import serializers

# Modelos
from django.contrib.auth.models import User
from .models import Perfil


class PerfilSerializer(serializers.ModelSerializer):

    class Meta:
        model = Perfil
        fields = ("biografia", "edad", "avatar",)


class UserSerializer(serializers.ModelSerializer):

    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    confirmar = serializers.CharField(min_length=2)

    class Meta:
        model = User
        fields = ("username", "first_name", "email", "last_name", "password", "confirmar")


class UserReadSerializer(serializers.ModelSerializer):

    perfil = PerfilSerializer(required=False)

    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email", "perfil")
""" Views para el modelo Usuario"""

# Python
import json

# Django
from django.core.files import File
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, filters, viewsets

# Django REST Framework
from rest_framework.decorators import action
from rest_framework.response import Response


# Modelos
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import Perfil

# Serializers
from .serializers import UserSerializer, UserReadSerializer

# Permisos
from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import IsUserAccount


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_fields = ("username", "first_name")
    search_fields = ("username", "first_name")
    ordering_fields = ("id", "username")

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retireve':
            return UserReadSerializer
        else:
            return UserSerializer
    
    def get_permissions(self):
        if self.action == "create" or self.action == "login":
            permission_classes = [AllowAny]
        elif self.action == "destroy":
            permission_classes = [IsAuthenticated, IsUserAccount]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwagrs):
        data = request.data
        serializer_class = self.get_serializer_class()
        if data["password"] != data["confirmar"]:
            return Response({"detail": "contraseñas no coinciden"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        data.pop("confirmar")
        usuario = User.objects.create_user(**data)
        perfil = Perfil.objects.create(user=usuario)
        return Response(UserReadSerializer(usuario).data, status.HTTP_201_CREATED)

    @action(methods=["post"], detail=False)
    def login(self, request, *args, **kwargs):
        data = request.data
        try: 
            usuario = User.objects.get(username=data["username"])
            if usuario.check_password(data["password"]):
                token, created = Token.objects.get_or_create(user=usuario)
                serializer = UserReadSerializer(usuario)
                return Response({"user": serializer.data, "token": token.key}, status=status.HTTP_200_OK)
            return Response({"detail": "contraseña incorrecta"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"detail": "No se encontro al usuario"}, status=status.HTTP_404_NOT_FOUND)
        except KeyError as e:
            return Response({"detail": "{} es un campo requerido".format(str(e))}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=["post"], detail=False)
    def logout(self, request, *args, **kwargs):
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Token.DoesNotExist:
            return Response({"detail": "sesion no encontrada."}, status.HTTP_404_NOT_FOUND)
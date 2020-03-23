""" Modelo de Pefil """

# Django
from django.db import models

# Modelos
from django.contrib.auth.models import User


class Perfil(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    biografia = models.TextField(max_length=700, null=True,)
    edad = models.PositiveIntegerField(null=True)
    avatar = models.ImageField('usuario avatar', upload_to='usuarios/perfil', null=True, blank=True)

    def __str__(self):
        return self.user.username

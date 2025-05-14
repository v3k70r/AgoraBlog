from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

def get_default_user():
    return User.objects.get(username='prueba').id  # Asegúrate de que exista

class Publicacion(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    imagen = models.ImageField(upload_to='blog/images/', null=True, blank=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE, default=get_default_user)

    def __str__(self):
        return self.titulo
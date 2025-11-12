from django.db import models
from django.contrib.auth.models import User


class Hexagrama(models.Model):
    numero = models.PositiveSmallIntegerField(unique=True, default=1)
    nombre_chino = models.CharField(max_length=10)
    nombre = models.CharField(max_length=100)
    significado = models.TextField()
    recomendacion = models.TextField()
    monedas = models.JSONField(help_text="Lista de 6 valores: 'yin' o 'yang'")

    def __str__(self):
        return f"{self.numero}. {self.nombre} ({self.nombre_chino})"

class Consulta(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    pregunta = models.TextField()
    hexagrama = models.ForeignKey(Hexagrama, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Consulta de {self.usuario.username} - Hexagrama {self.hexagrama.numero}"

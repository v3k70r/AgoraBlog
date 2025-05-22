from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from blog.models import Publicacion  # Asegúrate que el modelo se importe correctamente
from django.utils import timezone

@receiver(post_save, sender=User)
def bienvenida(sender, instance, created, **kwargs):
    if created:
        try:
            autor_bienvenida = User.objects.get(username='Heraldo')  # cambia esto si usas otro nombre
        except User.DoesNotExist:
            return  # Si el usuario "oraculo" no existe, no hacemos nada

        Publicacion.objects.create(
            titulo=f"¡{instance.first_name} {instance.last_name} ha bajado desde el Olimpo!",
            contenido="¡Atencion todos! demos la bienvenida a nuestro nuevo miembro.",
            autor=autor_bienvenida,
            fecha_publicacion=timezone.now()
        )

from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import User
from core.models import Usuario, Rol, Juego
@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        if instance.is_superuser:
            rol = Rol.get_rol_por_nombre("Chamán")
        else:
            rol = Rol.get_rol_por_nombre("Forastero")

        # Fallback por si no existen aún
        rol = rol or Rol.objects.first()

        Usuario.objects.create(
            user=instance,
            nombre=instance.username,
            apellido="",
            rol=rol
        )
@receiver(post_migrate)
def inicializar_datos(sender, **kwargs):
    Rol.inicializar_roles()
    Juego.inicializar_juegos()
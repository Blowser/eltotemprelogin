from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        from .models import Rol
        # Crear roles iniciales si no existen
        for rol_id, tipo in Rol.ROLES_INICIALES:
            Rol.objects.get_or_create(id_rol=rol_id, defaults={'tipo_rol': tipo})

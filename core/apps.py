from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        import core.signals
        from core.models import Rol, Juego

        Rol.inicializar_roles()
        Juego.inicializar_juegos()

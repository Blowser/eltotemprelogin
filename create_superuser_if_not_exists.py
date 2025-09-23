from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Usuario
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ElTotem.settings')  # Ajustá si tu settings está en otro módulo
django.setup()

class Command(BaseCommand):
    help = 'Crea un superuser y su perfil totémico'

    def handle(self, *args, **kwargs):
        username = 'admin'
        password = 'eltotem123'
        email = 'admin@example.com'

        user, created = User.objects.get_or_create(username=username)
        if created:
            user.email = email
            user.is_staff = True
            user.is_superuser = True
            user.set_password(password)
            user.save()
            self.stdout.write("✅ Chamán creado")

        else:
            user.set_password(password)
            user.save()
            self.stdout.write("🔄 Chamán ya existía, contraseña actualizada")

        if not hasattr(user, 'perfil'):
            Usuario.objects.create(
                user=user,
                nombre='Admin',
                apellido='Totémico',
                rol_id=1  # Asegurate de que exista el rol con ID 1
            )
            self.stdout.write("✅ Perfil totémico creado")
        else:
            self.stdout.write("🔍 El chamán ya tenía perfil")

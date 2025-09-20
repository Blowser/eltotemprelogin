# reset_admin_password.py
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ElTotem.settings")
django.setup()

from django.contrib.auth.models import User

username = "admin"  # cámbialo si tu superuser tiene otro nombre
new_password = "Grupo3ProyectoTitulo"

try:
    user = User.objects.get(username=username)
    user.set_password(new_password)
    user.save()
    print(f"✅ Contraseña de '{username}' cambiada con éxito")
except User.DoesNotExist:
    print(f"❌ El usuario '{username}' no existe")

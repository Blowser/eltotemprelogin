# core/scripts/reset_admin_password.py
import sys
import os
import django

# Agregamos el path raíz del proyecto
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ElTotem.settings')
django.setup()


from django.contrib.auth.models import User

user = User.objects.get(username='admin')
user.set_password('eltotem123')
user.save()

print("✅ Contraseña de 'admin' cambiada con éxito")

# core/scripts/verificar_chaman.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ElTotem.settings')  # Ajustá si tu settings está en otro módulo
django.setup()

from django.contrib.auth import authenticate

from django.contrib.auth.models import User

try:
    user = User.objects.get(username='admin')
    if user.check_password('eltotem123'):
        print(f"✅ Chamán encontrado: {user.username}")
    else:
        print("❌ El chamán no responde. Contraseña incorrecta.")
except User.DoesNotExist:
    print("❌ El chamán no existe.")

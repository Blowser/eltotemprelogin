# core/scripts/verificar_chaman.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ElTotem.settings')  # Ajustá si tu settings está en otro módulo
django.setup()

from django.contrib.auth import authenticate

user = authenticate(username='admin', password='TuPasswordSegura123')
if user:
    print(f"✅ Chamán encontrado: {user.username}")
else:
    print("❌ El chamán no responde. Verificá la contraseña o existencia.")

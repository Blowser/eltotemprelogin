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
    

from django.contrib.auth.models import User
from core.models import Usuario

user = User.objects.get(username='admin')
perfil = Usuario.objects.filter(user=user).first()

if perfil:
    print("✅ El chamán tiene perfil")
else:
    print("❌ El chamán no tiene perfil. Creando...")

    Usuario.objects.create(
        user=user,
        nombre='Admin',
        apellido='Totémico',
        rol_id=1  # Ajustá según tus roles disponibles
    )
    print("✅ Perfil creado con éxito")


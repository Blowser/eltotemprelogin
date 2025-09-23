# core/scripts/verificar_chaman.py

from django.contrib.auth import authenticate

user = authenticate(username='admin', password='TuPasswordSegura123')
if user:
    print(f"✅ Chamán encontrado: {user.username}")
else:
    print("❌ El chamán no responde. Verificá la contraseña o existencia.")

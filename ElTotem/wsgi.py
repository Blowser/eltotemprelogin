"""
WSGI config for ElTotem project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ElTotem.settings')

application = get_wsgi_application()


# Verificar superuser creado
# 🔍 Verificar superuser creado
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()

    for u in User.objects.all():
        print(f"👤 Usuario: {u.username} | Staff: {u.is_staff} | Superuser: {u.is_superuser}")
except Exception as e:
    print(f"⚠️ Error al listar usuarios: {e}")

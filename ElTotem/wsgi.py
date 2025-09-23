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
# 🔥 Invocar al chamán si no existe
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()

    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='TuPasswordSegura123'
        )
        print("🔥 Superusuario creado desde wsgi")
    else:
        print("🧙‍♂️ Superusuario ya existe")
except Exception as e:
    print(f"⚠️ Error creando superusuario: {e}")

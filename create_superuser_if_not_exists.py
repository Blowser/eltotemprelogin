from django.contrib.auth import get_user_model
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ElTotem.settings')
django.setup()

User = get_user_model()

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='TuPasswordSegura123'
    )
    print("Superuser creado")
else:
    print("Superuser ya existe")


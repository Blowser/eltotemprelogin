import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ElTotem.settings')
django.setup()

from django.contrib.auth.models import User

username = "admin"
email = "admin@example.com"
password = "eltotem123"

user, created = User.objects.get_or_create(username=username)
if created:
    user.email = email
    user.is_staff = True
    user.is_superuser = True
    user.set_password(password)
    user.save()
    print("✅ Chamán creado")
else:
    print("🔍 Chamán ya existía")

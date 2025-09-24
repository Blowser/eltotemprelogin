import os
import django

# 🔮 Inicializa Django correctamente
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ElTotem.settings")
django.setup()


from core.models import Producto
from django.core.files import File

MEDIA_PATH = "media/productos"
asignados = 0

for filename in os.listdir(MEDIA_PATH):
    if filename.endswith(".webp"):
        nombre_base = filename.split("_")[0].lower()
        posibles = Producto.objects.filter(nombre__icontains=nombre_base)

        for producto in posibles:
            if not producto.imagen:
                file_path = os.path.join(MEDIA_PATH, filename)
                with open(file_path, "rb") as f:
                    producto.imagen.save(filename, File(f))
                    producto.save()
                    asignados += 1
                    print(f"🖼️ Imagen asignada a: {producto.nombre}")

print(f"🔮 Total imágenes asignadas: {asignados}")

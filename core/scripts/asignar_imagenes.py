import os
from django.core.files import File
from core.models import Producto

# Ruta al altar local
MEDIA_PATH = "media/productos"

# Recorremos cada archivo en la carpeta
for filename in os.listdir(MEDIA_PATH):
    if filename.endswith(".webp"):
        # Intentamos encontrar un producto cuyo nombre esté contenido en el nombre del archivo
        nombre_base = filename.split("_")[0].lower()
        posibles = Producto.objects.filter(nombre__icontains=nombre_base)

        for producto in posibles:
            if not producto.imagen:
                file_path = os.path.join(MEDIA_PATH, filename)
                with open(file_path, "rb") as f:
                    producto.imagen.save(filename, File(f))
                    producto.save()
                    print(f"🖼️ Imagen asignada a: {producto.nombre}")

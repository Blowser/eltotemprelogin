import os
from django.core.files import File
from django.core.management.base import BaseCommand
from core.models import Producto

class Command(BaseCommand):
    help = "Asigna imágenes desde media/productos a productos que no tienen imagen"

    def handle(self, *args, **kwargs):
        media_path = os.path.join("media", "productos")
        asignados = 0

        for filename in os.listdir(media_path):
            if filename.endswith(".webp"):
                nombre_base = filename.split("_")[0].lower()
                posibles = Producto.objects.filter(nombre__icontains=nombre_base)

                for producto in posibles:
                    if not producto.imagen:
                        file_path = os.path.join(media_path, filename)
                        with open(file_path, "rb") as f:
                            producto.imagen.save(filename, File(f))
                            producto.save()
                            asignados += 1
                            self.stdout.write(self.style.SUCCESS(f"🖼️ Imagen asignada a: {producto.nombre}"))

        self.stdout.write(self.style.WARNING(f"🔮 Total imágenes asignadas: {asignados}"))

import os
from django.core.files import File
from django.core.management.base import BaseCommand
from core.models import Producto

class Command(BaseCommand):
    help = "Asigna imágenes desde media/productos a productos que no tienen imagen"

    def handle(self, *args, **kwargs):
        media_path = os.path.join("media", "productos")
        asignados = 0

        try:
            archivos = os.listdir(media_path)
            self.stdout.write(self.style.WARNING(f"📂 Archivos encontrados: {archivos}"))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR("❌ Carpeta media/productos no encontrada"))
            return

        for filename in archivos:
            if filename.endswith(".webp"):
                nombre_base = filename.replace(".webp", "").replace("_", "-").strip().lower()
                self.stdout.write(f"🔎 Buscando producto con slug exacto: '{nombre_base}'")

                try:
                    producto = Producto.objects.get(slug=nombre_base)
                    if not producto.imagen:
                        file_path = os.path.join(media_path, filename)
                        with open(file_path, "rb") as f:
                            producto.imagen.save(filename, File(f))
                            producto.save()
                            asignados += 1
                            self.stdout.write(self.style.SUCCESS(f"🖼️ Imagen asignada a: {producto.nombre}"))
                    else:
                        self.stdout.write(f"⚠️ Producto '{producto.nombre}' ya tiene imagen")
                except Producto.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"❌ No se encontró producto con slug: '{nombre_base}'"))

        self.stdout.write(self.style.WARNING(f"🔮 Total imágenes asignadas: {asignados}"))
#che
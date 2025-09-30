import json
from django.core.management.base import BaseCommand
from core.models import Producto

class Command(BaseCommand):
    help = "Carga productos desde JSON"

    def handle(self, *args, **kwargs):
        with open("core/scripts/productos_exportados.json", "r", encoding="utf-8") as f:
            productos = json.load(f)
            for p in productos:
                Producto.objects.update_or_create(
                    id_producto=p["id_producto"],
                    defaults=p
                )
        self.stdout.write(self.style.SUCCESS("✅ Productos cargados correctamente desde JSON"))

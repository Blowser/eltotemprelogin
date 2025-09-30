import json
from django.core.management.base import BaseCommand
from core.models import Producto

class Command(BaseCommand):
    help = "Exporta productos como JSON"

    def handle(self, *args, **kwargs):
        productos = Producto.objects.all()
        data = []
        for p in productos:
            data.append({
                "id_producto": p.id_producto,
                "nombre": p.nombre,
                "tipo_producto": p.tipo_producto,
                "tipo_accesorio": p.tipo_accesorio,
                "descripcion": p.descripcion,
                "precio_unitario": p.precio_unitario,
                "stock_total": p.stock_total,
                "imagen": str(p.imagen),
                "juego_id": p.juego_id,
                "edicion_id": p.edicion_id,
                "cartas_por_mazo": p.cartas_por_mazo,
                "cartas_por_sobre": p.cartas_por_sobre,
                "tipo_sobre": p.tipo_sobre,
                "slug": p.slug
            })
        with open("core/scripts/productos_exportados.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

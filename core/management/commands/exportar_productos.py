from django.core.management.base import BaseCommand
from core.models import Producto
import html


class Command(BaseCommand):
    help = "Exporta productos como comandos SQL INSERT"

    def handle(self, *args, **kwargs):
        productos = Producto.objects.all()
        with open("core/scripts/productos_exportados.sql", "w", encoding="utf-8") as f:
            for p in productos:
                insert = f"""INSERT INTO core_producto (
  id_producto, nombre, tipo_producto, tipo_accesorio, descripcion,
  precio_unitario, stock_total, imagen, juego_id, edicion_id,
  cartas_por_mazo, cartas_por_sobre, tipo_sobre, slug
) VALUES (
  {p.id_producto},
  {quote(p.nombre)},
  {quote(p.tipo_producto)},
  {quote_or_null(p.tipo_accesorio)},
  {quote_or_null(p.descripcion)},
  {p.precio_unitario},
  {p.stock_total},
  {quote_or_null(str(p.imagen))},
  {p.juego_id if p.juego_id else 'NULL'},
  {p.edicion_id if p.edicion_id else 'NULL'},
  {p.cartas_por_mazo if p.cartas_por_mazo else 'NULL'},
  {p.cartas_por_sobre if p.cartas_por_sobre else 'NULL'},
  {quote_or_null(p.tipo_sobre)},
  {quote(p.slug)}
);\n"""
                f.write(insert)

def quote(val):
    if val is None:
        return 'NULL'
    val = str(val)
    val = val.replace('"', '\\"')  # escapa comillas dobles
    val = val.replace('\n', ' ').replace('\r', '')  # limpia saltos
    val = val.encode('utf-8', 'ignore').decode('utf-8')  # limpia caracteres rotos
    val = val.replace('\\', '\\\\')  # escapa backslashes
    return f'"{val.strip()}"'




def quote_or_null(val):
    return quote(val) if val else 'NULL'

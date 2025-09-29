from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = "Carga productos desde productos_exportados.sql si la tabla está vacía"

    def handle(self, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM core_producto")
            count = cursor.fetchone()[0]
            if count == 0:
                path = "core/scripts/productos_exportados.sql"
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        sql = f.read()
                    for i, statement in enumerate(sql.split(';')):
                        if statement.strip():
                            try:
                                cursor.execute(statement + ';')
                            except Exception as e:
                                self.stdout.write(self.style.ERROR(f"❌ Error en línea #{i}: {e}"))
                                self.stdout.write(statement)
                    self.stdout.write(self.style.SUCCESS("🔥 Productos cargados exitosamente"))
                except FileNotFoundError:
                    self.stdout.write(self.style.ERROR(f"⚠️ Archivo no encontrado: {path}"))
            else:
                self.stdout.write("⚠️ La tabla ya tiene productos, no se cargó nada.")

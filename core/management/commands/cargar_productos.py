from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = "Carga productos desde productos.sql si la tabla está vacía"

    def handle(self, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM core_producto")
            count = cursor.fetchone()[0]
            if count == 0:
                with open("core/scripts/productos.sql", "r", encoding="utf-8") as f:
                    sql = f.read()
                for statement in sql.split(';'):
                    if statement.strip():
                        cursor.execute(statement + ';')
                self.stdout.write(self.style.SUCCESS("🔥 Productos cargados exitosamente"))
            else:
                self.stdout.write("⚠️ La tabla ya tiene productos, no se cargó nada.")

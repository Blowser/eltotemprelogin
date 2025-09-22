from django.contrib import admin
from .models import (
    Rol, Usuario, Producto, Juego, Edicion, Accesorio,
    FiguraColeccion, Mazo, Sobre, CarroCompras, ItemEnCarro,
    Direccion, Pedido, MetodoPago, Pago, Thread, ForoPost, ForoReporte, NoticiaTCG
)

@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ('id_rol', 'tipo_rol')

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id_usuario', 'nombre_usuario', 'nombre', 'apellido', 'email', 'rol')

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id_producto', 'tipo_producto', 'precio_unitario', 'stock_total')

@admin.register(Juego)
class JuegoAdmin(admin.ModelAdmin):
    list_display = ('id_juego', 'nombre', 'desarrollador', 'sitio_web')

@admin.register(Edicion)
class EdicionAdmin(admin.ModelAdmin):
    list_display = ('id_edicion', 'nombre_edicion', 'fecha_lanzamiento', 'descripcion')

@admin.register(Accesorio)
class AccesorioAdmin(admin.ModelAdmin):
    list_display = ('id_accesorio', 'tipo_accesorio', 'precio_unitario', 'stock', 'producto')

@admin.register(FiguraColeccion)
class FiguraColeccionAdmin(admin.ModelAdmin):
    list_display = ('id_figura', 'precio_unitario', 'stock', 'juego', 'producto')

@admin.register(Mazo)
class MazoAdmin(admin.ModelAdmin):
    list_display = ('id_mazo', 'cartas_por_mazo', 'precio_unitario', 'stock', 'edicion', 'juego', 'producto')

@admin.register(Sobre)
class SobreAdmin(admin.ModelAdmin):
    list_display = ('id_sobre', 'nombre', 'tipo_sobre', 'cartas_por_sobre', 'precio_unitario', 'stock', 'juego', 'edicion', 'producto')

@admin.register(CarroCompras)
class CarroComprasAdmin(admin.ModelAdmin):
    list_display = ('id_carro', 'total_sin_iva', 'iva_compra', 'precio_final', 'fecha_uso', 'usuario')

@admin.register(ItemEnCarro)
class ItemEnCarroAdmin(admin.ModelAdmin):
    list_display = ('id_item', 'cantidad_items', 'precio_unitario', 'total_sin_iva', 'fecha_uso', 'carro', 'producto')

@admin.register(Direccion)
class DireccionAdmin(admin.ModelAdmin):
    list_display = ('id_direccion', 'direccion', 'comuna', 'region', 'codigo_postal', 'usuario')

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id_pedido', 'fecha_pedido', 'estado_pedido', 'total_sin_iva', 'iva_compra', 'precio_final', 'usuario', 'direccion', 'carro')

@admin.register(MetodoPago)
class MetodoPagoAdmin(admin.ModelAdmin):
    list_display = ('id_metodo_pago', 'tipo', 'detalle', 'estado', 'usuario')

@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('id_pago', 'monto', 'estado', 'fecha_proceso', 'pedido', 'metodo_pago')

@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ('id_thread', 'titulo', 'asunto', 'fecha_creacion')

@admin.register(ForoPost)
class ForoPostAdmin(admin.ModelAdmin):
    list_display = ('id_foro_post', 'asunto', 'fecha_creacion', 'usuario', 'thread')

@admin.register(ForoReporte)
class ForoReporteAdmin(admin.ModelAdmin):
    list_display = ('id_foro_reporte', 'motivo', 'fecha_creacion', 'estado', 'foro_post', 'usuario')

@admin.register(NoticiaTCG)
class NoticiaTCGAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'juego', 'tipo_evento', 'fecha')
    search_fields = ('titulo', 'resumen')
    list_filter = ('juego', 'tipo_evento', 'fecha')
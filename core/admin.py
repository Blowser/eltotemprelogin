from django.contrib import admin
from .models import (
    Rol, Usuario, Producto, Juego, Edicion,
    CarroCompras, ItemEnCarro, Direccion, Pedido,
    MetodoPago, Pago, Thread, ForoPost, ForoReporte, NoticiaTCG
)

@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ('id_rol', 'tipo_rol')

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id_usuario', 'get_username', 'nombre', 'apellido', 'get_email', 'rol')
    search_fields = ('nombre', 'apellido', 'user__username', 'user__email')
    list_filter = ('rol',)

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id_producto', 'tipo_producto', 'precio_unitario', 'stock_total')
    list_filter = ('tipo_producto',)

@admin.register(Juego)
class JuegoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'desarrollador', 'sitio_web')
    search_fields = ('nombre',)
    list_filter = ('desarrollador',)

@admin.register(Edicion)
class EdicionAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_edicion', 'fecha_lanzamiento', 'descripcion')
    list_filter = ('fecha_lanzamiento',)
    search_fields = ('nombre_edicion',)


@admin.register(CarroCompras)
class CarroComprasAdmin(admin.ModelAdmin):
    list_display = ('id_carro', 'total_sin_iva', 'iva_compra', 'precio_final', 'fecha_uso', 'usuario')
    list_filter = ('usuario', 'fecha_uso')

@admin.register(ItemEnCarro)
class ItemEnCarroAdmin(admin.ModelAdmin):
    list_display = ('id_item', 'cantidad_items', 'precio_unitario', 'total_sin_iva', 'fecha_uso', 'carro', 'producto')
    list_filter = ('carro', 'producto')

@admin.register(Direccion)
class DireccionAdmin(admin.ModelAdmin):
    list_display = ('id_direccion', 'direccion', 'comuna', 'region', 'codigo_postal', 'usuario')
    list_filter = ('region', 'usuario')

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id_pedido', 'fecha_pedido', 'estado_pedido', 'total_sin_iva', 'iva_compra', 'precio_final', 'usuario', 'direccion', 'carro')
    list_filter = ('estado_pedido', 'usuario', 'fecha_pedido')

@admin.register(MetodoPago)
class MetodoPagoAdmin(admin.ModelAdmin):
    list_display = ('id_metodo_pago', 'tipo', 'detalle', 'estado', 'usuario')
    list_filter = ('estado', 'usuario')

@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('id_pago', 'monto', 'estado', 'fecha_proceso', 'pedido', 'metodo_pago')
    list_filter = ('estado', 'metodo_pago', 'pedido')

@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ('id_thread', 'titulo', 'asunto', 'fecha_creacion')
    list_filter = ('fecha_creacion',)
    search_fields = ('titulo', 'asunto')

@admin.register(ForoPost)
class ForoPostAdmin(admin.ModelAdmin):
    list_display = ('id_foro_post', 'asunto', 'fecha_creacion', 'usuario', 'thread')
    list_filter = ('usuario', 'thread')

@admin.register(ForoReporte)
class ForoReporteAdmin(admin.ModelAdmin):
    list_display = ('id_foro_reporte', 'motivo', 'fecha_creacion', 'estado', 'foro_post', 'usuario')
    list_filter = ('estado', 'usuario', 'foro_post')
    search_fields = ('motivo',)

@admin.register(NoticiaTCG)
class NoticiaTCGAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'juego', 'tipo_evento', 'fecha')
    search_fields = ('titulo', 'resumen')
    list_filter = ('juego', 'tipo_evento', 'fecha')

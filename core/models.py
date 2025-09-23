from django.db import models

class Rol(models.Model):
    id_rol = models.AutoField(primary_key=True)
    tipo_rol = models.CharField(
        max_length=25,
        unique=True,
        help_text="Chamán (Admin), Guardián (Soporte), Aprendíz, Forastero (Usuario)"
    )

    ROLES_INICIALES = [
        (1, "Chamán"),     # Admin
        (2, "Guardián"),   # Soporte
        (3, "Aprendíz"),   # En formación
        (4, "Forastero"),  # Usuario
    ]

    def __str__(self):
        return f"{self.tipo_rol}"

    @classmethod
    def get_rol_por_nombre(cls, nombre):
        return cls.objects.filter(tipo_rol=nombre).first()

    @classmethod
    def inicializar_roles(cls):
        for id_rol, tipo in cls.ROLES_INICIALES:
            cls.objects.get_or_create(id_rol=id_rol, defaults={'tipo_rol': tipo})



###MODELO PARA USUARIOS
from django.contrib.auth.models import User

from django.contrib.auth.models import User

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    nombre = models.CharField(max_length=20)
    apellido = models.CharField(max_length=20)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    rol = models.ForeignKey('core.Rol', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.user.username})"



class Juego(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=255)
    desarrollador = models.CharField(max_length=50)
    sitio_web = models.CharField(max_length=255, help_text="Enlace al sitio web del juego")

    def __str__(self):
        return self.nombre


class Edicion(models.Model):
    nombre_edicion = models.CharField(max_length=50)
    fecha_lanzamiento = models.DateField(null=True, blank=True)
    descripcion = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre_edicion


class Producto(models.Model):
    TIPO_CHOICES = [
        ('kit', 'Kit'),
        ('mazo', 'Mazo'),
        ('sobre', 'Sobre'),
        ('accesorio', 'Accesorio'),
        ('figura', 'Figura de colección'),
        ('plushie', 'Plushie Pokémon'),
    ]

    ACCESORIO_CHOICES = [
        ('portamazo', 'Portamazo'),
        ('tapete', 'Tapete'),
        ('funda', 'Funda de cartas'),
        ('moneda', 'Moneda Pokémon'),
        ('oro', 'Oro holográfico'),
        ('plushie', 'Plushie Pokémon'),
    ]

    id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    tipo_producto = models.CharField(max_length=30, choices=TIPO_CHOICES)
    tipo_accesorio = models.CharField(max_length=40, choices=ACCESORIO_CHOICES, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    precio_unitario = models.IntegerField()
    stock_total = models.IntegerField()
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    juego = models.ForeignKey(Juego, on_delete=models.CASCADE, null=True, blank=True)
    edicion = models.ForeignKey(Edicion, on_delete=models.SET_NULL, null=True, blank=True)

    # Campos opcionales para productos específicos
    cartas_por_mazo = models.IntegerField(blank=True, null=True)
    cartas_por_sobre = models.IntegerField(blank=True, null=True)
    tipo_sobre = models.CharField(max_length=25, blank=True, null=True, help_text="Booster, Starter, etc")

    def __str__(self):
        return self.nombre

class CarroCompras(models.Model):
    id_carro = models.AutoField(primary_key=True)
    total_sin_iva = models.IntegerField()
    iva_compra = models.IntegerField()
    precio_final = models.FloatField()
    fecha_uso = models.DateTimeField(help_text="Para trazabilidad")
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

class ItemEnCarro(models.Model):
    id_item = models.AutoField(primary_key=True)
    cantidad_items = models.IntegerField()
    precio_unitario = models.IntegerField()
    total_sin_iva = models.IntegerField()
    fecha_uso = models.DateTimeField(help_text="Para trazabilidad")
    carro = models.ForeignKey(CarroCompras, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)

class Direccion(models.Model):
    id_direccion = models.AutoField(primary_key=True)
    direccion = models.CharField(max_length=50, help_text="Incluye numeración")
    comuna = models.CharField(max_length=30)
    region = models.CharField(max_length=30)
    codigo_postal = models.IntegerField(null=True, blank=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

class Pedido(models.Model):
    id_pedido = models.AutoField(primary_key=True)
    fecha_pedido = models.DateTimeField()
    estado_pedido = models.CharField(max_length=20)
    total_sin_iva = models.IntegerField()
    iva_compra = models.IntegerField()
    precio_final = models.IntegerField()
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    direccion = models.ForeignKey(Direccion, on_delete=models.CASCADE)
    carro = models.ForeignKey(CarroCompras, on_delete=models.CASCADE)

class MetodoPago(models.Model):
    id_metodo_pago = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=15)
    detalle = models.CharField(max_length=100, null=True, blank=True)
    estado = models.CharField(max_length=15)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

class Pago(models.Model):
    id_pago = models.AutoField(primary_key=True)
    monto = models.IntegerField()
    estado = models.CharField(max_length=15)
    fecha_proceso = models.DateField()
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    metodo_pago = models.ForeignKey(MetodoPago, on_delete=models.CASCADE)

class Thread(models.Model):
    id_thread = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=20)
    asunto = models.CharField(max_length=200)
    fecha_creacion = models.DateField()

class ForoPost(models.Model):
    id_foro_post = models.AutoField(primary_key=True)
    asunto = models.CharField(max_length=255)
    fecha_creacion = models.DateField()
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)

class ForoReporte(models.Model):
    id_foro_reporte = models.AutoField(primary_key=True)
    motivo = models.CharField(max_length=100)
    fecha_creacion = models.DateField()
    estado = models.CharField(max_length=15)
    foro_post = models.ForeignKey(ForoPost, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

# Modelo de sección NOTICIAS (ya pobladas)

class NoticiaTCG(models.Model):
    titulo = models.CharField(max_length=200)
    resumen = models.TextField()
    fecha = models.DateField()
    juego = models.CharField(max_length=50, choices=[
        ('pokemon', 'Pokémon TCG'),
        ('yugioh', 'Yu-Gi-Oh!'),
        ('mitosyleyendas', 'Mitos y Leyendas'),
        ('otros', 'Otros')
    ])
    tipo_evento = models.CharField(max_length=50, choices=[
        ('torneo', 'Torneo'),
        ('lanzamiento', 'Lanzamiento'),
        ('actualizacion', 'Actualización'),
        ('comunidad', 'Comunidad')
    ])
    fuente = models.URLField()
    imagen = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.titulo} ({self.juego})"


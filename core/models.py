from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone


class Rol(models.Model):
    id_rol = models.AutoField(primary_key=True)
    tipo_rol = models.CharField(max_length=25, help_text="Usuario, Admin, Soporte, etc")

    # Lista de roles
    ROLES_INICIALES = [
        (1, 'Admin'),
        (2, 'Usuario')
    ]

    def __str__(self):
        return self.tipo_rol

class UsuarioManager(BaseUserManager):
    def create_user(self, nombre_usuario, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(nombre_usuario=nombre_usuario, email=email, **extra_fields)
        user.set_password(password)  # Hash automático
        user.save(using=self._db)
        return user

class Usuario(AbstractBaseUser):
    nombre_usuario = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=20)
    apellido = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    objects = UsuarioManager()

    USERNAME_FIELD = 'nombre_usuario'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.nombre_usuario


class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    tipo_producto = models.CharField(max_length=30)
    precio_unitario = models.IntegerField()
    stock_total = models.IntegerField()

class Juego(models.Model):
    id_juego = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=255)
    desarrollador = models.CharField(max_length=50)
    sitio_web = models.CharField(max_length=255, help_text="Enlace al sitio web del juego")

class Edicion(models.Model):
    id_edicion = models.AutoField(primary_key=True)
    nombre_edicion = models.CharField(max_length=50)
    fecha_lanzamiento = models.DateField(null=True, blank=True)
    descripcion = models.CharField(max_length=255)

class Accesorio(models.Model):
    id_accesorio = models.AutoField(primary_key=True)
    tipo_accesorio = models.CharField(max_length=40)
    precio_unitario = models.IntegerField()
    stock = models.IntegerField()
    producto = models.OneToOneField(Producto, on_delete=models.CASCADE)

class FiguraColeccion(models.Model):
    id_figura = models.AutoField(primary_key=True)
    precio_unitario = models.IntegerField()
    stock = models.IntegerField()
    juego = models.ForeignKey(Juego, on_delete=models.CASCADE)
    producto = models.OneToOneField(Producto, on_delete=models.CASCADE)

class Mazo(models.Model):
    id_mazo = models.AutoField(primary_key=True)
    cartas_por_mazo = models.IntegerField()
    precio_unitario = models.IntegerField()
    stock = models.IntegerField()
    edicion = models.ForeignKey(Edicion, on_delete=models.CASCADE)
    juego = models.ForeignKey(Juego, on_delete=models.CASCADE)
    producto = models.OneToOneField(Producto, on_delete=models.CASCADE)

class Sobre(models.Model):
    id_sobre = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=255)
    tipo_sobre = models.CharField(max_length=25, help_text="Booster, Starter, etc")
    cartas_por_sobre = models.IntegerField()
    precio_unitario = models.IntegerField()
    stock = models.IntegerField()
    juego = models.ForeignKey(Juego, on_delete=models.CASCADE)
    producto = models.OneToOneField(Producto, on_delete=models.CASCADE)
    edicion = models.ForeignKey(Edicion, on_delete=models.CASCADE)

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

class Rol(models.Model):
    id_rol = models.AutoField(primary_key=True)
    tipo_rol = models.CharField(max_length=25, help_text="Usuario, Admin, Soporte, etc")
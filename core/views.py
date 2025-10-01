#IMPORTACIONE CON COMENTARIOS
from django.shortcuts import render, redirect
#render:Renderiza un template HTML y lo devuelve como respuesta al navegador.
#Se usa para mostrar una página, como login.html, perfil.html, registrarse.html, etc.
#redirect: Redirige al usuario a otra URL o vista, sin mostrar un template.
#Se usa Después de un login exitoso, un registro, un logout, o cualquier acción que no necesita mostrar una página intermedia.

from django.contrib.auth import authenticate, login # para manejar el inicio de sesión
#authenticate(request, username, password):Verifica si el usuario existe y si la contraseña es correcta.
#login(request, user): Si el usuario fue autenticado, lo registra en la sesión activa.

from django.contrib.auth.forms import UserCreationForm
#clase de formulario que Django da lista para usar en el registro de usuarios. 
# Ya incluye validación de contraseñas, verificación de campos, etc.

from django.contrib.auth.decorators import user_passes_test, login_required
#decoradores que se usan para proteger vistas:
#@login_required: Solo permite acceder a la vista si el usuario está logueado.
#@user_passes_test(lambda u: u.is_superuser):Solo permite acceso si el usuario cumple una condición (como ser admin).

from django.views.generic import ListView
#Una de las tantas vistas preconstruidas de django, está basada en clase y sirve para mostrar lista de objetos de un modelo
#Seleccionamos cual modelo mostrar, qué plantilla usar, y cómo filtrar los datos.
from .models import NoticiaTCG
#importamos nuestro modelo personalizado para las noticias, así podemos consultar, fitlrar y mostrar
#“Traéme las runas que definimos para las noticias, que vamos a mostrarlas al clan”.

#IMPORTES PARA SCRAPPING:
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from core.models import NoticiaTCG
from django.http import HttpResponse




# CREACIÓN DE VISTAS
from django.shortcuts import render
from core.models import Producto, Thread, NoticiaTCG
from django.db.models import Count


def index_view(request):
    productos_nuevos = Producto.objects.order_by('-fecha_creacion')[:4]
    publicaciones_populares = Thread.objects.annotate(num_comentarios=Count('comentarios')).order_by('-num_comentarios')[:4]
    noticias_recientes = NoticiaTCG.objects.order_by('-fecha_publicacion')[:4]

    return render(request, 'core/index.html', {
        'productos_nuevos': productos_nuevos,
        'publicaciones_populares': publicaciones_populares,
        'noticias_recientes': noticias_recientes,
    })


# Se define el index para que sea la página principal, este será nuestra página de inicio de la pagina web aquí, en views.py
#El segundo paso será crear la url en url.py tanto de core como de Eltotem, y se crean las rutas
#Tercer paso es agregar 'core' en settings.py de Eltotem en la parte de INSTALLED_APPS

# core/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.utils import timezone
from .models import Usuario, Rol, Direccion

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.hashers import make_password, check_password
from .models import Usuario, Rol, Direccion

# =====================
# REGISTRO
# =====================
from django.contrib.auth.models import User
from django.contrib.auth import login

def registrarse_view(request):
    if request.method == 'POST':
        try:
            username = request.POST['username'].strip()
            nombre = request.POST['nombre'].strip()
            apellido = request.POST['apellido'].strip()
            email = request.POST['email'].strip()
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            direccion_text = request.POST['direccion'].strip()
            numero_dpto_casa = request.POST['numero_dpto_casa'].strip()
            comuna = request.POST['comuna'].strip()
            region = request.POST['region'].strip()

            if password1 != password2:
                return render(request, 'core/registrarse.html', {'error': 'Las contraseñas no coinciden'})

            rol_default, _ = Rol.objects.get_or_create(id_rol=2, defaults={'tipo_rol': 'Usuario'})

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1
            )
            user.first_name = nombre
            user.last_name = apellido
            user.save()

            usuario = user.perfil  # gracias a la señal

            Direccion.objects.create(
                direccion=direccion_text,
                numero_dpto_casa=numero_dpto_casa,
                comuna=comuna,
                region=region,
                usuario=usuario
            )

            login(request, user)  # 🔐 Invoca al espíritu en el altar
            request.session['usuario_id'] = usuario.id
            request.session['registro_exitoso'] = f'Usuario registrado exitosamente. Bienvenido "{username}" al Clan'
            return redirect('perfil')

        except Exception as e:
            return render(request, 'core/registrarse.html', {'error': f'Ocurrió un error inesperado: {e}'})

    return render(request, 'core/registrarse.html')

# =====================
# LOGIN
# =====================
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username'].strip()
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # o 'perfil' si querés ir directo al altar
        else:
            messages.error(request, "⚠️ Usuario o contraseña incorrectos.")
            return redirect('login')  # 🔥 redirige para que el mensaje se muestre

    return render(request, 'core/login.html')
# =====================
# LOGOUT
# =====================
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    list(messages.get_messages(request))  # Consume los mensajes
    return redirect('login')
# =====================
# VER PERFIL
# =====================
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def ver_perfil(request):
    usuario = request.user.perfil
    return render(request, 'core/ver_perfil.html', {'usuario': usuario})

# Vista para la página "Quiénes somos"
def quienes_somos_view(request):
    return render(request, 'core/quienes_somos.html')


#AHORA SE IMPORTA EL VIEWLIST DE LAS NOTICIAS, LUEGO SE CREA LA CLASE PARA FILTRAR
class NoticiasFiltradasView(ListView):
    model = NoticiaTCG
    template_name = 'core/noticias.html'
    context_object_name = 'noticias'

    def get_queryset(self):
        qs = super().get_queryset()
        juego = self.request.GET.get('juego')
        tipo = self.request.GET.get('tipo_evento')
        fecha = self.request.GET.get('fecha')

        if juego:
            qs = qs.filter(juego=juego)
        if tipo:
            qs = qs.filter(tipo_evento=tipo)
        if fecha:
            qs = qs.filter(fecha__gte=fecha)

        return qs.order_by('-fecha')
# VISTAS PARA SCRAPPING:

from datetime import datetime
import requests
from bs4 import BeautifulSoup
from django.http import HttpResponse
from .models import NoticiaTCG

def parse_fecha(texto):
    meses = {
        'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4,
        'mayo': 5, 'junio': 6, 'julio': 7, 'agosto': 8,
        'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
    }
    partes = texto.split()
    dia = int(partes[0])
    mes = meses[partes[1].lower()]
    año = int(partes[2])
    return datetime(año, mes, dia).date()

def extraer_url_de_style(style):
    inicio = style.find("url(") + 4
    fin = style.find(")", inicio)
    url_relativa = style[inicio:fin].strip("'\"")
    return "https://www.yugioh-card.com" + url_relativa

def obtener_fecha_desde_articulo(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        fecha_tag = soup.find('p', class_='date')  # Ajustar si cambia
        if fecha_tag:
            return datetime.strptime(fecha_tag.text.strip(), "%B %d, %Y").date()
    except Exception as e:
        print("Error al obtener fecha:", e)
    return datetime.today().date()

def scrap_tcg(request):
    # 🔹 Yu-Gi-Oh!
    url_yugi = "https://www.yugioh-card.com/eu/es/noticias/"
    response_yugi = requests.get(url_yugi)
    soup_yugi = BeautifulSoup(response_yugi.text, 'html.parser')
    noticias_yugi = soup_yugi.find_all('article', class_='news-tile')
    print("Noticias Yu-Gi-Oh encontradas:", len(noticias_yugi))

    for item in noticias_yugi:
        titulo_tag = item.find('h2', class_='news-tile__heading')
        resumen_tag = item.find('p', class_='news-tile__excerpt')
        fecha_tag = item.find('p', class_='news-tile__date')
        imagen_style = item.find('div', class_='news-tile__image')['style']
        enlace_tag = item.find('a', class_='news-tile__link')

        titulo = titulo_tag.text.strip() if titulo_tag else "Sin título"
        resumen = resumen_tag.text.strip() if resumen_tag else "Sin resumen"
        fecha = parse_fecha(fecha_tag.text.strip()) if fecha_tag else datetime.today().date()
        fuente = "https://www.yugioh-card.com" + enlace_tag['href'] if enlace_tag else url_yugi
        imagen = extraer_url_de_style(imagen_style) if imagen_style else None

        obj, creado = NoticiaTCG.objects.get_or_create(
            fuente=fuente,
            defaults={
                'titulo': titulo,
                'resumen': resumen,
                'fecha': fecha,
                'juego': 'yugioh',
                'tipo_evento': "actualizacion",
                'imagen': imagen
            }
        )
        print("Yu-Gi-Oh:", "Guardada" if creado else "Ya existía", titulo)

    # 🔹 Pokeguardian (fuente alternativa Pokémon TCG)
    url_pg = "https://www.pokeguardian.com/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response_pg = requests.get(url_pg, headers=headers)
    soup_pg = BeautifulSoup(response_pg.text, 'html.parser')
    noticias_pg = soup_pg.find_all('article', class_='jw-news-post')
    print("Noticias Pokeguardian encontradas:", len(noticias_pg))

    for item in noticias_pg:
        titulo_tag = item.find('h2', class_='jw-news-post__title')
        resumen_tag = item.find('div', class_='jw-news-post__lead')
        fecha_tag = item.find('span', class_='jw-news-date')
        enlace_tag = item.find('a', class_='jw-news-color-heading')
        imagen_style = item.find('div', style=lambda s: s and 'background-image' in s)

        titulo = titulo_tag.text.strip() if titulo_tag else "Sin título"
        resumen = resumen_tag.text.strip() if resumen_tag else "Sin resumen"
        try:
            fecha = datetime.strptime(fecha_tag.text.strip(), "%d %b %Y").date() if fecha_tag else datetime.today().date()
        except:
            fecha = datetime.today().date()
        fuente = "https://www.pokeguardian.com" + enlace_tag['href'] if enlace_tag else url_pg
        imagen = None
        if imagen_style:
            style = imagen_style['style']
            inicio = style.find("url(") + 4
            fin = style.find(")", inicio)
            imagen = style[inicio:fin].strip("'\"")

        obj, creado = NoticiaTCG.objects.get_or_create(
            fuente=fuente,
            defaults={
                'titulo': titulo,
                'resumen': resumen,
                'fecha': fecha,
                'juego': 'pokemon',
                'tipo_evento': "actualizacion",
                'imagen': imagen
            }
        )
        print("Pokeguardian:", "Guardada" if creado else "Ya existía", titulo)
    # 🔹 Mitos y Leyendas
    url_myl = "https://casamyl.cl/blogs/myl"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response_myl = requests.get(url_myl, headers=headers)
    soup_myl = BeautifulSoup(response_myl.text, 'html.parser')
    noticias_myl = soup_myl.find_all('li', class_='grid__item')
    print("Noticias Mitos y Leyendas encontradas:", len(noticias_myl))

    for item in noticias_myl:
        enlace_tag = item.find('a', class_='article__link')
        titulo_tag = item.find('h2', class_='article__title')
        resumen_tag = item.find('div', class_='rte article__grid-excerpt')
        fecha_tag = item.find('time')
        imagen_tag = item.find('img')

        titulo = titulo_tag.text.strip() if titulo_tag else "Sin título"
        resumen = resumen_tag.text.strip() if resumen_tag else "Sin resumen"
        fecha = datetime.strptime(fecha_tag['datetime'][:10], "%Y-%m-%d").date() if fecha_tag else datetime.today().date()
        fuente = "https://casamyl.cl" + enlace_tag['href'] if enlace_tag else url_myl
        imagen = "https:" + imagen_tag['src'] if imagen_tag and 'src' in imagen_tag.attrs else None

        obj, creado = NoticiaTCG.objects.get_or_create(
            fuente=fuente,
            defaults={
                'titulo': titulo,
                'resumen': resumen,
                'fecha': fecha,
                'juego': 'mitosyleyendas',
                'tipo_evento': "actualizacion",
                'imagen': imagen
            }
        )
        print("Mitos y Leyendas:", "Guardada" if creado else "Ya existía", titulo)

    return HttpResponse("Scraping combinado de TCG completado.")
###VIEWS DE PRODUCTOS
from django.views.generic import ListView
from .models import Producto

from django.http import HttpResponseServerError

def ProductosView(request):
    juego = request.GET.get('juego')
    tipo = request.GET.get('tipo')

    productos = Producto.objects.all()

    if juego:
        productos = productos.filter(juego__nombre__icontains=juego)

    if tipo:
        productos = productos.filter(tipo_producto=tipo)

    return render(request, 'core/productos.html', {'productos': productos})

        
### VIEWS PARA LOS DETALLES DE LOS PRODUCTOS
from django.shortcuts import get_object_or_404

def detalle_producto(request, id):
    producto = get_object_or_404(Producto, id_producto=id)
    return render(request, 'core/detallesproducto.html', {'producto': producto})


def ProductosView(request):
    juego = request.GET.get('juego')
    tipo = request.GET.get('tipo')

    productos = Producto.objects.all()

    if juego:
        productos = productos.filter(juego__nombre__icontains=juego)

    if tipo:
        productos = productos.filter(tipo_producto=tipo)

    return render(request, 'core/productos.html', {'productos': productos})

###VIEWS PARA ACCESORIOS
def AccesoriosView(request):
    tipo = request.GET.get('tipo')
    juego = request.GET.get('juego')

    accesorios = Producto.objects.filter(tipo_producto='accesorio')

    if tipo:
        accesorios = accesorios.filter(tipo_accesorio=tipo)

    if juego:
        accesorios = accesorios.filter(juego__nombre__icontains=juego)

    return render(request, 'core/accesorios.html', {'accesorios': accesorios})


 ###VIEWS PARA FORO:
from django.shortcuts import render, redirect, get_object_or_404
from core.models import Thread, ForoPost
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from core.models import Thread

@login_required(login_url='/login/')
def crear_thread(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        asunto = request.POST.get('asunto')
        imagen = request.FILES.get('imagen')

        if titulo and asunto:
            Thread.objects.create(
                titulo=titulo,
                asunto=asunto,
                usuario=request.user.perfil,
                imagen=imagen
            )
            messages.success(request, "🔥 Hilo creado con imagen. El fuego ha sido encendido.")
            return redirect('ver_threads')
        else:
            messages.error(request, "⚠️ Faltan inscripciones. El hilo no puede nacer sin título y asunto.")
    return render(request, 'core/crear_thread.html')

   
def ver_threads(request):
    hilos = Thread.objects.order_by('-fecha_creacion')
    return render(request, 'core/ver_threads.html', {'hilos': hilos})


@login_required(login_url='/login/')
def crear_post(request, thread_id):
    hilo = get_object_or_404(Thread, id_thread=thread_id)
    if request.method == 'POST':
        asunto = request.POST.get('asunto')
        imagen = request.FILES.get('imagen')  # 🔥 Captura la imagen

        if asunto:
            ForoPost.objects.create(
                asunto=asunto,
                usuario=request.user.perfil,
                thread=hilo,
                imagen=imagen  # 🔥 Aquí la pasamos al modelo
            )
            messages.success(request, "🔥 Respuesta enviada con imagen. El fuego crece.")
            return redirect('detalle_thread', thread_id=thread_id)
        else:
            messages.error(request, "⚠️ El mensaje está vacío. No se puede encender sin palabras.")
    return render(request, 'core/crear_post.html', {'hilo': hilo})




def detalle_thread(request, thread_id):
    hilo = get_object_or_404(Thread, id_thread=thread_id)
    posts = ForoPost.objects.filter(thread=hilo).order_by('fecha_creacion')
    return render(request, 'core/detalle_thread.html', {'hilo': hilo, 'posts': posts})

###VIEWS DE CARRITO
from core.models import CarroCompras, ItemEnCarro, Producto, Pedido, MetodoPago, Pago
from datetime import datetime

@login_required(login_url='login')
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id_producto=producto_id)
    cantidad = int(request.POST.get('cantidad', 1))

    carro = CarroCompras.objects.filter(usuario=request.user.perfil).order_by('-fecha_uso').first()
    if not carro:
        carro = CarroCompras.objects.create(
            usuario=request.user.perfil,
            fecha_uso=datetime.now(),
            total_sin_iva=0,
            iva_compra=0,
            precio_final=0
        )

    item, creado = ItemEnCarro.objects.get_or_create(
        carro=carro,
        producto=producto,
        defaults={
            'cantidad_items': cantidad,
            'precio_unitario': producto.precio_unitario,
            'total_sin_iva': cantidad * producto.precio_unitario,
            'fecha_uso': datetime.now()
        }
    )

    if not creado:
        item.cantidad_items += cantidad
        item.total_sin_iva = item.cantidad_items * item.precio_unitario
        item.save()

    messages.success(request, f"🛒 Se agregaron {cantidad} unidades al carrito.")
    return redirect('ver_carrito')


@login_required(login_url='login')
def ver_carrito(request):
    carro = CarroCompras.objects.filter(usuario=request.user.perfil).order_by('-fecha_uso').first()
    items = ItemEnCarro.objects.filter(carro=carro) if carro else []
    total = sum(item.total_sin_iva for item in items)
    iva = int(total * 0.19)
    precio_final = total + iva

    return render(request, 'core/ver_carrito.html', {
        'items': items,
        'total': total,
        'iva': iva,
        'precio_final': precio_final
    })

@login_required(login_url='login')
def eliminar_item_carrito(request, item_id):
    item = get_object_or_404(ItemEnCarro, id_item=item_id, carro__usuario=request.user.perfil)
    item.delete()

    # Actualizar totales del carrito
    item.carro.actualizar_totales()

    messages.success(request, f"🧹 Se eliminó {item.producto.nombre} del carrito.")
    return redirect('ver_carrito')

@login_required(login_url='login')
def finalizar_compra(request):
    perfil = request.user.perfil
    carro = CarroCompras.objects.filter(usuario=perfil).order_by('-fecha_uso').first()
    direccion = Direccion.objects.filter(usuario=perfil).first()
    metodo = MetodoPago.objects.filter(usuario=perfil).first()

    if not carro or not direccion or not metodo:
        messages.error(request, "Falta dirección, método de pago o carrito.")
        return redirect('ver_carrito')

    total = carro.total_sin_iva
    iva = carro.iva_compra
    precio_final = carro.precio_final

    pedido = Pedido.objects.create(
        fecha_pedido=datetime.now(),
        estado_pedido="pendiente",
        total_sin_iva=total,
        iva_compra=iva,
        precio_final=precio_final,
        usuario=perfil,
        direccion=direccion,
        carro=carro
    )

    Pago.objects.create(
        monto=precio_final,
        estado="pendiente",
        fecha_proceso=datetime.now(),
        pedido=pedido,
        metodo_pago=metodo
    )

    messages.success(request, "🎉 Pedido registrado. El ritual está completo.")
    return redirect('ver_carrito')  # O donde quieras mostrar el resumen

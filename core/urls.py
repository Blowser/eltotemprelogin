# core/urls.py

from django.urls import path
from . import views
from .views import ProductosView, AccesoriosView, crear_thread, ver_threads, crear_post, detalle_thread, ver_carrito, finalizar_compra
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index_view, name='index'),
    path('registrarse/', views.registrarse_view, name='registrarse'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.ver_perfil, name='ver_perfil'),
    path('perfil/metodo/agregar/', views.agregar_metodo_pago, name='agregar_metodo_pago'),
    path('quienes-somos/', views.quienes_somos_view, name='quienes_somos'),
    path('noticias/', views.NoticiasFiltradasView.as_view(), name='noticias'),
    path('scrap-tcg/', views.scrap_tcg, name='scrap_tcg'),
    path('productos/', ProductosView, name='productos'),
    path('producto/<int:id>/', views.detalle_producto, name='detalle_producto'),
    path('accesorios/', AccesoriosView, name='accesorios'),
    path('foro/crear/', crear_thread, name='crear_thread'),
    path('foro/', ver_threads, name='ver_threads'),
    path('foro/<int:thread_id>/responder/', crear_post, name='crear_post'),
    path('foro/<int:thread_id>/', detalle_thread, name='detalle_thread'),
    path('carrito/agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/eliminar/<int:item_id>/', views.eliminar_item_carrito, name='eliminar_item_carrito'),
    path('carrito/finalizar/', views.finalizar_compra, name='finalizar_compra'),
    
]

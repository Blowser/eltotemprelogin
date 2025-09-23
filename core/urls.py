# core/urls.py

from django.urls import path
from . import views
from .views import ProductosView, AccesoriosView
urlpatterns = [
    path('', views.index, name='index'),
    path('registrarse/', views.registrarse_view, name='registrarse'),
    path('login/', views.login_view, name='login'),
    path('quienes-somos/', views.quienes_somos_view, name='quienes_somos'),
    path('noticias/', views.NoticiasFiltradasView.as_view(), name='noticias'),
    path('scrap-tcg/', views.scrap_tcg, name='scrap_tcg'),
    path('productos/', ProductosView, name='productos'),
    path('producto/<int:id>/', views.detalle_producto, name='detalle_producto'),
    path('accesorios/', AccesoriosView, name='accesorios'),
]

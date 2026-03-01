from django.urls import path
from .views import hello_world, get_juegos, get_precios_juego, get_categorias

urlpatterns = [
    path('hello/', hello_world, name='hello_world'),
    path('juegos/', get_juegos, name='get_juegos'),
    path('juegos/<int:juego_id>/precios/', get_precios_juego, name='get_precios_juego'),
    path('categorias/', get_categorias, name='get_categorias'),
]

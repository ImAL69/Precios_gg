from django.urls import path
from .views import (
    hello_world, get_juegos, get_precios_juego, get_categorias,
    get_steam_games, get_steam_game_details, get_epic_games
)

urlpatterns = [
    path('hello/', hello_world, name='hello_world'),
    path('juegos/', get_juegos, name='get_juegos'),
    path('juegos/<int:juego_id>/precios/', get_precios_juego, name='get_precios_juego'),
    path('categorias/', get_categorias, name='get_categorias'),
    path('steam/search/', get_steam_games, name='get_steam_games'),
    path('steam/details/<int:app_id>/', get_steam_game_details, name='get_steam_game_details'),
    path('epic/search/', get_epic_games, name='get_epic_games'),
]

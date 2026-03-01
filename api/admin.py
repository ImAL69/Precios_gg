from django.contrib import admin
from .models import Juego, Categoria, Plataforma, Precio

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre_categoria',)

@admin.register(Juego)
class JuegoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'id_categoria', 'fecha_lanzamiento')
    search_fields = ('titulo',)
    list_filter = ('id_categoria',)

@admin.register(Plataforma)
class PlataformaAdmin(admin.ModelAdmin):
    list_display = ('nombre_plataforma',)

@admin.register(Precio)
class PrecioAdmin(admin.ModelAdmin):
    list_display = ('id_juego', 'id_plataforma', 'precio_actual', 'moneda', 'fecha_consulta')
    list_filter = ('id_plataforma', 'moneda')
    search_fields = ('id_juego__titulo',)

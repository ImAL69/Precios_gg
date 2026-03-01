from django.http import JsonResponse
from .models import Juego, Categoria, Plataforma, Precio

def hello_world(request):
    return JsonResponse({"message": "el pepe", "status": "success"})

def get_juegos(request):
    """Obtiene todos los juegos y opcionalmente filtra por nombre"""
    search = request.GET.get('q', None)
    if search:
        juegos = Juego.objects.filter(titulo__icontains=search)
    else:
        juegos = Juego.objects.all()

    data = []
    for juego in juegos:
        data.append({
            "id": juego.id,
            "titulo": juego.titulo,
            "descripcion": juego.descripcion,
            "categoria": juego.id_categoria.nombre_categoria,
            "fecha_lanzamiento": juego.fecha_lanzamiento,
        })
    return JsonResponse(data, safe=False)

def get_precios_juego(request, juego_id):
    """Obtiene los precios de un juego específico en todas sus plataformas"""
    precios = Precio.objects.filter(id_juego_id=juego_id).select_related('id_plataforma')
    data = []
    for p in precios:
        data.append({
            "plataforma": p.id_plataforma.nombre_plataforma,
            "precio": float(p.precio_actual),
            "moneda": p.moneda,
            "fecha_consulta": p.fecha_consulta.isoformat()
        })
    return JsonResponse(data, safe=False)

def get_categorias(request):
    """Obtiene todas las categorías"""
    categorias = Categoria.objects.all()
    data = [{"id": c.id, "nombre": c.nombre_categoria} for c in categorias]
    return JsonResponse(data, safe=False)

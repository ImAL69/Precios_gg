import requests
import os
import re
from django.http import JsonResponse
from dotenv import load_dotenv
from .models import Juego, Categoria, Plataforma, Precio

load_dotenv()
STEAM_API_KEY = os.getenv('STEAM_API_KEY')

def get_steam_price_scraping(app_id):
    """Obtiene el precio de Steam mediante scraping simple si la API falla o no lo tiene"""
    url = f"https://store.steampowered.com/app/{app_id}/?cc=CO"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'es-CO,es;q=0.9'
    }
    try:
        response = requests.get(url, headers=headers, timeout=5)
        # Buscar el patrón de precio en el HTML (ej: "ARS$ 1.200,00" o "Free to Play")
        price_match = re.search(r'discount_final_price">([^<]+)</div>', response.text)
        if price_match:
            return price_match.group(1).strip()

        price_match = re.search(r'game_purchase_price price">([^<]+)</div>', response.text)
        if price_match:
            return price_match.group(1).strip()

        return "N/A"
    except Exception:
        return "N/A"

def hello_world(request):
    return JsonResponse({"message": "el pepe", "status": "success"})

def get_juegos(request):
    """Obtiene todos los juegos y opcionalmente filtra por nombre, incluyendo sus precios"""
    search = request.GET.get('q', None)
    if search:
        juegos = Juego.objects.filter(titulo__icontains=search).prefetch_related('precios__id_plataforma')
    else:
        juegos = Juego.objects.all().prefetch_related('precios__id_plataforma')

    data = []
    for juego in juegos:
        precios = []
        for p in juego.precios.all():
            precios.append({
                "plataforma": p.id_plataforma.nombre_plataforma,
                "precio": float(p.precio_actual),
                "moneda": p.moneda,
            })

        data.append({
            "id": juego.id,
            "titulo": juego.titulo,
            "descripcion": juego.descripcion,
            "categoria": juego.id_categoria.nombre_categoria,
            "fecha_lanzamiento": juego.fecha_lanzamiento,
            "precios": precios
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

def get_steam_games(request):
    """Obtiene una lista de juegos populares de Steam con scraping de respaldo para precios"""
    search_term = request.GET.get('q', 'action')
    url = f"https://store.steampowered.com/api/storesearch/?term={search_term}&l=spanish&cc=CO"

    try:
        response = requests.get(url)
        data = response.json()

        # Si hay juegos, formateamos el precio para el frontend
        if data.get('items'):
            for item in data['items']:
                price_data = item.get('price')
                if price_data and isinstance(price_data, dict):
                    # Formatear precio desde el objeto de Steam
                    final_price = price_data.get('final', 0) / 100
                    currency = price_data.get('currency', 'COP')
                    item['price'] = f"{currency} {final_price:,.2f}"
                elif not price_data:
                    item['price'] = get_steam_price_scraping(item['id'])

        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def get_steam_game_details(request, app_id):
    """Obtiene detalles de un juego específico por su AppID"""
    url = f"https://store.steampowered.com/api/appdetails?appids={app_id}&l=spanish&cc=CO"

    try:
        response = requests.get(url)
        return JsonResponse(response.json(), safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

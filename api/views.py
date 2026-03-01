import requests
import os
import re
from django.http import JsonResponse
from django.core.cache import cache
from dotenv import load_dotenv
from .models import Juego, Categoria, Precio

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
    """Obtiene todos los juegos y opcionalmente filtra por nombre y/o categoría, incluyendo sus precios"""
    search = request.GET.get('q', None)
    categoria_id = request.GET.get('categoria', None)

    juegos = Juego.objects.all().prefetch_related('precios__id_plataforma', 'id_categoria')

    if search:
        juegos = juegos.filter(titulo__icontains=search)
    if categoria_id and categoria_id != '0':
        juegos = juegos.filter(id_categoria_id=categoria_id)

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
    """Obtiene todas las categorías populares de Steam"""
    # Lista extendida de categorías/géneros comunes en Steam
    data = [
        {"id": "1", "nombre": "Acción"},
        {"id": "2", "nombre": "Estrategia"},
        {"id": "3", "nombre": "RPG"},
        {"id": "4", "nombre": "Aventura"},
        {"id": "25", "nombre": "Carreras"},
        {"id": "28", "nombre": "Simulación"},
        {"id": "18", "nombre": "Deportes"},
        {"id": "70", "nombre": "Acceso anticipado"},
        {"id": "23", "nombre": "Indie"},
        {"id": "59", "nombre": "Multijugador masivo"},
        {"id": "37", "nombre": "Free to Play"},
        {"id": "Casual", "nombre": "Casual"},
        {"id": "Horror", "nombre": "Terror"},
        {"id": "Survival", "nombre": "Supervivencia"},
        {"id": "Shooter", "nombre": "Disparos (Shooter)"},
        {"id": "Puzzle", "nombre": "Puzles"},
        {"id": "Platformer", "nombre": "Plataformas"},
        {"id": "Anime", "nombre": "Anime"},
        {"id": "Open World", "nombre": "Mundo Abierto"},
        {"id": "Story Rich", "nombre": "Basado en la historia"},
        {"id": "Co-op", "nombre": "Cooperativo"},
    ]
    # Eliminar duplicados si los hay
    visto = set()
    data_limpia = []
    for item in data:
        if item['nombre'] not in visto:
            data_limpia.append(item)
            visto.add(item['nombre'])

    return JsonResponse(data_limpia, safe=False)

def get_exchange_rate():
    """Obtiene la tasa de cambio USD a COP con caché de 24 horas"""
    rate = cache.get('usd_cop_rate')
    if rate:
        return rate

    try:
        url = "https://api.exchangerate-api.com/v4/latest/USD"
        response = requests.get(url, timeout=5)
        data = response.json()
        rate = data.get('rates', {}).get('COP', 4000) # Fallback razonable
        cache.set('usd_cop_rate', rate, 86400) # 24 horas
        return rate
    except Exception:
        return 4000

def get_epic_games(request):
    """Busca juegos en Epic Games Store usando CheapShark API como respaldo al bloqueo de Epic"""
    search_term = request.GET.get('q', '')
    if not search_term:
        return JsonResponse({"items": []})

    # Intentar obtener de caché
    cache_key = f"epic_search_{search_term.lower()}"
    cached_data = cache.get(cache_key)
    if cached_data:
        return JsonResponse(cached_data, safe=False)

    # StoreID 25 es Epic Games Store en CheapShark
    url = f"https://www.cheapshark.com/api/1.0/deals?storeID=25&title={search_term}"

    try:
        rate = get_exchange_rate()
        response = requests.get(url, timeout=10)
        deals = response.json()

        items = []
        for deal in deals:
            # Formatear precio a COP
            try:
                sale_price_usd = float(deal.get('salePrice', 0))
                price_cop = sale_price_usd * rate
                price_str = f"COP {price_cop:,.2f}"
            except (ValueError, TypeError):
                price_str = "N/A"

            items.append({
                "id": deal.get('gameID'),
                "name": deal.get('title'),
                "price": price_str,
                "tiny_image": deal.get('thumb'),
                "platform": "Epic Games",
                "deal_id": deal.get('dealID') # Útil para enlaces
            })

        result = {"items": items}
        # Guardar en caché por 1 hora para no saturar
        cache.set(cache_key, result, 3600)

        return JsonResponse(result, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def get_steam_games(request):
    """Obtiene una lista de juegos populares de Steam con filtrado por categoría opcional"""
    search_term = request.GET.get('q', '')
    categoria_id = request.GET.get('categoria', '0')

    # Diccionario extendido para soportar más categorías como términos de búsqueda
    categorias_nombres = {
        "1": "Action", "2": "Strategy", "3": "RPG", "4": "Adventure",
        "25": "Racing", "28": "Simulation", "18": "Sports",
        "70": "Early Access", "23": "Indie", "59": "Massively Multiplayer", "37": "Free to Play",
        "Horror": "Horror", "Survival": "Survival", "Shooter": "Shooter", "Puzzle": "Puzzle",
        "Platformer": "Platformer", "Anime": "Anime", "Open World": "Open World",
        "Story Rich": "Story Rich", "Co-op": "Co-op", "Casual": "Casual"
    }

    # Si hay una categoría seleccionada y no hay término de búsqueda, usamos la categoría como término
    term_to_search = search_term
    if not term_to_search and categoria_id != '0':
        term_to_search = categorias_nombres.get(categoria_id, search_term)

    if not term_to_search:
        term_to_search = 'indie' # Valor por defecto más variado

    url = f"https://store.steampowered.com/api/storesearch/?term={term_to_search}&l=spanish&cc=CO"

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        if data.get('items'):
            for item in data['items']:
                # Formatear precio
                price_data = item.get('price')
                if price_data and isinstance(price_data, dict):
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

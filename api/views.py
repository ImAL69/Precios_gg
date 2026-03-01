from django.http import JsonResponse

def hello_world(request):
    return JsonResponse({"message": "el pepe", "status": "success"})

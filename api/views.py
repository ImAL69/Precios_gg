from django.http import JsonResponse

def hello_world(request):
    return JsonResponse({"message": "Hola desde Django!", "status": "success"})

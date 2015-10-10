from general_views import send_response
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def login(request):
    if request.method == "POST":
        id = request.POST.get('login', False)
        password = request.POST.get('password', False)
        return send_response([1, 1, "admin"])
    else:
        return send_response([1, 1, "admin"])

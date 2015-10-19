from general_views import send_response
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


@csrf_exempt
def login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user = authenticate(username=data['username'], password=data['password'])
        if user is not None:
            if user.is_superuser:
                return send_response([user.id, user.id, "admin"])
            else:
                return send_response("Pas d'utilisateur 1.", 500)
        else:
            return send_response("Pas d'utilisateur 2.", 500)
    else:
        return send_response("Pas d'utilisateur 3.", 500)

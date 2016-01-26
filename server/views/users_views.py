from general_views import send_response
from django.views.decorators.csrf import csrf_exempt
import json
import uuid
from django.contrib.auth import authenticate

@csrf_exempt
def login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user = authenticate(username=data['username'], password=data['password'])
        if user is not None:
            return send_response([user.username, str(uuid.uuid4()), "user", user.id])
        else:
            return send_response("NO_USER", 500)

from general_views import send_response
from django.views.decorators.csrf import csrf_exempt
import json
import uuid
from srcds import SourceRconError
from srcds import SourceRcon
from valve.source.rcon import RCON
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

@csrf_exempt
def login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user = authenticate(username=data['username'], password=data['password'])
        if user is not None:
            return send_response([user.username, str(uuid.uuid4()), "user"])
        else:
            return send_response("NO_USER", 500)

from general_views import send_response
from django.views.decorators.csrf import csrf_exempt
import json
from srcds import SourceRconError
from srcds import SourceRcon
from valve.source.rcon import RCON
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


@csrf_exempt
def login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user = authenticate(username=data['username'], password=data['password'])
        if user is not None:
            return send_response([user.id, user.id, "admin"])
        else:
            return send_response("NO_USER", 500)




'''
if request.method == "POST":
    setting = json.loads(request.body)

    if test_connexion(setting['server'], setting['port'], setting['password']):
        return send_response(True)
    else:
        return send_response("Error", 521)
'''

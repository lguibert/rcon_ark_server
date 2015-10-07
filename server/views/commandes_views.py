from general_views import send_response
import srcds as rcon
import urllib
from django.views.decorators.csrf import csrf_exempt
import json

path = "C:/projects/RCON/mcrcon.exe"
server = "tpdo.fr"
port = 32330
password = "tpdopwd"
con = rcon.SourceRcon(server, port, password, 15)

@csrf_exempt
def execute_command(request):
    if request.method == "POST":
        data = json.loads(request.body)
        cmd = data[0]
        params = data[1]
        if params is not None:
            params = params.split(",")
            params_striged = ''
            for param in params:
                params_striged = params_striged + ' ' + param

            result = create_command(cmd, param)
        else:
            result = create_command(cmd)

        return send_response(result)
    else:
        return send_response("nop")


def create_command(attr, param=None):
    if param:
        result = con.rcon(attr + " " + param)
    else:
        result = con.rcon(attr)

    return result

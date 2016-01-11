from general_views import send_response
from django.views.decorators.csrf import csrf_exempt
import json
from srcds import SourceRconError
from srcds import SourceRcon
from valve.source.rcon import RCON


@csrf_exempt
def login(request):
    if request.method == "POST":
        setting = json.loads(request.body)

        if test_connexion(setting['server'], setting['port'], setting['password']):
            return send_response(True)
        else:
            return send_response("Error", 521)


def test_connexion(server, port, password):
    try:
        con = SourceRcon(server, int(port), password)
        con.connect()
        con.disconnect()
        return True
    except:
        return False


''' svadd = ('tpdo.fr', 32332)

 with RCON(svadd, "arkfree33") as rcon:
     print(rcon('fly'))'''

# try:
# return True
# except SourceRconError:
#    return False

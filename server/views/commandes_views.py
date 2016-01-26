# encoding=utf8
from general_views import send_response
import srcds as rcon
from srcds import SourceRconError
from django.views.decorators.csrf import csrf_exempt
import json
from django.conf import settings
import re
from server.models import Servers

#con = rcon.SourceRcon(settings.SERVER, settings.PORT, settings.PASSWORD, 10)


def create_con(uuid_server):
    server = Servers.objects.get(uuid=uuid_server)
    return rcon.SourceRcon(server.address, server.port, server.password)


@csrf_exempt
def execute_command(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print data
        cmd = data[0]
        params = data[1]
        uuid = data[2]

        try:
            if params is not None:
                params = params.split(",")
                params_striged = ''
                for param in params:
                    params_striged = params_striged + ' ' + param

                result = create_command(cmd, uuid, param)
            else:
                result = create_command(cmd, uuid)

            parsed_result = parse_with(result, cmd.lower())

            return send_response([cmd, parsed_result])
        except SourceRconError:
            return send_response("Serveur non disponible.", 503)
    else:
        return send_response(None, 500)


def create_command(cmd, uuid, param=None):
    print uuid
    con = create_con(uuid)
    if param:
        result = con.rcon(cmd + " " + param)
    else:
        result = con.rcon(cmd)

    return result


def parse_with(result, cmd):
    resulted = None
    if cmd == "listplayers":
        resulted = parse_listplayer(result)

    return resulted


def parse_listplayer(result):
    results = result.split("\n")
    parsed = []
    for player in results:
        if player is not "":
            playered = re.search("(?P<uid>\d*)\. (?P<playername>.+), (?P<steamid>[0-9]+) ?", player)
            if playered:
                parsed.append(playered.groupdict())

    if parsed:
        return parsed
    else:
        return "No player connected"

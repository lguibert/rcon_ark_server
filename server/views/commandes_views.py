# encoding=utf8
from general_views import send_response
import srcds as rcon
from srcds import SourceRconError
from django.views.decorators.csrf import csrf_exempt
import json
from django.conf import settings
import re, os
from server.models import Servers
from datetime import datetime


# con = rcon.SourceRcon(settings.SERVER, settings.PORT, settings.PASSWORD, 10)


def create_con(uuid_server):
    server = Servers.objects.get(uuid=uuid_server)
    return rcon.SourceRcon(server.address, server.port, server.password)


@csrf_exempt
def execute_command(request):
    if request.method == "POST":
        data = json.loads(request.body)
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

            parsed_result = parse_with(result, cmd.lower(), uuid)

            return send_response([cmd, parsed_result])
        except SourceRconError:
            return send_response("Serveur non disponible.", 503)
    else:
        return send_response(None, 500)


def create_command(cmd, uuid, param=None):
    con = create_con(uuid)
    if param:
        result = con.rcon(cmd + " " + param)
    else:
        result = con.rcon(cmd)

    return result


def parse_with(result, cmd, uuid):
    if cmd == "listplayers":
        return parse_listplayer(result)
    elif cmd == "getgamelog":
        return parse_gamelog(result, uuid)
    else:
        return result


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


log_path = "E:/wamp/www/rcon_ark_server/logs"


def parse_gamelog(result, uuid):
    print result
    splited = result.split("\n")

    for i, part in enumerate(splited):
        if part in ["\n", " ", None, "Server received, But no response!! "]:
            splited.pop(i)
    splited.pop(splited.__len__() - 1)  # supprime le caractere vide à la fin qui veut pas partir

    '''splited = ['2016.01.28_14.50.07: SERVER: vous pouvez envoyer plein de message dans le chat please ?',
               '2016.01.28_14.50.10: Colonel Dimanche (Bob): dfsd',
               '2016.01.28_14.50.11: Salem Le Chat (Bob2): sdfgsqdfg',
               '2016.01.28_14.50.11: Colonel Dimanche (Bob): sdf', '2016.01.28_14.50.11: Colonel Dimanche (Bob): sdf',
               '2016.01.28_14.50.11: Salem Le Chat (Bob2): dfsg', '2016.01.28_14.50.11: Colonel Dimanche (Bob): sd',
               '2016.01.28_14.50.12: Salem Le Chat (Bob2): sdfg', '2016.01.28_14.50.12: Salem Le Chat (Bob2): sdfg',
               '2016.01.28_14.50.13: SalemLe Chat (Bob2): sdfg', '2016.01.28_14.50.18: Colonel Dimanche (Bob): dfg',
               "2016.01.28_14.50.28: Salem Le Chat (Bob2): c'est bon?", ' ']'''

    path_todir = log_path + "/" + uuid
    path_tofile = path_todir + "/log.log"

    if not os.access(path_tofile, os.F_OK):
        if not os.path.exists(path_todir):
            os.mkdir(path_todir)

        # os.mknod(path_tofile)
        file(path_tofile, "w").close()

    log = open(path_tofile, "a")
    for i, element in enumerate(splited):
        type = format_html(element)
        element = format_dateandtime(element)
        log.write("<span class='" + type + "'>" + element + "</span><br/>")

    log.close()

    log = open(path_tofile, "r")
    result = log.read()
    log.close()

    return result


def format_html(content):
    if re.search("(.*)was killed by(.*)", content):
        return "kill"
    elif re.search("(.*)joined this ARK!", content):
        return "joinLeft"
    elif re.search("(.*)left this ARK!", content):
        return "joinLeft"
    elif re.search("(.*)was killed!", content):
        return "kill"
    elif re.search("(.*)Tamed a ([A-z ]*) \\- (.*)", content):
        return "tame"
    elif re.search("(.*)SERVER:(.*)", content):
        return "server"
    else:
        return "normal"


def format_dateandtime(element):
    splited = element.split(":",1)
    fulldate = splited[0].split("_")
    date = fulldate[0].split(".")
    time = fulldate[1].split(".")

    finaldate = datetime(int(date[0]), int(date[1]), int(date[2]), int(time[0]), int(time[1]), int(time[2]))
    stringed_finaldate = add_zero(str(finaldate.day)) + '/' + add_zero(str(finaldate.month)) + '/' + add_zero(str(finaldate.year)) + '-' + add_zero(str(
        finaldate.hour)) + ':' + add_zero(str(finaldate.minute)) + ':' + add_zero(str(finaldate.second))

    return "<i>["+stringed_finaldate + "]</i>" + splited[1]


def add_zero(i):
    if len(i) < 2:
        i = "0" + i

    return i

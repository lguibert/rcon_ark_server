from general_views import send_response
import srcds as rcon

path = "C:/projects/RCON/mcrcon.exe"
server = "tpdo.fr"
port = 32330
password = "tpdopwd"
con = rcon.SourceRcon(server, port, password, 15)


def execute_command(request, cmd, params=None):
    if params is not None:
        print params
        params = params.split(",")
        params_striged = ''
        for param in params:
            print param
            params_striged = params_striged + ' ' + param

        result = create_command(cmd, param)
    else:
        result = create_command(cmd)

    return send_response(result)


def create_command(attr, param=None):
    if param:
        result = con.rcon(attr + " " + param)
    else:
        result = con.rcon(attr)

    return result

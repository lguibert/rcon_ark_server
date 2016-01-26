from general_views import send_response, serialize
from django.views.decorators.csrf import csrf_exempt
import json
from server.models import Servers
from django.contrib.auth.models import User
from srcds import SourceRcon, SourceRconError
import time


@csrf_exempt
def get_myservers(request):
    if request.method == "POST":
        username = request.body

        myservers = get_servers_from_username(username)

        return send_response(list(myservers))


def get_servers_from_username(username, values=None):
    user = User.objects.get(username=username)
    if not values:
        return Servers.objects.filter(user=user).values()
    else:
        return Servers.objects.filter(user=user).values(values)


def get_id_server(servers):
    servers_ids = []
    for serv in servers:
        servers_ids.append(serv['id'])
    return servers_ids


@csrf_exempt
def change_myservers(request):
    if request.method == "POST":
        data = json.loads(request.body)
        server = data[0]
        username = data[1]

        if 'id' in server:
            #update

            servers = get_servers_from_username(username, 'id')
            servers_ids = get_id_server(servers)

            if server['id'] in servers_ids:
                update = Servers.objects.get(id=server['id'])
                update.name = server['name']
                update.address = server['address']
                update.port = server['port']
                update.password = server['password']
                update.save()

                return send_response("Update ok")
        else:
            #add
            new = Servers()
            new.name = server['name']
            new.address = server['address']
            new.port = server['port']
            new.password = server['password']
            new.user = User.objects.get(username=username)
            new.save()

            return send_response("Add ok")


@csrf_exempt
def connect_to_server(request):
    if request.method == "POST":
        data = json.load(request)
        server = data[0]
        username = data[1]

        servers = get_servers_from_username(username, 'id')
        servers_ids = get_id_server(servers)

        if server['id'] in servers_ids:
            if test_connection(server):
                return send_response(server['uuid'])
            else:
                return send_response("CO_NOP", 500)
        else:
            return send_response("NOT_ALLOWED", 500)


def test_connection(server):
    try:
        con = SourceRcon(server['address'], int(server['port']), server['password'])
        con.connect()
        con.disconnect()
        return True
    except SourceRconError:
        return False


@csrf_exempt
def delete_server(request):
    if request.method == "POST":
        data = json.load(request)
        server = data[0]
        username = data[1]

        servers = get_servers_from_username(username, 'id')
        servers_ids = get_id_server(servers)

        if server['id'] in servers_ids:
            try:
                Servers.objects.get(id=server['id']).delete()
                return send_response("DELETE_OK")
            except:
                return send_response("ERROR_DELETE", 500)
        else:
            return send_response("NOT_ALLOWED", 500)
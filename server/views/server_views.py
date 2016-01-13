from general_views import send_response, serialize
from django.views.decorators.csrf import csrf_exempt
import json
from server.models import Servers
from django.contrib.auth.models import User
from django.core import serializers
from django.forms.models import model_to_dict


@csrf_exempt
def get_myservers(request):
    if request.method == "POST":
        #data = json.loads(request.body)

        myservers = get_servers_from_username("Lucas")

        return send_response(list(myservers))


def get_servers_from_username(username, values=None):
    user = User.objects.get(username=username)
    if not values:
        return Servers.objects.filter(user=user).values()
    else:
        return Servers.objects.filter(user=user).values(values)


@csrf_exempt
def change_myservers(request):
    if request.method == "POST":
        data = json.loads(request.body)
        server = data[0]
        username = data[1]

        if 'id' in server:
            #update

            servers = get_servers_from_username(username, 'id')
            servers_ids = []
            for serv in servers:
                servers_ids.append(serv['id'])

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

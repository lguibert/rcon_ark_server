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

        user = User.objects.get(username='Lucas')

        myservers = Servers.objects.filter(user=user).values()

        return send_response(list(myservers))


def test_connexion(server, port, password):
    return True
    '''try:
        con = SourceRcon(server, int(port), password)
        con.connect()
        con.disconnect()
        return True
    except:
        return False'''


''' svadd = ('tpdo.fr', 32332)

 with RCON(svadd, "arkfree33") as rcon:
     print(rcon('fly'))'''

# try:
# return True
# except SourceRconError:
#    return False


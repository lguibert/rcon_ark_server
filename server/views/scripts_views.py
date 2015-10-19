from general_views import send_response
import json
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import requests


@csrf_exempt
def execute_script(request):
    #if request.method == "POST":
    data = json.loads(request.body)
    test = "http://" + settings.SERVER + ":" + str(settings.PORT_SCRIPT) + "/" + data
    print test
    #r = requests.get("http://" + settings.SERVER + ":" + str(settings.PORT_SCRIPT) + "/" + data[0])
    return send_response(data) #r.text
    #else:
    #    return send_response("")

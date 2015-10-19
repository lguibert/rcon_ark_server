from general_views import send_response
import srcds as rcon
from django.views.decorators.csrf import csrf_exempt
import json
from django.conf import settings

con = rcon.SourceRcon(settings.SERVER, settings.PORT, settings.PASSWORD, 15)

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
		return send_response("", 500)


def create_command(attr, param=None):
	if param:
		result = con.rcon(attr + " " + param)
	else:
		result = con.rcon(attr)

	return result

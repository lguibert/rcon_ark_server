from general_views import send_response
import os

path = "C:/projects/rcon-ark/media/img/backgrounds"

def backgrounds(request):
    background = None
    for root, subdirs, files in os.walk(path):
        background = files
        break;

    print background

    return send_response(background)
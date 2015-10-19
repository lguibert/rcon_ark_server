from general_views import send_response
import os
from django.conf import settings


def backgrounds(request):
    background = None
    for root, subdirs, files in os.walk(settings.PATH_BACKGROUND):
        background = files
        break

    print background

    return send_response(background)

# -*- coding: utf-8 -*-
from django.http import HttpResponse
import json
from django.core import serializers


def send_response(data, code=200):
    response = HttpResponse(json.dumps(data), content_type='application/json')
    response.status_code = code
    response["Access-Control-Allow-Origin"] = "*"
    return response


def serialize(data):
    return serializers.serialize('json', data)

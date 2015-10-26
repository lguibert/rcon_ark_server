from general_views import send_response
import os
from django.conf import settings
import urllib2
from bs4 import BeautifulSoup
import json


def backgrounds(request):
    background = None
    for root, subdirs, files in os.walk(settings.PATH_BACKGROUND):
        background = files
        break

    return send_response(background)


def get_items(request):
    url = "http://www.ark-survival.net/fr/liste-des-ids-liste-des-items/"
    rqt = urllib2.Request(url, headers={'User-Agent': "Magic Browser"})
    page = urllib2.urlopen(rqt).read()
    soup = BeautifulSoup(page, "lxml")

    trs = soup.table.find_all("tr")
    data = []

    for tr in trs:
        tds = tr.find_all("td")
        tab = []
        for td in tds:
            if td.img:
                tab.append(td.img["src"])
            else:
                tab.append(td.contents[0])
        data.append(tab)

    jsoned = list_to_json(data)

    return send_response(jsoned)


def list_to_json(data):
    js = {}
    for i, line in enumerate(data):
        item = {}
        for y, raw in enumerate(line):
            item.update({correspond_index_name(y): raw})
        js.update({i: item})
        item = {}

    return js


def correspond_index_name(index):
    if index == 0:
        return "icone"
    elif index == 1:
        return "id"
    elif index == 2:
        return "name"
    elif index == 3:
        return "type"
    elif index == 4:
        return "stack"

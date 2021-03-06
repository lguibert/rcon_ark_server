from django.db import models
from django.contrib.auth.models import User
from json import JSONEncoder
from uuid import UUID, uuid4

JSONEncoder_olddefault = JSONEncoder.default
def JSONEncoder_newdefault(self, o):
    if isinstance(o, UUID): return str(o)
    return JSONEncoder_olddefault(self, o)
JSONEncoder.default = JSONEncoder_newdefault


class Servers(models.Model):
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=50)
    port = models.IntegerField()
    password = models.CharField(max_length=200)
    uuid = models.UUIDField(default=uuid4)

    user = models.ForeignKey(User)

    active = models.BooleanField(default=True)

from django.db import models
from django.contrib.auth.models import User


class Servers(models.Model):
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=50)
    port = models.IntegerField()
    password = models.CharField(max_length=200)

    user = models.ForeignKey(User)

    active = models.BooleanField(default=True)

# Create your models here.

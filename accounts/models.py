
from django.contrib.auth.models import User
from django.db import models


class Token(models.Model):
    code = models.IntegerField()
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING) # DO_NOTHING -> if token need to be deleted we don't have to delete the USer. 

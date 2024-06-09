from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Cliente(models.Model):
    id = models.AutoField(primary_key=True)
    id_user = models.OneToOneField(User, on_delete=models.CASCADE)
    celular = models.CharField(max_length=13,default='')
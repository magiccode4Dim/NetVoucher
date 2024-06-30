from django.db import models
from django.utils import timezone

# Create your models here.
class Pacote(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100,default='')
    script = models.CharField(max_length=700,default='')
    #m-h-d-s-m-a minuto,hora,dia,semana,mes,ano
    expira_em = models.CharField(max_length=1000,default='0-0-0-0-0-0')
    device_limit = models.IntegerField(default=1)
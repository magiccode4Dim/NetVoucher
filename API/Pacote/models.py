from django.db import models
from django.utils import timezone

# Create your models here.
class Pacote(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100,default='')
    script = models.CharField(max_length=700,default='')
    preco = models.FloatField(default=0.0)
    expira_em = models.DateTimeField(default=None)
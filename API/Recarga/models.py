from django.db import models
from django.utils import timezone
from Pacote.models import Pacote

# Create your models here.
class Recarga(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=12,default='',unique=True)
    preco = models.FloatField(default=0.0)
    id_pacote = models.ForeignKey(Pacote, on_delete=models.CASCADE)
    is_valid = models.BooleanField(default=True)
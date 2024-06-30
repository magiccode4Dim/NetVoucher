from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from Cliente.models import Cliente
from Recarga.models import Recarga
# Create your models here.

class Compra(models.Model):
    id = models.AutoField(primary_key=True)
    data = models.DateTimeField(default=timezone.now)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    id_recarga = models.OneToOneField(Recarga, on_delete=models.CASCADE)

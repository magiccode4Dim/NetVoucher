from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from Pacote.models import Pacote
from Cliente.models import Cliente
# Create your models here.

class Compra(models.Model):
    id = models.AutoField(primary_key=True)
    data = models.DateTimeField(default=timezone.now)
    id_pacote = models.ForeignKey(Pacote, on_delete=models.CASCADE)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

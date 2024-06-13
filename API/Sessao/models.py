from django.db import models
from Router.models import Router
from Compra.models import Compra


class Sessao(models.Model):
    id = models.AutoField(primary_key=True)
    id_rooter = models.ForeignKey(Router, on_delete=models.CASCADE)
    id_compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    radius_user = models.CharField(max_length=300,default='')
    device = models.CharField(max_length=700,default='')
    expira_em = models.DateTimeField(default=None) #"2024-06-09T12:00:00" preciso fazer um metodo pra calcular dependendo do pacote
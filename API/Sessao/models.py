from django.db import models
from Pacote.models import Pacote
from Router.models import Router
from Cliente.models import Cliente


class Sessao(models.Model):
    id = models.AutoField(primary_key=True)
    id_pacote = models.ForeignKey(Pacote, on_delete=models.CASCADE)
    id_rooter = models.ForeignKey(Router, on_delete=models.CASCADE)
    id_client = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    radius_user = models.CharField(max_length=300,default='')
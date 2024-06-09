from django.db import models
from Router.models import Router

# Create your models here.
class Network(models.Model):
    id = models.AutoField(primary_key=True)
    id_rooter = models.ForeignKey(Router, on_delete=models.CASCADE)
    address = models.CharField(max_length=300,default='')
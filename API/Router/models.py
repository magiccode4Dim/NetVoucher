from django.db import models

# Create your models here.
class Router(models.Model):
    id = models.AutoField(primary_key=True)
    hostname = models.CharField(max_length=100,default='')
    address = models.CharField(max_length=300,default='')

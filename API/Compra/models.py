from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Compra(models.Model):
    id = models.AutoField(primary_key=True)

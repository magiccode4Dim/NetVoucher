from rest_framework import serializers
from .models import Agente

class CompraSerializer(serializers.ModelSerializer):
    class Meta:
        model=Compra
        fields=('id')
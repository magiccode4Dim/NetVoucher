from rest_framework import serializers
from .models import Compra

class CompraSerializer(serializers.ModelSerializer):
    class Meta:
        model=Compra
        fields=('id','data','id_pacote','id_cliente')
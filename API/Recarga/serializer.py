from rest_framework import serializers
from .models import Recarga

class RecargaSerializer(serializers.ModelSerializer):
    class Meta:
        model=Recarga
        fields=('id','code','preco','id_pacote','is_valid')
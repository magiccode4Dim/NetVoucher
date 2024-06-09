from rest_framework import serializers
from .models import Pacote

class PacoteSerializer(serializers.ModelSerializer):
    class Meta:
        model=Pacote
        fields=('id','nome','script','preco','expira_em')